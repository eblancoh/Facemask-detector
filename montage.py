# import the necessary packages
from imutils import build_montages
from imutils import paths
import argparse
import random
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-s", "--sample", type=int, default=400,
	help="# of images to sample")
args = vars(ap.parse_args())

# grab the paths to the images, then randomly select a sample of
# them
imagePaths = list(paths.list_images(args["images"]))
random.shuffle(imagePaths)
imagePaths = imagePaths[:args["sample"]]

# initialize the list of images
images = []
# loop over the list of image paths
for imagePath in imagePaths:
	# load the image and update the list of images
	image = cv2.imread(imagePath)
	images.append(image)

# construct the montages for the images
montages = build_montages(images, (50, 50), (20, 20))

# loop over the montages and display each of them
for montage in montages:
	cv2.imshow("Montage", montage)
	cv2.imwrite('sprite.jpg', montage) 
	cv2.waitKey(0)

# python montage.py --images dataset_sample