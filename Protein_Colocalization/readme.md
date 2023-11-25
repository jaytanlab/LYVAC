#### Instructions to run on data

The program that you can have a try to quantify the cell death is listed in **Code_sample** directory.

```
# Please make sure that your terminal is in the "Code_sample" directory
cd Code_sample

# run the program

# for colocalization, this one is used very often in the work; please do try this
python process.py --mode coloc_total

# for single channel intensity calculation, used less often
python process.py --mode single_total
```

This is mini-dataset sample from "LYVAC recruitment to LAMP1 with Apilimod under different time points".

#### Expected output

```
Example outputs are already placed at the correct position; rerunning the program will overwrite the results.
1. You'll get an output folder.
2. You'll get an excel form summarizing the data
```

**The output folder should contain intermediate results** about the quantified cells and for each cell quantified, and it should show the area of each channel that has been quantified (that you're interested in).

In the output excel, each row is a piece of data (an image).

#### Expected run time

Expected run time for demo on a "normal" desktop computer should be less than 5 minutes. Each image file may take you about 5-10 seconds. If longer time or an error is encountered, please contact the authors as stated in the major readme file.

#### How to run the software on your data

You may want to adapt this program to **quantify the single channel protein intensity or the colocalization of two channels** on your data. You need to take care of the following items when you pursue it:

* Place your input files in the correct input folder with the correct name. Pay special attention to whether the file name is similar to our file naming method: our program separates different experiment groups and several pictures in this group by identifying "_" and "-" in the file ("_0.png"); Our program may only recognize jpg or png or tif, you need to obtain the correct image format or modify the corresponding code Adjust the appropriate threshold and manually check whether the results are consistent.
* Before running the program, you need to manually label the cells. See "painted" folder in the "Code_sample" folder as an example. We tried Cellpose, but it's not perfect in detecting cells in immunofluorescence images without further training data :)
* After running the program, all detected cells and the quantified area of all channels will be saved in the output folder. You need to check that the detected cells and the independent channels are roughly what you expected. We set a threshold to distinguish which area are "puncta" and which are not; if a large number of background is detected, it may be because your threshold setting is too low; if a lot of signals are not detected, it may be because your threshold setting is set too high. We recommend that you check the results carefully.

Since you may want to modify the program, we have added English comments to the code as much as possible to facilitate your modification, but we still recommend that you contact us before modifying, we can provide a better code explanation and help for you. Please contact the author Haoxiang Yang (yanghaoxiang7@gmail.com) and copy the corresponding author Jay Xiaojun Tan (jay.tan@pitt.edu).

#### Reproduction instructions

The source code in **Code_full_list** is directly copied from the folder where we run the program to get the results. No specific adaptation is needed to further reproduce it except that you need the source data.

Based on the nature of the article currently under review, we have uploaded the minimum data set that can ensure the program runs as a part of reproduction instructions. All source data can be acquired upon reasonable request. For the acquisition of quantitative data in all papers, we retained all procedures and the intermediate results of their runs. Fixed random seeds are set up for all random sampling links to ensure that the results of each run of the program are the same.