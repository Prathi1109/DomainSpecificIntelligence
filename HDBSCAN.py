import json
from sklearn.cluster import DBSCAN
import numpy as np
import math
from collections import defaultdict
import hdbscan
from collections import Counter
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import collections

def translatePattern(final_indexed_data, all_labels, obj_list):
    local_cluster_log = {}
    all_cluster_logs = {}
    unique_labels = np.unique(all_labels)

    unique_labels = np.delete(unique_labels, np.where(unique_labels == -1))

    final_indexed_data['cluster_labels'] = all_labels

    print("unique_labels",unique_labels)

    for label in unique_labels:
        if label != -1:
            cluster_members = final_indexed_data.loc[final_indexed_data['cluster_labels'] == label]
            for obj in obj_list:
                freq_member = cluster_members[obj].value_counts().idxmax()
                local_cluster_log[obj] = freq_member
            
            local_cluster_log['size'] = cluster_members.shape[0]

            all_cluster_logs[label] = local_cluster_log
    
            local_cluster_log = {}
    print("all_cluster_logs",all_cluster_logs)
    return final_indexed_data,unique_labels,all_cluster_logs



def findMinClusterSize(log_length, onehot_indexed_data):
    cluster_log = {}
    min_sample_sizes = [int(log_length * 0.5/100), int(log_length * 1/100), int(log_length * 1.5/100),
                       int(log_length * 2/100), int(log_length * 2.5/100), int(log_length * 3/100)
                       , int(log_length * 3.5/100), int(log_length * 4/100)]

    for min_sample_size in min_sample_sizes:
        clustering = hdbscan.HDBSCAN(min_cluster_size=min_sample_size, metric='euclidean')
        all_labels = clustering.fit_predict(onehot_indexed_data)
        
        counter = dict(collections.Counter(all_labels))
        cluster_log[min_sample_size] = counter[-1]
        print("Min size= "+str(min_sample_size)+ ", Noise cluster size= "+str(counter[-1]))
    
    best_min_size = min(cluster_log, key=cluster_log.get)
    print("Best min sample size: "+str(best_min_size))
    return best_min_size

def generateCluster(final_indexed_data, obj_list):
    enc = OneHotEncoder(handle_unknown='ignore')
    onehot_indexed_data = enc.fit_transform(final_indexed_data).toarray()
    log_length = len(onehot_indexed_data)

    best_min_size = findMinClusterSize(log_length, onehot_indexed_data)

    clustering = hdbscan.HDBSCAN(min_cluster_size=168, metric='euclidean')
    all_labels = clustering.fit_predict(onehot_indexed_data)
    print("all_labels",all_labels)
    counter=collections.Counter(all_labels)
    print(counter)

    print("Clustering completed, translating pattern...")

    final_indexed_data,unique_labels,all_cluster_logs = translatePattern(final_indexed_data, all_labels, obj_list)
    #To display the datapoints(After Indexing) belonging to each cluster
#    for i in range(len(unique_labels)):
#        print(final_indexed_data[final_indexed_data['cluster_labels']==i].to_string())
# 
    return final_indexed_data,unique_labels,all_cluster_logs
