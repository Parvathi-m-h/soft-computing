from random import seed
from random import randrange
from random import random
from csv import reader
import collections
import math
import sys

def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset
 
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())



def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	
	count_0=0
	count_1=0
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	for row in dataset:
		if row[column] == 0:
			# row[column]="yes"
			count_0=count_0+1		#rows with class label "no"
		else:
			# row[column]="no"
			count_1=count_1+1
	
	return count_0,count_1

def compare(x,y):
	comp=lambda x, y: collections.Counter(x) == collections.Counter(y)
	return comp

def eucledian_dist(dataset_row,cluster_row):
	
	sum=0
	for col in range(0,len(dataset_row)-1):
		
		diff=(dataset_row[col]-cluster_row[col])*(dataset_row[col]-cluster_row[col])
		sum+=diff
	distance=math.sqrt(sum)
	return distance

def mean(cluster):
	cluster_new=zip(*cluster)
	centroid=list()
	for i in range(0,len(cluster_new)-1):
		sum=0
		for col in cluster_new[i]:
			sum+=col
		mean=(sum)/len(cluster_new[0])
		centroid.append(mean)
	
	return centroid


def kmeans(dataset,k):
	cluster=list()
	for i in range(0,k):
		center=randrange(0,109)##109
		cluster.append(dataset[center])
	
	count_itr=0
	while True:
		cluster_0=list()
		cluster_1=list()
		
		for dataset_row in dataset:
			distance=list()
			for cluster_row in cluster:
				dist=eucledian_dist(dataset_row,cluster_row)
				distance.append(dist)

			min_dist=min(distance)
		
			
			
			cluster_index=distance.index(min_dist)
			
			

			# if type(cluster_index) is list:
			# 	cluster_index=min(cluster_index)

			if cluster_index == 0:
				cluster_0.append(dataset_row)
			
			else:
				cluster_1.append(dataset_row)
		

		centroid_0=mean(cluster_0)
		centroid_1=mean(cluster_1)
		
		
		cluster_new=list()
		

		cluster_new.append(centroid_0)
		cluster_new.append(centroid_1)
		
		count_itr=count_itr+1
		if min(cluster)==min(cluster_new) and max(cluster)==max(cluster_new):
			break
		
		cluster=cluster_new
		
		
	return cluster_0,cluster_1,count_itr




filename = sys.argv[1]
dataset = load_csv(filename)
for i in range(len(dataset[0])-1):
	str_column_to_float(dataset, i)

count_0,count_1=str_column_to_int(dataset, len(dataset[0])-1)
dataset_new=list()
dataset_new.append(dataset)
# for row in dataset:
# 	del row[44]##44

k=2
cluster_0,cluster_1,count=kmeans(dataset,k)

print "count of itr",count

print "len of cluster_0",len(cluster_0)
print "len of cluster_1",len(cluster_1)

print "count",count_0,count_1

zip_cluster_0=zip(*cluster_0)
c0=zip_cluster_0[44]
c0_new=collections.Counter(c0)

zip_cluster_1=zip(*cluster_1)
c1=zip_cluster_1[44]
c1_new=collections.Counter(c1)
print "c0_new",c0_new
print "c1_new",c1_new
max_0=0
min_0=0
if (len(c0_new)>1):
	if c0_new[0]>c0_new[1]:
		max_0=c0_new[0]
		min_0=c0_new[1]
	else:
		max_0=c0_new[1]
		min_0=c0_new[0]
else:
	 if c0_new[0]:
	 	max_0=c0_new[0]
	 else:
	 	max_0=c0_new[1]

max_1=0
min_1=0
if (len(c1_new)>1):
	if c1_new[0]>c1_new[1]:
		max_1=c1_new[0]
		min_1=c1_new[1]
	else:
		max_1=c1_new[1]
		min_1=c1_new[0]
else:
	 if c1_new[0]:
	 	max_1=c1_new[0]
	 else:
	 	max_1=c1_new[1]

print "max,min 0",max_0,min_0
print "max,min 1",max_1,min_1

acc=((max_0+max_1)*1.0/(count_1+count_0))*100
print "accuracy",acc

posPre=(((max_0)*1.0)/(max_0+min_0))*100
print "(+) Precision",posPre

posRec=(((max_0)*1.0)/(max_0+min_1))*100
print "(+) Recall",posRec

negPre=(((max_1)*1.0)/(max_1+min_1))*100
print "(-) Precision",negPre

negRec=(((max_1)*1.0)/(max_1+min_0))*100
print "(-) Recall",negRec


