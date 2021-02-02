import os
import numpy as np
import torch
import torch.nn as nn
import torchvision
from torch.utils.data import DataLoader
from modified_alexnet import Modified_AlexNet
import modified_vgg
from Concatenator import Concatenator
from pathlib import Path

curr_path = os.path.dirname(os.path.abspath(__file__))
datasets_path = str(Path(curr_path).parents[0]) +  "/AmazonSet"

print("Concatinating training data")
training_concatenator = Concatenator(datasets_path, "train_expanded.csv")
print("Finished")

print("Concatinating testing data")
testing_concatenator = Concatenator(datasets_path, "test_expanded.csv")
print("Finished")

print("Loading training set")
batch_size = 64
trainloader = DataLoader(training_concatenator, batch_size, shuffle=True)

print("Loading testing set")
batch_size = 64
testloader = DataLoader(testing_concatenator, batch_size, shuffle=False)

print("Creating Model")
model = Modified_AlexNet()
#model = modified_vgg.vgg11()
print(model)

print("Training Model")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

for epoch in range(3):

	running_loss = 0.0
	for i, batch in enumerate(trainloader, 0):

		concat_images, labels = batch
		optimizer.zero_grad()

		outputs = model(concat_images)
		loss = criterion(outputs, labels)
		loss.backward()
		optimizer.step()

		running_loss += loss.item()

	print(f"Epoch {epoch}: Loss = {running_loss}")
	running_loss = 0

print("Testing Model")

correct = 0
total = 0

with torch.no_grad():
	for data in testloader:
		images, labels = data
		outputs = model(images)
		_, predicted = torch.max(outputs.data, 1)
		total += labels.size(0)
		correct += (predicted == labels).sum().item()

print(f"Accuracy over test set: {100*correct/total}%")
print(correct)
print(total)

