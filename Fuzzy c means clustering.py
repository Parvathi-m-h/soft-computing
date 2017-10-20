import sys
from csv import reader
import csv
from random import randrange
from random import random
import math
import collections
import copy
import numpy as np

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
			count_0=count_0+1		#rows with class label "yes"
		else:
			# row[column]="no"
			count_1=count_1+1
	
	return count_0,count_1

def eucledian_dist(dataset_row,cluster_row):
	
	sum=0
	for col in range(0,len(dataset_row)-1):
		
		diff=(dataset_row[col]-cluster_row[col])*(dataset_row[col]-cluster_row[col])
		sum+=diff
	distance=math.sqrt(sum)
	return distance

cluster_0=list()
cluster_1=list()
def fcm(dataset):
	k=2
	m=2.0
	theta=0.3
	
	
	# Uij_prev=[[randrange(0,1) for col in range(0,k)] for row in range(0,len(dataset))]
	Uij_prev=np.random.dirichlet(alpha=(len(dataset),2),size=len(dataset))
	# print len(Uij_prev)
	while True:

		Uij_col=zip(*Uij_prev)
		dataset_new=copy.deepcopy(dataset)
		dataset_col=zip(*dataset_new)
		cluster=list()

		data_col_len=len(dataset_col)
		del dataset_col[data_col_len-1]#deleting class label column
		# print dataset
		
		for row in Uij_col:	
			cluster_row=list()
			for dataset_row in dataset_col:
				res=0
				sum=0
				for idx in range(0,len(Uij_col[0])):
					power=float(math.pow(row[idx],m))
					res=res+float(power*dataset_row[idx])
					sum=sum+power
				c=float(res/sum)
				cluster_row.append(c)
			cluster.append(cluster_row)



		Uij_new=list()
		for i in dataset:
			Uij_row=list()
			for j in cluster:
				sum=0
				for cluster_row in cluster:
					numer=eucledian_dist(i,j)#i=dataset_row
					denom=eucledian_dist(i,cluster_row)
					div=float(numer/denom)
					power=float(2/(m-1))
					sum=sum+math.pow(div,power)
					# Uij_row.append(ans)

				res=float(1/sum)
				Uij_row.append(res)
			
			Uij_new.append(Uij_row)

		# return Uij


		
		# return Uij,cluster_new
		flag=0
		for i in range(0,len(Uij_new)):
			for j in range(0,len(Uij_new[0])):
				diff=Uij_new[i][j] - Uij_prev[i][j]
				# print "diff i j",diff,i,j
				if (diff > theta):
					flag=1
					
		
		Uij_prev=Uij_new
		
		
		if (flag == 0):
			break
		
		
	return Uij_new,cluster

filename = sys.argv[1]
dataset = load_csv(filename)
for i in range(len(dataset[0])-1):
	str_column_to_float(dataset, i)


count_0,count_1=str_column_to_int(dataset, len(dataset[0])-1)

Uij,cluster_new=fcm(dataset)
# print Uij
# print "cluster_new",cluster_new
i=0
for row in Uij:
	idx=row.index(max(row))

	if (idx==0):
		cluster_0.append(dataset[i])
	else:
		cluster_1.append(dataset[i])
	i+=1

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

print "max,min of cluster 0",max_0,min_0#tp,fn
print "max,min of cluster 1",max_1,min_1#tn,fp

acc=((max_0+max_1)*1.0/(count_1+count_0))*100#(tp+tn)/(len(dataset))
print "accuracy",acc

posPre=(((max_0)*1.0)/(max_0+min_0))*100 #tp/(tp+fn) 
print "(+) Precision",posPre

posRec=(((max_0)*1.0)/(max_0+min_1))*100#tp/(tp+tn) 
print "(+) Recall",posRec

negPre=(((max_1)*1.0)/(max_1+min_1))*100#fp/(tp+tn)
print "(-) Precision",negPre

negRec=(((max_1)*1.0)/(max_1+min_0))*100#fp/(fp+fn)
print "(-) Recall",negRec







# cluster_0=list()
# cluster_1=list()
# if row in cluster_new:
# 			if (row[44]== 0):

# 				cluster_0.append(row)
# 			else:
# 				print "row[44]",row[44]
# 				cluster_1.append(row)
