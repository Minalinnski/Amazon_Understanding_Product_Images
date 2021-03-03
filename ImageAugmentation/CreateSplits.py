from PIL import Image
import cv2
import os
import re
import numpy as np
import pandas as pd
import random

def create_datasets(dataset_path, numsame=500, numdif=500):

	randDF = pd.DataFrame(columns=['image1', 'image2', 'label'])

	for i in range(numsame):
		folder = random.choice(os.listdir(dataset_path))
		while not os.path.isdir(os.path.join(dataset_path, folder)):
			folder = random.choice(os.listdir(dataset_path))
		folder = os.path.join(dataset_path, folder) # Folder = Number, e.g. 4
		subfolder = random.choice(os.listdir(folder)) # Subfolder = product, e.g. A0123456789
		count = 10
		while len(os.listdir(os.path.join(folder, subfolder))) == 1 and count != 0:
			subfolder = random.choice(os.listdir(folder)) # We want more than one picture for this product

			count = count - 1

		if count == 0:
			continue

		image = random.choice(os.listdir(os.path.join(folder, subfolder)))
		product_id = image[0:-4]

		sameimage = str(product_id[0:10]) + '_' + str(random.randint(0, 10)) + '.jpg'

		count = 10
		while not os.path.exists(os.path.join(os.path.join(folder, subfolder), sameimage)) and count != 0:
			sameimage = str(product_id[0:10]) + '_' + str(random.randint(0, 10)) + '.jpg'
			
			count = count - 1


		if count == 0:
			continue

		image = os.path.join(folder, os.path.join(subfolder, image))
		sameimage = os.path.join(folder, os.path.join(subfolder, sameimage))
		im1 = np.asarray(Image.open(image))
		im2 = np.asarray(Image.open(sameimage))

		try:
			if im1.shape[2] != 3 or im2.shape[2] !=3:
				print(":(")
				continue

		except:
			continue

		label = {'image1': image, 'image2': sameimage, 'label': "same"}
		randDF = randDF.append(label, ignore_index=True)

	for i in range(numdif):
		folder = random.choice(os.listdir(dataset_path))
		while not os.path.isdir(os.path.join(dataset_path, folder)):
			folder = random.choice(os.listdir(dataset_path))
		folder = os.path.join(dataset_path, folder) # Folder = Number, e.g. 4
		subfolder1 = random.choice(os.listdir(folder)) # Subfolder = product, e.g. A0123456789
		image = random.choice(os.listdir(os.path.join(folder, subfolder1)))
		product_id = image[0:-4]

		subfolder2 = random.choice(os.listdir(folder))
		count = 10
		while subfolder1 == subfolder2 and count != 0:
			subfolder2 = random.choice(os.listdir(folder))

			count = count - 1

		if count == 0:
			continue

		diffimage = random.choice(os.listdir(os.path.join(folder, subfolder2)))

		image = os.path.join(folder, os.path.join(subfolder1, image))
		diffimage = os.path.join(folder, os.path.join(subfolder2, diffimage))

		im1 = np.asarray(Image.open(image))
		im2 = np.asarray(Image.open(diffimage))

		try:
			if im1.shape[2] != 3 or im2.shape[2] !=3:
				print(":(")
				continue

		except:
			continue

		label = {'image1': image, 'image2': diffimage, 'label': "different"}
		randDF = randDF.append(label, ignore_index=True)

	return randDF

def splitDF(df, destination_path, test_ratio=.2):
	different_images = df.loc[df['label'] == 'different']
	same_images = df.loc[df['label'] == 'same']

	train_diff = different_images.sample(frac=(1-test_ratio))
	test_diff = different_images.drop(train_diff.index)

	train_same = same_images.sample(frac=(1-test_ratio))
	test_same = same_images.drop(train_same.index)

	train_frames = [train_diff, train_same]
	train = pd.concat(train_frames)

	test_frames = [test_diff, test_same]
	test = pd.concat(test_frames)

	train.to_csv(destination_path + '/train.csv', index=False)
	test.to_csv(destination_path + '/test.csv', index=False)
	


dataset_path = r'../DataSets/multiimage_products'

destination_path = r'../DataSets/multiimage_products'

df = create_datasets(dataset_path, numsame=3000, numdif=3000)
print("Datasets created")
splitDF(df, destination_path)
print("Datasets split and csvs are created")
