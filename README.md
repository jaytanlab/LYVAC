# LYVAC

Source code, minimal datasets, and the tutorial on how to run the code for the LYVAC manuscript.

#### Instructions: Run the Demo

For the following sections (sub-folders), we provide instructions to run on data, expected output, and expected run time for a demo on a "normal" desktop computer. Please go into separate sub-folders and see the details there. We're also trying our best to provide reproduction instructions.

**Please read the README file in each sub-folder to get an overview before running the program.**

**Folder 1**: Vacuolation quantification

**Folder 2**: Protein colocalization quantification

Note: this folder includes the files to quantify single/double channel signal intensity

**Folder 3**: Cell death quantification

**Folder 4**: Molecular_Dynamics

#### System requirements

Our program uses Python (used for all quantization) and C++ (only for vacuolation quantization) for quantization. Python and C++ have corresponding versions under commonly used operating systems, but you need to install the corresponding environment correctly. All experiments are performed (and the runtime is reported based on) a Windows laptop with an 8-core CPU and 16 GB of memory, except for the molecular dynamics, where the code is run on a linux server with 2x43 CPUs cores and 2x 3090.

**Python installation**
For Windows, Linux, and macOS platforms, we do not recommend that you download a separate program to install Python on the Internet. We recommend that you install Python through the Anaconda installation environment as described in the following section, which can automatically install the required dependency files and ensure compatibility with multiple operating systems.

**C++ installation**
For the Windows platform, we use Dev-C++ to compile the program (version: 5.11). For Unix platforms (Linux/MacOS), the operating system has its own C++ compiler when installed. If not, we recommend that you follow the tutorials on the Internet according to your operating system and install the "g++" software.

**A note on running your program on Unix**

Our program compiles and runs normally under Windows. If you want to run the program under Linux or macOS, especially the parts involving C++, we recommend that you contact the author team and ask for help (see the last section). The authors can guide you in debugging for your platform.

#### Installation guide

If you have Python on your computer, feel free to skip sections 1 and 2 (we **strongly recommend** an installation in a clean environment through Anaconda with the installation order of Python (3.8) and cellpose we provide, as installing cellpose in an existing environment can cause failures. See debug [here](https://cellpose.readthedocs.io/en/latest/installation.html#dependencies).)

1. Install [Anaconda](https://www.anaconda.com/download#Downloads): Please follow the instructions on the official website. It's just a download through one click. If you are asked about Anaconda-related settings, choose the default settings, unless you are asked if you want Anaconda to be added to environment variables or started with the terminal, in which case you should choose "Yes".

Anaconda will help you organize the Python environments in different projects and find the dependencies needed to install software (e.g., Python). It is cross-platform.

The following commands are run in terminals. If you want to reproduce the code but don't know what terminals are, we suggest you search for "What is a terminal" and "How can I open a terminal in Windows/Linux/MacOS" or contact us.

2. Install Python3 with Anaconda (there should be a default "base" environment, but a separate environment is recommended):

```
(In terminal)
conda create -n LYVAC python=3.8
conda activate LYVAC
```


3. Install the Cellpose (If you want to quantify the vacuolation). Notice that Cellpose does not need GPUs to run (We ran it on a CPU), but if you have an available GPU, it will make the program much faster.

```
(In terminal)
pip install cellpose
# Note that this will automatically install torch 2.x
```

4. Install other dependencies

```
pip install opencv-python scikit-image pandas seaborn
```

Note: The installed version is 2.2, but we only used the functions existing in Cellpose 1.0, so we cite the software version and the paper as the authors stated [here](https://github.com/MouseLand/cellpose#citation).

The typical installation may take you less than 1 h to finish if you are familiar with the system. However, it may be confusing and take you 1 week if you are not familiar with the Python environment or encounter problems. Please pose an issue on GitHub or reach out in this case. 

#### Code Reproducibility and Contact Information

We have uploaded the minimum data set that can ensure the program runs as part of the reproduction instructions. All source data can be acquired upon reasonable request. For the acquisition of quantitative data in all papers, we retained all procedures and the intermediate results of their runs. Fixed random seeds are set up for all random sampling links to ensure that the results of each run of the program are the same.

If you want to modify the program based on the code reproduction results, we have added English comments to the code as many as possible to help you, but we still recommend that you contact us before modifying: we are here to help. Please contact the author, Shawn Haoxiang Yang (yanghaoxiang7@gmail.com), and cc the corresponding author, Jay Xiaojun Tan (jay.tan@pitt.edu). We will try to respond within 24 hours during workdays.
