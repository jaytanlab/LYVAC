import os
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import sem

from argparse import ArgumentParser

# get function name
def get_name(my_array):
    return [k for k, v in globals().items() if v is my_array][0]

if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument('--basedir', type=str, default="../", help="base directory")
    parser.add_argument('--directory_name', type=str, default="directory_names.txt", help="directory names")
    parser.add_argument('--mode', type=str, default="dumping")
    # mode: benchmark, dumping, all (default)
    args = parser.parse_args()

    # Set random seed
    random.seed(2023)

    # Open directory name
    with open(args.directory_name, 'r') as fin:
        config_all = fin.readlines()
        config_all = [config.strip() for config in config_all if config != ""]

    # Iterate over all directories
    for rootDir in config_all:
        print("working on directory:", rootDir)
        input_dir = args.basedir + "Data/" + rootDir + "/"
        output_dir = args.basedir + "Bubble/" + rootDir + "/"

        # Get file names and the prefixs
        fileprefixname_list = []
        all_files = os.listdir(input_dir)
        all_files.sort()
        for filename in all_files:
            if filename.endswith(".tif") or filename.endswith(".jpg") or filename.endswith(".png"):
                file_suffix = filename.split("-")[-1]
                file_suffix = file_suffix.split("_")[-1]
                true_name = filename[:-len(file_suffix)]
                if true_name not in fileprefixname_list:
                    fileprefixname_list.append(true_name)
        fileprefixname_list.sort()

        # Iterate over each prefix (e.g. "wt control", "pd8ko control")
        ids, answers = [], []

        for fileprefixname in fileprefixname_list:

            # Iterate over each file with this prefix (fileprefixname)
            # Read file content
            file_answer = []
            for filename in all_files:
                if not filename.startswith(fileprefixname): continue

                file_suffix = filename.split(".")[-1]
                true_name = filename[:-len(file_suffix)]
                output_file = output_dir + true_name + "txt"
                if not os.path.exists(output_file):
                    continue
                with open(output_file, "r") as fin:
                    lines = fin.readlines()
                    file_answer += lines

            # Iterate over the file content and extract information of each cell
            line_no = 0
            cnts, total_areas, each_areas = [], [], []
            while line_no < len(file_answer):
                n, area_wholecell = file_answer[line_no].strip().split(" ")
                n, area_wholecell = int(n), int(area_wholecell)

                total_area_this_cell = 0
                each_area_this_cell = []
                for i in range(n):
                    cur_line_no = line_no + i + 1
                    cur_line = file_answer[cur_line_no]

                    area_this_bubble = float(cur_line.strip())

                    # Filter the bubbles too large. these are wrong outliers
                    if area_this_bubble > 900:
                        continue

                    total_area_this_cell += area_this_bubble
                    each_area_this_cell.append(area_this_bubble)

                # Read the next cell and append the answers
                line_no += n + 1
                
                # Do not consider those cells with too large bubble area
                # most possibly circular dead cells
                if total_area_this_cell / area_wholecell > 0.5:
                    continue

                cnts.append(n)
                total_areas.append(total_area_this_cell / area_wholecell)
                each_areas.append(each_area_this_cell)
            
            # Collect the answer into a dictionary
            answer = {}
            for array in [cnts, total_areas, each_areas]:
                name = get_name(array)[:-1]
                answer[name] = array

            ids.append(fileprefixname[:-1])
            answers.append(answer)

        # Randomly sample same number of cells
        # Use default or mininum number of all folders
        length = 300
        for id, answer in zip(ids, answers):
            now_length = len(answer["cnt"])
            print(f"{id} number of cells detected: {now_length}")
            length = min(length, now_length)
        print(f"Sample {length} cells from all samples")
        
        # Perform sampling
        for idx in range(len(answers)):
            for array_name in ["cnt", "total_area", "each_area"]:
                answers[idx][array_name] = random.sample(answers[idx][array_name], length)

        for array_name in ["total_area"]:
            now_ids, now_answers = [], []
            for id, answer in zip(ids, answers):
                
                if array_name in ["each_area"]:
                    now_arr = [item for cell in answer[array_name] for item in cell]
                else:
                    now_arr = answer[array_name]

                now_ids += [id for i in range(len(now_arr))]
                now_answers += now_arr

            # Benchmark mode for debug
            if args.mode == "benchmark":
                wt, pd8ko1, pd8ko2, pd8ko3, pd8rescue = [], [], [], [], []
                answer_dict = {}
                for id, answer in zip(now_ids, now_answers):
                    if id not in answer_dict:
                       answer_dict[id] = []
                    answer_dict[id].append(answer)

                    if id == "wt treat":
                        wt.append(answer)
                    if id == "pd8ko1 treat":
                        pd8ko1.append(answer)
                    if id == "pd8ko2 treat":
                        pd8ko2.append(answer)
                    if id == "pd8ko3 treat":
                        pd8ko3.append(answer)
                    if id == "pd8ko+pd8fg treat":
                        pd8rescue.append(answer)

                desired_length = 40
                for id, answer in answer_dict.items():
                    print(id.ljust(desired_length), "%.10f" % np.mean(answer))
                
                print("======= Benchmark =======")
                print("WT", np.mean(wt))
                print("PD8KO1", np.mean(pd8ko1))
                print("PD8KO2", np.mean(pd8ko2))
                print("PD8KO3", np.mean(pd8ko3))
                print("PD8Rescue", np.mean(pd8rescue))
                print("WT / PD8KO1", np.mean(wt) / np.mean(pd8ko1))
                print("WT / PD8KO2", np.mean(wt) / np.mean(pd8ko2))
                print("WT / PD8KO3", np.mean(wt) / np.mean(pd8ko3))
                print("WT / PD8Rescue", np.mean(wt) / np.mean(pd8rescue))
                print("Benchmark", np.mean(wt) * 3 / (np.mean(pd8ko1) + np.mean(pd8ko2) + np.mean(pd8ko3)))
                continue

            elif args.mode == "dumping":
                outfile = args.basedir + "Bubble/" + f"results_{rootDir}_{array_name}.csv"

                # create a dictionary where the keys are the ids and the values are lists of answers
                data_dict = {}

                # loop over your data, appending answers to the appropriate list in the dictionary
                for now_id, now_answer in zip(now_ids, now_answers):
                    if now_id not in data_dict:
                        data_dict[now_id] = []
                    data_dict[now_id].append(now_answer)
                
                for key, arr in data_dict.items():
                    print(f"{key:40}: {np.mean(arr)}")
                all_keys = data_dict.keys()
                with open(outfile, "w") as fout:
                    for key in all_keys:
                        fout.write(f"{key},")
                    fout.write("\n")
                    for i in range(length):
                        for key in all_keys:
                            fout.write(f"{data_dict[key][i]},")
                        fout.write("\n")

                # exit(0)
                continue
            
            elif args.mode == "dumping":
                _now_ids, _now_answers = [], []
                for sample_idx, (id, answer) in enumerate(zip(now_ids, now_answers)):
                    if sample_idx % 5 != 0: # sample to 1/5
                        continue
                    if answer > 0.3:
                        continue
                    if answer < 0.00001:
                        _now_ids.append(id)
                        random_num = random.random()
                        if sample_idx % 4 == 0:
                            _now_answers.append(answer)
                        elif sample_idx % 4 == 1:
                            _now_answers.append(answer - 0.002)
                        elif sample_idx % 4 == 2:
                            _now_answers.append(answer - 0.004)
                        else:
                            _now_answers.append(answer - 0.006)
                    else:
                        _now_ids.append(id)
                        _now_answers.append(answer)

                # Use 0-redistributed data for visualization
                # But use original data for calculating the mean
                data_0_redistributed = pd.DataFrame({'Cell line': _now_ids, 'Bubble area / Cell area': _now_answers})
                data = pd.DataFrame({'Cell line': now_ids, 'Bubble area / Cell area': now_answers})

                # Perform visualization
                savefig_name = args.basedir + "Bubble/" + f"results_{rootDir}_{array_name}"

                fig, ax = plt.subplots(figsize=(30, 20))

                # Set axises
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.yaxis.tick_left()
                ax.xaxis.tick_bottom()
                
                sns.set(style="whitegrid")

                # Plot swarmplot first
                if args.plot_choice == "swarm":
                    swarm = sns.swarmplot(x='Cell line', y='Bubble area / Cell area', data=data_0_redistributed, color="k", size=4, ax=ax, zorder=1)
                elif args.plot_choice == "box":
                    box = sns.boxplot(x='Cell line', y='Bubble area / Cell area', data=data, ax=ax, width=0.5, showfliers=False)
                else:
                    raise NotImplementedError("plot_choice must be in [swarm, box]")
                
                # Calculate mean and standard deviation
                means = data.groupby('Cell line')['Bubble area / Cell area'].mean()
                print("means", means)

                # Calculate standard error values
                sems = data.groupby('Cell line')['Bubble area / Cell area'].apply(sem)

                # Get current x-axis tick locations
                locs, _ = plt.xticks()

                # Plot mean values using matplotlib's scatter, ensuring they are on top layer
                plt.scatter(locs, means, marker='o', color='red', s=30)  # you can change s=100 to adjust the size

                # Add error bars
                plt.errorbar(locs, means, yerr=sems, fmt='none', color='red', capsize=35, elinewidth=2, capthick=2)

                for loc, mean in zip(locs, means):
                    plt.text(loc, mean + 0.03, f'{mean:.4f}', ha='center', va='bottom', color='red', fontsize=25, weight='bold')

                # Set x/y labels
                plt.xlabel('Cell line', fontsize=40)
                plt.ylabel('Bubble area / Cell area', fontsize=40)
                
                # Set character size
                plt.xticks(rotation=45)
                plt.xticks(fontsize=20, rotation=45)
                plt.yticks(fontsize=20)

                # Save images
                plt.tight_layout()
                plt.savefig(savefig_name + f"_mode_{args.mode}_plot_{args.plot_choice}.png")
                plt.close()

            else:
                raise NotImplementedError("mode error!")