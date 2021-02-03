import torch
import numpy as np

def Tensor_confusion_matrix(prediction, labels):
	# prediction and labels are 1D tensors

	true_0 = 0
	true_1 = 0
	false_0 = 0
	false_1 = 0

	pred_array = prediction.numpy().tolist()
	labels_array = labels.numpy().tolist()

	for index, item in enumerate(pred_array):
		if item == 0:
			if labels_array[index] == 0:
				true_0 += 1
			else:
				false_0 += 1

		elif item == 1:
			if labels_array[index] == 0:
				false_1 += 1
			else:
				true_1 += 1

	return (true_0, true_1, false_0, false_1) 

