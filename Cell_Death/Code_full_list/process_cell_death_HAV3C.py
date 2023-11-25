# python process.py --mode single_total

import os
import cv2
import csv
import copy
import numpy as np
from argparse import ArgumentParser

# Set color random seed
np.random.seed(2023)

# Red 2, Green 1, Blue 0
# Set input arguments
parser = ArgumentParser()
parser.add_argument('--first_channel', type=int, default=0)
args = parser.parse_args()

rootDir = "./"

# Set directory
original_image_dir = os.path.join(rootDir, 'original')
output_dir = os.path.join(rootDir, "result")

# Create output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get files
fileprefixname_list = []
all_files = os.listdir(original_image_dir)
all_files.sort()
for filename in all_files:
    if filename.endswith(('.jpg')):
        file_suffix = filename.split("_")[-1]
        true_name = filename[:-len(file_suffix)]
        if true_name not in fileprefixname_list:
            fileprefixname_list.append(true_name)
fileprefixname_list.sort()

full_cell_number = {}
max_concen = {}
results = {}
max_len = 0
for fileprefixname in fileprefixname_list:

    print("fileprefixname", fileprefixname)

    cell_numbers = []
    for filename in all_files:
        if not filename.startswith(fileprefixname): continue

        # Load the painted image and the original image
        original_read = os.path.join(original_image_dir, filename)

        original_read = cv2.imread(original_read)
        
        total_x, total_y = 9, 9
        length_x, length_y = original_read.shape[0] // total_x, original_read.shape[1] // total_y
        
        final_answer_original = np.zeros_like(original_read)
        final_answer_edited = np.zeros_like(original_read)
        
        valid_cell_num = 0
        for i_x in range(0, total_x):
            for i_y in range(0, total_y):
                # if i_x >= total_x - 2 and i_y <= 2: continue
                i_num = i_x * total_y + i_y
                original = original_read[i_x * length_x: (i_x + 1) * length_x, i_y * length_y: (i_y + 1) * length_y]
                original_copy = copy.deepcopy(original)

                original_background = np.percentile(original[:, :, args.first_channel], 20)
                original = np.uint8(np.maximum(0, np.float32(original) - original_background))
                
                # adjust brightness according to data setting
                percentile = np.percentile(original[:, :, args.first_channel], 70) + 15
                
                # Threshold the red channel of the painted image to get the cells
                _, thresholded = cv2.threshold(original[:, :, args.first_channel], percentile, 255, cv2.THRESH_BINARY)
                
                # Find the contours (i.e., the cells) in the thresholded image
                contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Filter out small / large contours
                contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 30 and cv2.contourArea(cnt) < 2000]

                valid_mask_first_channel = np.zeros_like(original)

                used_contours = []
                # save cross channel used
                for contour in contours:
                    # Create a mask of the cell
                    mask = np.zeros_like(original)
                    cv2.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)

                    # Use the mask to get the cell's pixels in the original image
                    cell_pixels = cv2.bitwise_and(original, mask)
                    first_channel = cell_pixels[:, :, args.first_channel]

                    # Calculate the area with too bright signal
                    area_bright = np.float32(first_channel > 250).sum()
                    if area_bright > 25:
                        continue

                    valid_cell_num += 1
                    used_contours.append(contour)
                
                # Create an image to visualize the detected contours
                original_coutours_original = cv2.drawContours(original_copy, used_contours, -1, (0, 255, 255), 2)
                original_coutours_edited = original # cv2.drawContours(original, used_contours, -1, (0, 255, 255), 2)

                final_answer_original[i_x * length_x: (i_x + 1) * length_x, i_y * length_y: (i_y + 1) * length_y] = original_coutours_original
                final_answer_edited[i_x * length_x: (i_x + 1) * length_x, i_y * length_y: (i_y + 1) * length_y] = original_coutours_edited


        cv2.imwrite(os.path.join(output_dir, filename[:-4] + f"_coutours_original.png"), final_answer_original)
        cv2.imwrite(os.path.join(output_dir, filename[:-4] + f"_coutours_edited.png"), final_answer_edited)

        cell_numbers.append(valid_cell_num)
        print(f"Frame {filename}: valid_cell_num {valid_cell_num}")

    # Print the basic numbers
    print("Mean", np.mean(cell_numbers))

    # extract filename and concentration number
    name_first_split = fileprefixname.split(" ")[-1]
    name_first_split = fileprefixname[:-len(name_first_split)]
    print("name_first_split", name_first_split)
    
    # Save the data of the current prefix
    if "control" in fileprefixname:
        full_cell_number[name_first_split] = np.mean(cell_numbers)
        
    max_len = max(max_len, len(cell_numbers))
    results[fileprefixname] = cell_numbers

lines = ["" for _ in range(max_len+1)]
for fileprefixname, cell_numbers in results.items():
    
    name_first_split = fileprefixname.split(" ")[-1]
    name_first_split = fileprefixname[:-len(name_first_split)]
        
    full_cell = full_cell_number[name_first_split]
    lines[0] += f"{fileprefixname},"
    for idx in range(max_len):
        if idx < len(cell_numbers):
            lines[idx+1] += f"{cell_numbers[idx]/full_cell},"
        else:
            lines[idx+1] += f","

with open(f"output.csv", "w") as fout:
    for line in lines:
        fout.write(line + "\n")

