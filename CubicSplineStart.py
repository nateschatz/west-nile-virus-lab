# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 13:07:53 2018

@author: Nathanael Schatz
"""

#%%
##Import the correct packages
import matplotlib.pyplot as plt #to plot functions
import numpy as np #to make arrays of data
import pandas as pd #used to help import data
from scipy import interpolate as intp 
import csv

#%%Defining functions for importing
#YOU DO NOT NEED TO CHANGE ANYTHING HERE
#The functions get_monthly_data() and
#get_weekly_data() return a list of data. 
#They will be used to extract data from
#the csv file with raw West Nile Virus data
def read_file(filename):
	data_read = []
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				print(str(len(row)) + " columns in total")
				print("Column names are " + ", ".join(row))
			else:
				data_read.append(row)
			line_count += 1
		print(str(line_count) + " rows in total")
	return data_read

####Function to get the monthly data
def get_monthly_data(data):
	to_ret = []
#	test_tot = 0
	for i in range(12):
		to_ret.append([0.0,0,0.0]) # [tot positive, tot data entry, percentage of positive]
	for row in data:
		month = int(row[6].split("/")[0]) - 1
		if row[8] == "positive":
#			test_tot += 1
			to_ret[month][0] += 1
		to_ret[month][1] += 1
	for j in range(12):
		if to_ret[j][1] != 0:
			to_ret[j][2] = to_ret[j][0] / to_ret[j][1]
		else:
			to_ret[j][2] = 0
	return pd.DataFrame(to_ret)[2] 

###Function to get the weekly averages
def get_weekly_data(data):
	to_ret = []
#	test_tot = 0
	for i in range(52):
		to_ret.append([0.0,0,0.0]) # [tot positive, tot data entry, percentage of positive]
	for row in data:
		week = int(row[1]) - 1
		if row[8] == "positive":
#			test_tot += 1
			to_ret[week][0] += 1
		to_ret[week][1] += 1
	for j in range(len(to_ret)):
		if to_ret[j][1] != 0:
			to_ret[j][2] = to_ret[j][0] / to_ret[j][1]
		else:
			to_ret[j][2] = 0
#	print(str(test_tot) + " pos in total")
	return pd.DataFrame(to_ret)[2]


#%%Import the data
#There was no data for the first few and last few months of each year
#For the x coordinates, we used months
#For the y coordinates, we used the proportion of positive traps
# num of positive traps/total number of traps tested for each month
data = read_file("West_Nile_Virus__WNV__Mosquito_Test_Results.csv")


#%%Extract the desired data
names = ['1 - Jan.','', '3 - Mar.', '', '5 - May', '', '7 - Jul.', '', '9 - Sep.', '', '11 - Nov.', ''] #months
xmonth = np.arange(1,13,1)#Months
xweek = np.linspace(1,13, num=52)#This generates x-points for weeks, scaled to match months
xgraph = np.linspace(1,max(xmonth),1000)#These points are just used to graph the function
ymonth = get_monthly_data(data)#Extract monthly data

#Using ymonth as an example, get the weekly data
#FINISH THE CODE HERE
yweek = 'insert your code here' #Use the get_weekly_data function to extract weekly data
csmonth = intp.CubicSpline(xmonth,ymonth)#Cubic Spline for monthly data

#FINISH THE CODE HERE
csweek = 'insert your code here' # use the intp.Cubic Spline function for weekly data


 #%%Plot the data points and the interpolated line
plt.plot(xmonth,ymonth,'o', xweek, yweek,"x", xgraph, csmonth(xgraph), '-', xgraph, csweek(xgraph), '--')
plt.legend(['Monthly Data', 'Weekly Data','Spline for Month', 'Spline for week'], loc = 'best')
plt.xlabel("Month")
plt.xticks(xmonth, names)
plt.ylabel("Propotion of positive traps")
plt.title("Predicted Prevalence of West Nile Virus by Month")
plt.show()
