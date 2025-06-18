#### Instructions to run on data

The program that you can have a try to quantify the vacuoles is listed in **Code_bubble** directory.

```
# Please make sure that your terminal is in the "Code_bubble" directory
cd Code_bubble

# compile the C++ file "process.cpp" and get an output
# you need to do this step according to your computer system (Windows/Linux/MacOS).
# on Windows, we expect that you get an "process.exe"
# a compiled C++ exe is provided. please try if it can work

# run the program
python get_segmentation.py
python get_bubble.py
python get_quantification.py
```

This is mini-dataset sample from vacuoles experiment of WT/LYVAC-KO1/LYVAC-KO2 with or without Apilimod.

#### Expected output

```
Example outputs are already placed at the correct position; rerunning the program will overwrite the results.
1. You'll get segmentation results in the segmentation output folder
2. You'll get vacuole detection results in the bubble output folder
2. You'll get an excel form summarizing the data and also output in the terminal
```

**The output folder should contain intermediate results** about the quantified cells and for each cell quantified, it should show all the bubbles detected.

Note that there will be a "tmp" temporary folder in your "Code_bubble" directory. It's huge (<1.5GB) but you can remove it after the run.

#### Expected run time

Expected run time for demo on a "normal" desktop computer should be less than 30 minutes. The program may need some time to initiate (~2min), and that's normal. Then, the segmentation of each image file may take you about 10-30 seconds by CPU. The vacuole detection costs around 5 minutes in total. The program is run in parellel, so the number of CPU cores on your computer can affect the speed, and that's normal too. If longer time or an error is encountered, please contact the authors as stated in the major readme file.

#### How to run the software on your data

You may want to adapt this program to **quantify the single channel protein intensity or the colocalization of two channels** on your data. You need to take care of the following items when you pursue it:

* Place your input files in the correct input folder with the correct name. Pay special attention to whether the file name is similar to our file naming method: our program separates different experiment groups and several pictures in this group by identifying "_" and "-" in the file ("_0.png"); Our program may only recognize jpg or png, you need to obtain the correct image format or modify the corresponding code Adjust the appropriate threshold and manually check whether the results are consistent.
* Before running the program, you need to manually label the cells. We tried Cellpose, but it's not perfect in detecting cells in immunofluorescence images without further training data :)
* After running the program, all detected cells and the quantified area of all channels will be saved in the output folder. You need to check that the detected cells and the independent channels are roughly what you expected. We set a threshold to distinguish which area are "puncta" and which are not; if a large number of background is detected, it may be because your threshold setting is too low; if a lot of signals are not detected, it may be because your threshold setting is set too high. We recommend that you check the results carefully.

Since you may want to modify the program, we have added English comments to the code as much as possible to facilitate your modification, but we still recommend that you contact us before modifying, we can provide a better code explanation and help for you. Please contact the author Haoxiang Yang (yanghaoxiang7@gmail.com) and copy the corresponding author Jay Xiaojun Tan (jay.tan@pitt.edu).

##### Segmentation resolution down-sampling trick

The segmentation does not affect the overall quantification. However, we found our default segmentation deep learning program slow (in Code_bubble_template, about 1-2 minute per image). We have used a resolution down-sampling trick in Code_bubble folder and in the latter part of the data: the program runs faster if the image resolution is appropriately reduced during the segmentation.

#### Reproduction instructions

Based on the nature of the article currently under review, we have uploaded the minimum data set that can ensure the program runs as a part of reproduction instructions. All source data can be acquired upon reasonable request. For the acquisition of quantitative data in all papers, we retained all procedures and the intermediate results of their runs. Fixed random seeds are set up for all random sampling links to ensure that the results of each run of the program are the same.

The source code in **Code_bubble_template** is copied as a parent folder from where we edit the program and run it to get the results. You need to make the following specific adaptations to further reproduce the results from the code. Note that we made the segmenration trick in **Code_bubble** so it's not exactly the same as **Code_bubble_template**.

We call the current version "template". It has the following parameter settings:

```
In get_segmentation.py:
  segmentation with original size, diameter = 120, image n_split = 5
  resize = (512, 512), diameter = 15, image n_split = 4
In process.cpp:
  tail <= 5000 (only cells with size >= 5000 is kept for quantification)
  int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 30;
```

We set proper thresholds to let the program correctly detect the cells and vacuole area. For the following folder, you need to change the corresponding setting to reproduce exactly the same results in the work. 

Please note that these changes are due to slightly different imaging conditions across all samples (detectable through our presented panels - they have not undergone brightness and contrast adjustments).

```
For the following folders:
vacuoles in VPS13C
vacuoles in 293T

Change in process.cpp: No changes needed
```

```
For the following folders:
vacuoles in metoclopramide

Change in process.cpp:
int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 45;
```

```
For the following folders:
vacuoles in PIKFyve
vacuoles in Fig4

Change in process.cpp:
int percentile_value = get_percentile(tmp, tmpcnt, 45, true) + 25;
plus: circularity is changed from 0.6 to 0.95
plus: the Touch_boundary of "if (tail >= 5000)" changed from 1 to 15
```

```
For the following folders:
vacuoles in LYVACKO_Rescue
vacuoles in 2A
vacuoles in OSBP

Change in process.cpp:
int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 25;
plus: tail <= 10000
```

```
For the following folders:
vacuoles in b2b BJ (besides, circularity is changed from 0.6 to 0.8 because cell segmentation is not good.)
vacuoles in COS7 1080

Change in process.py and process.cpp:
with segmentation resize = (512, 512), diameter = 35, image n_split = 1:
plus:int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 45/55;
```

```
For the following folders:
vacuoles in LYVACKO Rescue
vacuoles in OSBPKO Rescue

Change in process.py and process.cpp:
with segmentation resize = (512, 512), diameter = 35, image n_split = 1
plus: int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 65;
plus: tail <= 10000
```

```
For the following folders:
vacuoles in OSBPKO Rescue With ORP1

Change in process.py and process.cpp:
with segmentation resize = (512, 512), diameter = 35, image n_split = 1
plus: int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 35;
plus: tail <= 10000
```

```
For the following folders:
vacuoles in Hypotonic

Change in process.py and process.cpp:
with segmentation resize = (512, 512), diameter = 25, image n_split = 1
plus: int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 55;
```

```
For the following folders:
vacuoles in LYVAC_Mutants
vacuoles in water channel blocker
vacuoles in metoclopramide

Change in process.py and process.cpp:
with segmentation resize = (512, 512), diameter = 35, image n_split = 1
plus: int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 55;
plus: tail <= 10000
```

```
For the following folders:
vacuoles in SMP Mutants

Change in process.py and process.cpp:
with segmentation resize = (512, 512), diameter = 35, image n_split = 1
plus: int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 75;
plus: tail <= 8000
```

```
For the following folders:
vacuoles in WT+probe

Change in process.py and process.cpp:
with segmentation resize = (512, 512), diameter = 35, image n_split = 1
plus: int percentile_value = get_percentile(tmp, tmpcnt, 65, true) + 55;
plus: tail <= 8000
```

```
For the following folders:
vacuoles in WT+probe

Change in process.py and process.cpp:
with segmentation resize = (512, 512), diameter = 45, image n_split = 1
plus int percentile_value = get_percentile(tmp, tmpcnt, 75, true) + 90;
plus size >= 10000, tail2 <= 150
```

