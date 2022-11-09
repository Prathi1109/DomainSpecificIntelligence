from data_preprocess import LogGeneration
import matplotlib.pyplot as plt
import numpy as np
import jenkspy
import pandas as pd
import HDBSCAN as hdb
import cluster_weight_analysis as cwa
import sys
#sys.stdout = open('Analysis_new.txt', 'w')
import os
filepath = os.getcwd()

def generate_index(data, bin_ranges):
    bin_ranges[-1] += 10**-6
    data=np.digitize(np.array(data),bin_ranges)
    return data

def mean(lst):
    if len(lst) != 0:
        return sum(lst) / len(lst)
    else:
        return 0

def goodness_of_variance_fit(array, classes):
   # get the break points
   #print(classes)
   classes = jenkspy.jenks_breaks(array, classes)
   # classes=classes.tolist()
  
   # do the actual classification
   classified = np.array([classify(i, classes) for i in array])
   #print(classified.tolist())
   # max value of zones
   maxz = max(classified)

   # nested list of zone indices
   zone_indices = [[idx for idx, val in enumerate(classified) if zone + 1 == val] for zone in range(maxz)]
   #print(zone_indices)

   # sum of squared deviations from array mean

   sdam = np.sum((np.array(array) -mean(array)) ** 2)

   # sorted polygon stats
   array_sort = [np.array([array[index] for index in zone]) for zone in zone_indices]

   # sum of squared deviations of class means

   sdcm = sum([np.sum((classified - mean(classified)) ** 2) for classified in array_sort])

   # goodness of variance fit
   gvf = (sdam - sdcm) / sdam
 
   return classes, gvf

def classify(value, breaks):
   for i in range(1, len(breaks)):
       if value < breaks[i]:
           return i
   return len(breaks) - 1

def data_parser(obj_list, all_logs):
    #Parameters
    max_itr = 15
    gvf = 0.0
    nclasses = 2
    itr = 0

    data = []

    final_indexed_data = {}
    test_classes=[]
    for obj_key in obj_list:

        max_itr = 15
        gvf = 0.0
        nclasses = 2
        itr = 0

        if obj_key != 'speed':
            for keys, val in all_logs.items():
                data.append(val['objects'][0][obj_key])

        elif obj_key == 'speed':
            for keys, val in all_logs.items():
                data.append(val['speed'])

        while gvf < 0.8:
           classes, gvf = goodness_of_variance_fit(data, nclasses)
           classes = list(dict.fromkeys(classes))

           nclasses += 1
           itr += 1
           if itr == max_itr:
               break
        #print(obj_key,"Range:",classes)
        test_classes.append(classes)
        
        indexed_sensor_logs = generate_index(data, classes)
        data = []
        
        final_indexed_data[obj_key] = indexed_sensor_logs
        size = len(final_indexed_data[obj_key])
    
    return final_indexed_data, size,test_classes
 
frame_index = 0
Indexed_Json = {}
obj_list = ["person", "car", "bicycle", "bus", "truck", "motorbike", "traffic light", "speed"]

#access = LogGeneration("/Volumes/Prathibha/Testdata")
access = LogGeneration("/home/motorai/Workstation/DomainSpecificIntelligence")
access.preprocessing()
objects = access.object_process()
sensor = access.sensor_process()
print("Data Preprocessing completed successfully")

#Dictionary created with no of objects in each frame
final_dict = access.mergeObjectSensor(objects, sensor)

#Indexing the values 
final_indexed_data, size,test_classes = data_parser(obj_list, final_dict)

final_indexed_data = pd.DataFrame.from_dict(final_indexed_data)

print("Virtual Indexing completed successfully")

final_indexed_data ,unique_labels,all_cluster_logs= hdb.generateCluster(final_indexed_data, obj_list)

weights=cwa.process(final_indexed_data)
print("unique_labels",unique_labels)
print("weights",weights)
weights.pop(0)
weights=[l[1] for l in weights]
cluster_weights=dict(zip(unique_labels, weights))
print("all_cluster_logs",all_cluster_logs)
print("##################Displaying cluster_weights##################")
print("cluster_weights",cluster_weights)


tuples_list=[]
for i in test_classes:
    new_list = [x-0.000001 if x!=1.000001 else float(round(x-0.000001)) for x in  i[1:]] 
    enumer_list=[t+1 for t in range(len(i)-1)] 
    i.pop(-1)
    combo=tuple(zip(i,new_list,enumer_list))
    tuples_list.append(combo)
print(tuples_list)

Ranges_Dictionary = dict(zip(obj_list, tuples_list))


def MakeFile(file_name,test_classes):
    
    file = open(file_name, 'w')

    file.write('''
class VirtualIndex:
    VIRTUAL_INDEX=''')
    file.write(str(Ranges_Dictionary)) 
    file.write('''\n 
    @classmethod
    def keys(cls):
        return cls.VIRTUAL_INDEX.keys()

    @classmethod
    def bins(cls):
        return cls.VIRTUAL_INDEX''')
    file.close()
    
    print('Execution completed.') 
    
MakeFile("virtual_index.py",test_classes)





