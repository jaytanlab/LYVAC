import os
import random
import numpy as np

from argparse import ArgumentParser

# get function name
def get_name(my_array):
    return [k for k, v in globals().items() if v is my_array][0]

if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument('--basedir', type=str, default="../", help="base directory")
    parser.add_argument('--directory_name', type=str, default="directory_names.txt", help="directory names")
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

        # Dump data
        for array_name in ["total_area"]:
            now_ids, now_answers = [], []
            for id, answer in zip(ids, answers):
                
                if array_name in ["each_area"]:
                    now_arr = [item for cell in answer[array_name] for item in cell]
                else:
                    now_arr = answer[array_name]

                now_ids += [id for i in range(len(now_arr))]
                now_answers += now_arr

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
            