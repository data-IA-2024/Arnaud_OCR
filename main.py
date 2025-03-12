from backend.script.utils import open_image
from backend.script.segmentation import rgb_to_gray, extract_blocks
import cv2

image_path = "./../../data/2018/FAC_2018_0004-759.png"
image = open_image(image_path)

gray = rgb_to_gray(image)
blocks = extract_blocks(gray)

for block_name, block in blocks.items():
    cv2.imwrite(block_name+".png", block)