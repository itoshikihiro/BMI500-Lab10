# THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING
# A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - Jie Lin
# Python 3

#coding=utf-8
"""
@version: 1.0
@author: Jie Lin
@Mail: jlin246@emory.edu
@file: I10ToI9.py
@time: 11/02/2018 12:00pm
@purpose: this files contain a main method to call each function in class DataUtils in order to clean data
@code environment: ubuntu 18.01
"""
import sys
import pandas as pd
import numpy as np

I10noEntryCounter = 0;
I10oneToManyCounter = 0;

#read from I9 txt file
def readDataFromI10(I10_txt_path):
	data = pd.DataFrame(pd.read_csv(I10_txt_path,sep="\s+",names=["I10",'I9','flags'],dtype=str));
	return data;

#delete no map entries
def deleteNoMapEntries(data):
	global I10noEntryCounter;
	returnData = data.copy();
	for index, row in returnData.iterrows():
		if(row['flags']=='11000'):
			returnData.drop(index,inplace = True);
			I10noEntryCounter=I10noEntryCounter+1;

	#for testing purpose
	#print("there are "+str(I10noEntryCounter)+" no mapping in I10 to I9");
	return returnData;

#delete one to many entries and count how many one-to-many entries
#although we are clean data by using duplicated 10 columns
# , the I10oneToManyCounter only record once. 
def deleteOneToMany(data):
	global I10oneToManyCounter;
	returnData = data.copy();
	dup_origin_index = -1;
	dup_origin_value = "";
	deleteFlag = False;
	for index, row in returnData.iterrows():
		value = row['I10'];
		if(dup_origin_index != index and dup_origin_value==value):
			returnData.drop(index,inplace=True);
			deleteFlag=True;
		if(deleteFlag==False):
			dup_origin_value = value
			dup_origin_index = index;
		if(deleteFlag==True and dup_origin_value!=value):
			returnData.drop(dup_origin_index,inplace = True);
			I10oneToManyCounter=I10oneToManyCounter+1;
			deleteFlag = False;
			dup_origin_value = value
			dup_origin_index = index;

	return returnData;

def I10ToI9Answers(txt_path = '2018_I10gem.txt', output_path = 'I10ToI9Answers.txt'):
	I10data = readDataFromI10(txt_path);
	I10data = deleteNoMapEntries(I10data);
	I10data = deleteOneToMany(I10data);
	num_of_rows = I10data.shape[0];
	I10data.drop_duplicates(subset="I9",inplace = True, keep = False);
	real_one_to_one = I10data.shape[0];
	with open(output_path,'w+') as output_file:
		output_file.write("This document keeps the answers for I10 to I9 only\n")
		output_file.write("There are "+str(num_of_rows)+", which is based on what TA told me, one-to-one entries\n");
		output_file.write("There are "+str(real_one_to_one)+", which is based on the defination of one-to-one in Math, one-to-one entries\n");
		output_file.write("There are "+str(I10oneToManyCounter)+" one-to-many entries. \n");
		output_file.write("In general, one-to-many does not mean one is equivalent to many. One-to-many can also mean one is equivalent to the combination of many.\n");
		output_file.write("In addition, the combination of many means every element in those entries represents a partial explaination to the one. \n")
		output_file.write("There are "+str(I10noEntryCounter)+" no mapping entries. \n")
		output_file.write("9->10 is more feasible because the I9 has less number of no mapping entries than I10, which means I10 lose much more information than I9 does")




# main method
if __name__== "__main__":
    I10ToI9Answers(sys.argv[1],sys.argv[2]);
