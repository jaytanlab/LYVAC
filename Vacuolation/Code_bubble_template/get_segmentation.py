import os
import cv2
import colorsys
import numpy as np
from cellpose import plot, models

from argparse import ArgumentParser

def count_black_pixels(subimage):
    black_threshold = 5
    return np.sum(np.sum(subimage, axis=-1) < black_threshold)

def split_image(image, num_splits):
    n, m = image.shape
    sub_n, sub_m = n // num_splits, m // num_splits

    subimages = np.zeros((num_splits, num_splits, sub_n, sub_m), dtype=image.dtype)
    discarded = np.zeros((num_splits, num_splits), dtype=bool)

    for i in range(num_splits):
        for j in range(num_splits):
            subimage = image[i*sub_n:(i+1)*sub_n, j*sub_m:(j+1)*sub_m]
            black_pixels = count_black_pixels(subimage)
            
            if black_pixels > 100:
                discarded[i, j] = True
            else:
                subimages[i, j] = subimage

    return subimages, discarded

def merge_subimages(subimages, discarded):
    num_splits, _, sub_n, sub_m, _ = subimages.shape

    merged_image = np.zeros((num_splits*sub_n, num_splits*sub_m, 3), dtype=subimages.dtype)

    for i in range(num_splits):
        for j in range(num_splits):
            if not discarded[i, j]:
                merged_image[i*sub_n:(i+1)*sub_n, j*sub_m:(j+1)*sub_m, :] = subimages[i, j]

    return merged_image

def transfer(img):
    img0 = img.copy()

    if img0.shape[0] < 4:
        img0 = np.transpose(img0, (1,2,0))
    if img0.shape[-1] < 3 or img0.ndim < 3:
        img0 = plot.image_to_rgb(img0, channels=[0, 0])
    else:
        if img0.max()<=50.0:
            img0 = np.uint8(np.clip(img0*255, 0, 1))
    return img0

def rgb_to_hsv(arr):
    rgb_to_hsv_channels = np.vectorize(colorsys.rgb_to_hsv)
    r, g, b = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv_channels(r, g, b)
    hsv = np.stack((h,s,v), axis=-1)
    return hsv

def hsv_to_rgb(arr):
    hsv_to_rgb_channels = np.vectorize(colorsys.hsv_to_rgb)
    h, s, v = np.rollaxis(arr, axis=-1)
    r, g, b = hsv_to_rgb_channels(h, s, v)
    rgb = np.stack((r,g,b), axis=-1)
    return rgb

def mask_overlay(img, masks, colors=None):
    if colors is not None:
        if colors.max()>1:
            colors = np.float32(colors)
            colors /= 255
        colors = rgb_to_hsv(colors)
    if img.ndim>2:
        img = img.astype(np.float32).mean(axis=-1)
    else:
        img = img.astype(np.float32)
    
    HSV = np.zeros((img.shape[0], img.shape[1], 3), np.float32)
    # HSV[:,:,2] = np.clip((img / 255. if img.max() > 1 else img) * 1.5, 0, 1)
    HSV[:,:,2] = -1.0
    hues = np.linspace(0, 1, masks.max()+1)[np.random.permutation(masks.max())]
    for n in range(int(masks.max())):
        ipix = (masks==n+1).nonzero()
        if colors is None:
            HSV[ipix[0],ipix[1],0] = hues[n]
        else:
            HSV[ipix[0],ipix[1],0] = colors[n,0]
        HSV[ipix[0],ipix[1],1] = 1.0
    RGB = (hsv_to_rgb(HSV) * 255).astype(np.uint8)
    return RGB

def Segment(model, input_filename, output_filename, num_splits=5):
    image_input = cv2.imread(input_filename)
    image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)
    # remember_shape = (image_input.shape[1], image_input.shape[0])
    # image_input = cv2.resize(image_input, (512, 512))
    images, discarded = split_image(image_input, num_splits)

    diameter = 120  # defalt None
    flow_threshold = 0.9 # default 0.4
    cellprob_threshold = -1
    # not using nucleus
    channels = [0, 0]
    
    n, m = image_input.shape
    sub_n, sub_m = n // num_splits, m // num_splits
    segmentation = np.zeros((num_splits, num_splits, sub_n, sub_m, 3), dtype=image_input.dtype)

    for i in range(images.shape[0]):
        for j in range(images.shape[1]):
            if discarded[i][j] == True: continue

            image = images[i][j]
            masks, flows, styles, diams = model.eval(
                image, diameter=diameter, flow_threshold=flow_threshold, cellprob_threshold=cellprob_threshold, channels=channels)

            image0 = transfer(image)
            # outlines = utils.masks_to_outlines(maski)

            # seg = plot.mask_overlay(np.zeros_like(image, dtype=np.uint8), masks)
            seg = mask_overlay(image0, masks)
            segmentation[i][j] = seg

    image_output = merge_subimages(segmentation, discarded)
    # image_output = cv2.resize(image_output, remember_shape)
    cv2.imwrite(output_filename, image_output)
    length = len(output_filename.split(".")[-1])
    realname = output_filename[:-length-1]
    new_n, new_m = image_output.shape[:2]
    image_overlap = cv2.resize(image_input, (new_m, new_n)) * 0.8
    image_overlap = np.repeat(image_overlap.reshape(new_n, new_m, 1), 3, axis=-1)
    image_overlap = image_overlap + image_output * 0.2
    cv2.imwrite(realname + "_overlap." + output_filename[-length:], image_overlap)

if __name__ == "__main__":
    model = models.Cellpose(gpu=True, model_type="cyto2")
    print("model loaded")

    parser = ArgumentParser()
    parser.add_argument('--basedir', type=str, default="../", help="base directory")
    parser.add_argument('--directory_names', type=str, default="directory_names.txt")
    args = parser.parse_args()

    with open(args.directory_names, 'r') as fin:
        config_all = fin.readlines()
        config_all = [config.strip() for config in config_all if config != ""]

    # read file names
    for rootDir in config_all:
        print("working on directory:", rootDir)

        input_dir = args.basedir + "Data/" + rootDir + "/"
        output_dir = args.basedir + "Segmentation/" + rootDir + "/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        all_files = os.listdir(input_dir)
        all_files.sort()

        for idx, filename in enumerate(all_files):
            
            print(f"[{idx} / {len(all_files)}]", filename)
            try:
                Segment(model, input_dir + filename, output_dir + filename[:-4] + ".png")
            except KeyboardInterrupt:
                exit(0)
            except BaseException as e:
                print(input_dir, filename, "Wrong!")
                print(e)

