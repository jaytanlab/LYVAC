#### Instructions to repeat the molecular dynamics results in the paper

#### Generating the inputs

Please refer to https://charmm-gui.org/?doc=input

We used "Martini Maker" -> "Bilayer builder". "Membrane Only System" is chosen and martini 3.0.0 model is chosen.

We then choose "Number of lipid components". Water thickness all set to 22.5 (default). Default setting is applied to all the others except that 200 mM NaCl is chosen to be consistent with in vitro assays.

This generates the *unedited* inputs.

#### Editing the inputs

We provide the file edit.py. Supposing you download and unzip all your folders from CHARMM-GUI website, and place them under a folder "data", i.e. "data/charmm-gui-xxxxxx". Place the edit.py under "data/edit.py", run "python edit.py" under the "data" folder, and then you will see a series of "charmm-gui-xxxxxx-edited" folder **outside** the "data" folder. These folders should be used in the next step (e.g. zipped and upload).

#### System requirement

We follow the following website for the installation:

https://manual.gromacs.org/current/user-guide/mdrun-performance.html

We performed the experiment under linux with one NVIDIA RTX3090 GPU rent on an online platform. There's no custom need for running the code as long as you have a GPU. GPU is necessary but CPU still seems to be the bottleneck. With 43 core per computer node, our running speed is about 10 minutes per condition (per point). For some reasons, 4 GPUs doens't work for the checking step but 2 works well for installation. 

More concretely, we install GROMACS using the following command lines.

```
wget https://ftp.gromacs.org/gromacs/gromacs-2024.2.tar.gz
tar xfz gromacs-2024.2.tar.gz
pip install cmake # update to newer versions
# restart your anaconda by re-open a new terminal
cd gromacs-2024.2
mkdir build
cd build
# to build with CUDA support, add -DGMX_GPU=CUDA
cmake .. -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON -DCMAKE_INSTALL_PREFIX=/hy-tmp/gromacs -DGMX_GPU=CUDA
make -j
make check -j
sudo make install
source /hy-tmp/gromacs/bin/GMXRC # add this to .bashrc to keep it
# we download the data to Windows and found that we have to run this command so that the data format can be recognized under linux
ls | grep 'charmm-gui-' | sed -n 's/charmm-gui-\([0-9]*\)-edited/\1/p'
```

#### Performing the molecular dynamics

Step 1: generate the run.sh to run the code

```
# You need to create a file "folders.txt", with each line a directory id. Please see the example shown
# before running the following command, change the folder in the code accordingly (our example data is uploaded to this folder on the server: /hy-tmp/20250430-edited)
python make_sh.py
# then, you should see a script generated: run.sh
chmod +x ./run.sh
# an example run.sh is given

# the following code takes very long. Using a background running platform (e.g. tmux) is highly recommended.
./run.sh
# Please check your GPU and CPU usage. We observe 40% GPU and full CPU usage.
```

Step 2: change the small code and run things again to get the energy terms of lipid only

```
python add_one_line.py
# before running the following command, change the folder in the code accordingly (our example data is uploaded to this folder on the server: /hy-tmp/20250430-edited)
python make_sh_export.py
chmod +x ./export.sh
./export.sh
# you will see energy_Lipid_LJ.txt and energy_Lipid_Coul.txt in each separate folders
python export_summarize.py
# You will see outputs in the terminal
```

If you see no output for some of the runs, check the separate folder and see whether there is a .gro file generated for step7_production. If not, the run has failed.

If you see significant outliers, you need to double check your inputs.

#### Checking the recorded output we have

Please see "Lipid simulation - final.docx"

#### Generating the visualization plots from the output

Please run each code in the folder "code to run on server"

#### Full source data and all intermediate results

The source data, both the input or the output, are too large (>100GB) to be shared across databases we could find. To ensure reproducibility, we saved all the inputs and outputs in hard drives.

Upon request, we will share a minimal input data to be used (from our last run). Using this, you should be able to reproduce the pipeline of the code we're running.

To repeat specific parts in the paper, we will share the input data independently (smaller) and share the output data through online drives allowing for temporary storage or use physical shipping, depending on the download speed of the receiver.