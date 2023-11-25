#### Instructions to run on data

The program that you can have a try to quantify the cell death is listed in **Code_sample** directory.

```
# Please make sure that your terminal is in the "Code_sample" directory
cd Code_sample

# run the program
python process.py
```

This is mini-dataset sample from cell death experiment of sunitinib.

#### Expected output

```
Example outputs are already placed at the correct position; rerunning the program will overwrite the results.
1. You'll get an output folder
2. You'll get an excel form summarizing the data 
```

**The output folder should contain intermediate results** about the quantified cells and for each cell quantified, it should show all the cells that has been quantified in yellow.

In the output excel, each column is a group of sample; each row is a piece of data (an image).

#### Expected run time

Expected run time for demo on a "normal" desktop computer should be less than 2 minutes. If longer time or an error is encountered, please contact the authors as stated in the major readme file.

#### How to run the software on your data

You may want to adapt this program to **quantify the cell viability through DAPI staining** on your data. You need to take care of the following items when you pursue it:

* Place your input files in the correct input folder with the correct name. Pay special attention to whether the file name is similar to our file naming method: our program separates different experiment groups and several pictures in this group by identifying "_" and "-" in the file ("_0.png"); Our program may only recognize jpg or png, you need to obtain the correct image format or modify the corresponding code Adjust the appropriate threshold and manually check whether the results are consistent.
* After running the program, all detected cells will be saved in the output folder, indicated in yellow. You need to check that the detected cells and their numbers are roughly what you expected. We set a threshold to distinguish which cells are cells and which are not; if a large number of connected blocks are detected, it may be because your threshold setting is too low; if a large number of cells are not detected, it may be because your threshold setting is set too high. Although we have taken some image cropping methods to try to minimize variances in background staining (which is particularly noticeable under the 4x microscope), we still recommend that you check the results carefully.

Since you may want to modify the program, we have added English comments to the code as much as possible to facilitate your modification, but we still recommend that you contact us before modifying, we can provide a better code explanation and help for you. Please contact the author Haoxiang Yang (yanghaoxiang7@gmail.com) and copy the corresponding author Jay Xiaojun Tan (jay.tan@pitt.edu).

#### Reproduction instructions

The source code in **Code_full_list** is directly copied from the folder where we run the program to get the results. No specific adaptation is needed to further reproduce it except that you need the source data.

Based on the nature of the article currently under review, we have uploaded the minimum data set that can ensure the program runs as a part of reproduction instructions. All source data can be acquired upon reasonable request. For the acquisition of quantitative data in all papers, we retained all procedures and the intermediate results of their runs. Fixed random seeds are set up for all random sampling links to ensure that the results of each run of the program are the same.