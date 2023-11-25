import os
import cv2
import copy
import numpy as np

from skimage import io
from argparse import ArgumentParser

def Makedirs(d):
    if not os.path.exists(d):
        os.makedirs(d)

DEBUG = False

def GetAnswer(input_file, seg_file, output_file, process_id):
    Makedirs(f"./tmp/tmp_{process_id}")
    
    if DEBUG: print("Transfering images forward")
    img_in_1 = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE)

    sz_x, sz_y = img_in_1.shape
    sz_min = min(sz_x, sz_y)
    dx, dy = (sz_x - sz_min) // 2, (sz_y - sz_min) // 2
    img_in_1 = img_in_1[dx:sz_x - dx, dy:sz_y - dy]

    img_in_2 = cv2.imread(seg_file)

    sz_x, sz_y, _ = img_in_2.shape
    sz_min = min(sz_x, sz_y)
    dx, dy = (sz_x - sz_min) // 2, (sz_y - sz_min) // 2
    img_in_2 = img_in_2[dx:sz_x - dx, dy:sz_y - dy]

    img_in_1 = cv2.resize(img_in_1, (3024, 3024))
    img_in_2 = cv2.resize(img_in_2, (3024, 3024))

    img_in_1_copy = copy.deepcopy(img_in_1)
    
    # apply blur
    for _ in range(3):
        img_in_1 = cv2.GaussianBlur(img_in_1, (5, 5), 0)
    
    np.savetxt(f"./tmp/tmp_{process_id}/in_1.txt", img_in_1[:, :], fmt="%d")
    
    # Process the black background
    valid = img_in_2[:, :, 0] + img_in_2[:, :, 1] + img_in_2[:, :, 2] > 10
    valid = valid.reshape(valid.shape[0], valid.shape[1], 1).repeat(3, axis=-1)
    seg = np.where(valid, img_in_2, np.zeros_like(img_in_2))

    # Input to the model
    # 900 is just a large constant
    seg = seg[:, :, 0] * 900 * 900 \
        + seg[:, :, 1] * 900 \
        + seg[:, :, 2]
    np.savetxt(f"./tmp/tmp_{process_id}/in_2.txt", seg, fmt="%d")
    
    if DEBUG: print("Calling C++")
    # os.system(f"process {process_id} > /dev/null 2>&1")
    os.system(f"process.exe {process_id}")

    if DEBUG: print("Transfering images backward")
    
    img_out_1_r = np.loadtxt(f"./tmp/tmp_{process_id}/out_r.txt", dtype=np.uint8)
    img_out_1_g = np.loadtxt(f"./tmp/tmp_{process_id}/out_g.txt", dtype=np.uint8)
    img_out_1_b = np.loadtxt(f"./tmp/tmp_{process_id}/out_b.txt", dtype=np.uint8)
    img_out_1 = np.stack([img_out_1_r, img_out_1_g, img_out_1_b], axis=-1)

    n_bubble = 0
    with open(f"./tmp/tmp_{process_id}/result.txt", "r") as fin:
        file_answer = fin.readlines()
        line_no = 0
        while line_no < len(file_answer):
            n, cell_area = file_answer[line_no].strip().split(" ")
            n = int(n)
            n_bubble += n
            line_no += n + 1
    
    file_suffix = output_file.split(".")[-1]
    true_name = output_file[:-len(file_suffix)-1]
    
    io.imsave(true_name + "_in.png", img_in_1_copy)
    io.imsave(true_name + "_seg.png", img_in_2)
    io.imsave(true_name + "_out.png", img_out_1)

    print(f"***[Result] input_file {input_file} n_bubble {n_bubble}")

    os.system(f"copy \".\\tmp\\tmp_{process_id}\\result.txt\" \"{true_name}.txt\"")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input_file', type=str, help='input image path')
    parser.add_argument('--seg_file', type=str, help='segmentation image path')
    parser.add_argument('--output_file', type=str, help='output image path')
    parser.add_argument('--process_id', type=int, help='id of this process')
    
    args = parser.parse_args()
    
    GetAnswer(args.input_file, args.seg_file, args.output_file, args.process_id)
