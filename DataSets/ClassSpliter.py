# Returns a list of classes to be considered.
# If size == 'small', return 10 random classes
# If size == 'mediium', return 20 random classes
# If size == 'large', return all classes

import os
import random

def ClassSpliter(dataset_path, size='small'):

	classes = []

	if size == 'small':
		num_classes = 10

	elif size == 'medium':
		num_classes = 20

	elif size == 'large':
		return os.listdir(dataset_path)

	while num_classes != 0:
		folder = random.choice(os.listdir(dataset_path))
		if folder not in classes and os.path.isdir(os.path.join(dataset_path, folder)):
			classes.append(folder)
			num_classes = num_classes - 1

	print(classes)
	return classes



