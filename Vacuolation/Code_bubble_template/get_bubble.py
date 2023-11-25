import os
import numpy as np
import multiprocessing as mp
from argparse import ArgumentParser
from subprocess import call

class TrainDataGen(object):

    def __init__(self, num_processes, flog=None):
        self.num_processes = num_processes
        self.flog = flog
        
        self.todos = []
        self.processes = []
        self.is_running = False
        self.Q = mp.Queue()

    def __len__(self):
        return len(self.todos)

    def add_one_job(self, input_file, seg_file, output_file, process_id):
        if self.is_running:
            print('ERROR: cannot add a new job while DataGen is running!')
            exit(1)

        todo = (input_file, seg_file, output_file, process_id)
        self.todos.append(todo)
    
    @staticmethod
    def job_func(pid, todos, Q):
        succ_todos = []
        for todo in todos:
            cmd = 'python process.py --input_file \"%s\" --seg_file \"%s\" --output_file \"%s\" --process_id %d' % \
                (todo[0], todo[1], todo[2], todo[3])
            print("cmd", cmd)
            
            ret = call(cmd, shell=True)
            succ_todos.append(ret)
        Q.put(succ_todos)

    def start_all(self):
        if self.is_running:
            print('ERROR: cannot start all while DataGen is running!')
            exit(1)

        np.random.shuffle(self.todos)
        for i in range(self.num_processes):
            todos = [d for d in self.todos if d[3] == i]
            p = mp.Process(target=self.job_func, args=(i, todos, self.Q))
            p.start()
            self.processes.append(p)
        
        self.is_running = True

    def join_all(self):
        if not self.is_running:
            print('ERROR: cannot join all while DataGen is idle!')
            exit(1)

        ret = []
        for p in self.processes:
            ret += self.Q.get()

        for p in self.processes:
            p.join()

        self.todos = []
        self.processes = []
        self.Q = mp.Queue()
        self.is_running = False
        return 

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--basedir', type=str, default="../", help="base directory")
    parser.add_argument('--n_cpu', type=int, default=8, help="number of cpus")
    parser.add_argument('--directory_name', type=str, default="directory_names.txt", help="directory names")
    args = parser.parse_args()
    
    with open(args.directory_name, 'r') as fin:
        config_all = fin.readlines()
        config_all = [config.strip() for config in config_all if config != ""]

    # read file names
    idx = 0
    for rootDir in config_all:
        try:
            print("working on directory:", rootDir)
            input_dir = args.basedir + "Data/" + rootDir + "/"
            segmentation_dir = args.basedir + "Segmentation/" + rootDir + "/"
            output_dir = args.basedir + "Bubble/" + rootDir + "/"

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # get files
            fileprefixname_list = []
            all_files = os.listdir(input_dir)
            all_files.sort()
            for filename in all_files:
                if filename.endswith(('.jpg', '.jpeg', '.png', '.tif')) and "Segmentation" not in filename:
                    file_suffix = filename.split("-")[-1]
                    file_suffix = file_suffix.split("_")[-1]
                    true_name = filename[:-len(file_suffix)]
                    if true_name not in fileprefixname_list:
                        fileprefixname_list.append(true_name)
            fileprefixname_list.sort()

            # run parallel
            datagen = TrainDataGen(args.n_cpu)

            for filename in all_files:
                if filename.endswith(('.jpg', '.jpeg', '.png', '.tif')) and "Segmentation" not in filename:
                    input_file = input_dir + filename
                    seg_file = segmentation_dir + filename[:-4] + ".png"
                    output_file = output_dir + filename

                    datagen.add_one_job(input_file, seg_file, output_file, idx % args.n_cpu)
                    idx += 1
            
            datagen.start_all()
            datagen.join_all()

        except KeyboardInterrupt:
            exit(0)

        except BaseException as e:
            print(rootDir, "Wrong!")
            print(e)