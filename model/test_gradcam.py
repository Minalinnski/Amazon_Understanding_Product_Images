import os
import numpy as np
import torch
import math
import csv
import matplotlib.pyplot as plt
from PIL import Image
from ast import literal_eval
from modified_lenet import Modified_LeNet
from Concatenator import Concatenator
from pytorch_grad_cam import CAM
from pytorch_grad_cam.utils.image import show_cam_on_image


def test_gradcam(size='small'):
	parameters_path = os.path.join(os.getcwd(), "parameters")
	results_path = os.path.join(os.getcwd(), size)
	results_file = os.path.join(results_path, size + '_results.csv')

	with open(results_file, 'r') as f:
	    mycsv = csv.reader(f)
	    mycsv = list(mycsv)
	    image_dim = literal_eval(mycsv[4][1])
	    batch_size = int(mycsv[5][1])

	print(image_dim)
	print(type(image_dim))
	print(batch_size)
	print(type(batch_size))
	batch_size = 64

	dim = image_dim[0]
	dim = int((int(dim/2) - 2)/2) - 6
	model = Modified_LeNet(batch_size=batch_size, dim=dim)
	model.load_state_dict(torch.load(os.path.join(parameters_path, size + '.pth')))

	test_images_path = os.path.join(os.getcwd(), 'Test_GradCam')

	for folder in os.listdir(test_images_path):
		print(folder)
		f = os.path.join(test_images_path, folder)

		image0 = os.listdir(f)[0]
		image1 = os.listdir(f)[1]

		image0 = os.path.join(f, image0)
		image1 = os.path.join(f, image1)

		concatenator = Concatenator(csvfile=None, image_dim=image_dim)
		input_tensor = concatenator.concatenate(image0, image1)
		input_tensor = torch.tensor(np.expand_dims(input_tensor, axis=0))
		#torch_img = torch.tensor(np.expand_dims(torch_img, axis=0))
		method = 'gradcam++'

		target_layer = model.layer6

		cam = CAM(model=model, target_layer=target_layer)

		grayscale_cam = cam(input_tensor=input_tensor, method=method)

		first_image = concatenator.transform_image(image0).numpy()
		first_image = np.moveaxis(first_image, 0, -1)
		visualization0 = show_cam_on_image(first_image, grayscale_cam)
		plt.imshow(visualization0)
		plt.show()


test_gradcam(size='small')