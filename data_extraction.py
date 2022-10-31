#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 11:49:54 2022

@author: keatangill
"""



from netCDF4 import Dataset 
import numpy as np




#reading cdf file
my_example_nc_file = ' ' #path to either cyclic or anticyclic eddy file
fh = Dataset(my_example_nc_file, mode='r') 

#extracting all necessary varibles 
lons = fh.variables['longitude'][:]
lats = fh.variables['latitude'][:] 
radius = fh.variables['effective_radius'][:] 
time = fh.variables['time'][:] 
track = fh.variables['track'][:]


fh.close 


#forming data into a NumPy array 
lons = list(lons)
lats = list(lats)
radius = list(radius)
time = list(time) 
track = list(track)


eddies_dataset = np.array([lons,lats,radius,time,track])   
eddies_dataset = np.transpose(eddies_dataset)


#setting boundary constraints on the area of eddies 
lon_min = -10
lon_max = 10

lat_min = 60
lat_max = 80 

min_date = 25570           #days from 01/01/1950
max_date = min_date + 15



#refineing data set to boundary constraints 
eddies_dataset = eddies_dataset[eddies_dataset[:, 3] > min_date, :]  
eddies_dataset = eddies_dataset[eddies_dataset[:, 3] < max_date, :]

eddies_dataset = eddies_dataset[eddies_dataset[:, 0] > lon_min, :] 
eddies_dataset = eddies_dataset[eddies_dataset[:, 0] < lon_max, :] 


eddies_dataset = eddies_dataset[eddies_dataset[:, 1] > lat_min, :] 
eddies_dataset = eddies_dataset[eddies_dataset[:, 1] < lat_max, :]


eddies_dataset = np.delete(eddies_dataset, 3, 1)  





#calculating average position and effective radius of eddies
eddies =[]
for i in np.unique(eddies_dataset[:,3]):
    average_location = eddies_dataset[eddies_dataset[:, 3] == i, :]
    average_location = np.mean(average_location, axis=0)
    eddies.append(average_location)
    average_location = []
    
eddies = np.array(eddies)
eddies = np.delete(eddies, 3, 1)  





#outputting array as csv file 
filename = "eddies_3.2NRT_"+str(min_date)
np.savetxt("%s.csv" % filename, eddies, delimiter=",")

    
  
    














