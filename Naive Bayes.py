
from random import seed
from random import randrange
from random import random
from csv import reader

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
	dataset_0=list()
	dataset_1=list()
	count_0=0
	count_1=1
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	for row in dataset:
		if row[column] == 0:
			dataset_0.append(row)
			count_0=count_0+1		#rows with class label "no"
		else:
			dataset_1.append(row)		#rows with class label "yes"
			count_1=count_1+1
	prob_0=(count_0)/((count_1+count_0)*1.0)
	prob_1=(count_1)/((count_1+count_0)*1.0)
	return dataset_0,dataset_1,prob_0,prob_1


 
def calculate_mean_std_dev(dataset):
	attr=[]
	mean_list=list()
	std_dev_list=list()
	for col in range(0,len(dataset[0])-1):
		attr.append(zip(*dataset)[col]) # transpose of our dataset
	#print "attr[0][0]",attr[0][0]
	#print attr
	for row in attr:
	    sum=0.0
	    for column in range(0,len(dataset)-1):
	    	sum+=row[column]
	    	#print row[column]
	    mean=(sum)/(len(dataset))
	    #print "row ",row,"  mean ",mean
	    mean_list.append(mean)
	    num=0
	    for column in range(0,len(dataset)-1):
	    	num+=(column-mean)*(column-mean)
	    std_dev_sq=(num)/(len(dataset)-1)
	    std_dev=math.sqrt(std_dev_sq)
	    std_dev_list.append(std_dev)
	#print mean_list
	#print std_dev_list
	return mean_list,std_dev_list	 	

def con_probability(mean_list,std_dev_list,fold_row):
	mul=1
	for i in range(0,len(fold_row)-1):
		#print fold_row[0]
		#print mean_list[i]
		a=(fold_row[i]-mean_list[i])*(fold_row[i]-mean_list[i])
		b=2*(std_dev_list[i])*(std_dev_list[i])*1.0
		c=a/(b)
		expo=math.exp(-c)

		d=math.sqrt(2*math.pi)*(std_dev_list[i])
		res=expo/d
		
		mul*=res
	#print "mul",mul	
	return mul	


filename = sys.argv[1]
dataset = load_csv(filename)
for i in range(len(dataset[0])-1):
	str_column_to_float(dataset, i)

len_new=int((len(dataset)*(0.7)))
fold=list()
fold=dataset[len_new:len(dataset)-1]
del dataset[len_new:len(dataset)-1]

dataset_0,dataset_1,prob_0,prob_1=str_column_to_int(dataset, len(dataset[0])-1)

mean_list_0,std_dev_list_0=calculate_mean_std_dev(dataset_0)
#print mean_list_0,std_dev_list_0
mean_list_1,std_dev_list_1=calculate_mean_std_dev(dataset_1)
#print mean_list_1,std_dev_list_1


attr=[]
count=0
for row in range(0,len(fold)):
	#print "fold[row] ",fold[row]

	res_0=con_probability(mean_list_0,std_dev_list_0,fold[row])
	res_1=con_probability(mean_list_1,std_dev_list_1,fold[row])
	final_res_0=res_0*prob_0
	final_res_1=res_1*prob_1  	
	#print res_0,res_1, "prob_0,prob_1",prob_0,prob_1
	if(res_0<res_1):
		#print "row ",fold[row], "belongs to YES"
		predicted="Yes"
	else:
		#print "row ",fold[row], "belongs to NO"
		predicted="No"
	#print "fold",fold[row][len(fold[0])-1]," predicted",predicted
	if(fold[row][len(fold[0])-1]== predicted):

		count=count+1
acc=((count)/(len(fold)*1.0))*100
print acc	
