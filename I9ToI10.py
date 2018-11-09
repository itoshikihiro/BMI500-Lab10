# THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING
# A TUTOR OR CODE WRITTEN BY OTHER STUDENTS - Jie Lin
# Python 3

#coding=utf-8
"""
@version: 1.0
@author: Jie Lin
@Mail: jlin246@emory.edu
@file: I9ToI10.py
@time: 11/02/2018 12:00pm
@purpose: this files contain a main method to call each function in class DataUtils in order to clean data
@code environment: ubuntu 18.01
"""
import sys
import pandas as pd
import numpy as np

I9noEntryCounter = 0;
I9oneToManyCounter = 0;

#read from I9 txt file
def readDataFromI9(I9_txt_path):
	data = pd.DataFrame(pd.read_csv(I9_txt_path,sep="\s+",names=["I9",'I10','flags'],dtype=str));
	return data;

#delete no map entries
def deleteNoMapEntries(data):
	global I9noEntryCounter;
	returnData = data.copy();
	for index, row in returnData.iterrows():
		if(row['flags']=='11000'):
			returnData.drop(index,inplace = True);
			I9noEntryCounter=I9noEntryCounter+1;

	#for testing purpose
	#print("there are "+str(I9noEntryCounter)+" no mapping in I9 to I10");
	return returnData;

#delete one to many entries and count how many one-to-many entries
#although we are clean data by using duplicated I9 columns
# , the I9oneToManyCounter only record once. 
def deleteOneToMany(data):
	global I9oneToManyCounter;
	returnData = data.copy();
	dup_origin_index = -1;
	dup_origin_value = "";
	deleteFlag = False;
	for index, row in returnData.iterrows():
		value = row['I9'];
		if(dup_origin_index != index and dup_origin_value==value):
			returnData.drop(index,inplace=True);
			deleteFlag=True;
		if(deleteFlag==False):
			dup_origin_value = value
			dup_origin_index = index;
		if(deleteFlag==True and dup_origin_value!=value):
			returnData.drop(dup_origin_index,inplace = True);
			I9oneToManyCounter=I9oneToManyCounter+1;
			deleteFlag = False;
			dup_origin_value = value
			dup_origin_index = index;

	return returnData;

def I9ToI10Answers(txt_path = '2018_I9gem.txt', output_path = 'I9ToI10Answers.txt'):
	I9data = readDataFromI9(txt_path);
	I9data = deleteNoMapEntries(I9data);
	I9data = deleteOneToMany(I9data);
	num_of_rows = I9data.shape[0];
	I9data.drop_duplicates(subset="I10",inplace = True, keep = False);
	real_one_to_one = I9data.shape[0];
	with open(output_path,'w+') as output_file:
		output_file.write("This document keeps the answers for I9 to I10 only\n")
		output_file.write("There are "+str(num_of_rows)+", which is based on what TA told me, one-to-one entries\n");
		output_file.write("There are "+str(real_one_to_one)+", which is based on the defination of one-to-one in Math, one-to-one entries\n");
		output_file.write("There are "+str(I9oneToManyCounter)+" one-to-many entries. \n");
		output_file.write("In general, one-to-many does not mean one is equivalent to many. One-to-many can also mean one is equivalent to the combination of many.\n");
		output_file.write("In addition, the combination of many means every element in those entries represents a partial explaination to the one. \n")
		output_file.write("There are "+str(I9noEntryCounter)+" no mapping entries. \n")
		output_file.write("9->10 is more feasible because the I9 has less number of no mapping entries than I10, which means I10 lose much more information than I9 does")




# main method
if __name__== "__main__":
    I9ToI10Answers(sys.argv[1],sys.argv[2]);
