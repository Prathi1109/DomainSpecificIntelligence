import pandas as pd
import numpy as np
from collections import defaultdict
import os
import json

class LogGeneration:

    def __init__(self, data_path):
        self.data_path = data_path
        self.all_logs = defaultdict(list)
        self.all_sensor_logs = []

    def merge_two_dicts(self, x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z

    def list_files(self, dir):
        return next(os.walk(dir))[1]

    def frameProcess(self, frame_data):
        entity_json = {"person":0, "car":0, "bicycle":0, "bus":0, "truck":0, "motorbike":0, 'traffic light':0}

        for index, row in frame_data.iterrows():
#            if row[6] in entity_json.keys():
#              try:
            entity_json[row[6]] = entity_json[row[6]] + 1
            print("entity_json",entity_json)    
#                  print("noerror")
#              except:
#                  print("object missing")   #If there is a new object in our csv file it will throw an exception

        return entity_json

    def preprocessing(self):
#        csv_files = self.list_files(self.data_path)
#        sensor_csv_files = self.list_files(self.data_path)

        global_index = 0

       # for files, sensor_files in zip(csv_files,sensor_csv_files):
#            dataset = pd.read_csv(self.data_path+"/"+files+"/rgb_output1.csv", sep=",")
        dataset = pd.read_csv("/home/motorai/Workstation/DomainSpecificIntelligence/rgb_output1.csv", sep=",")
       # print("dataset",dataset)
        sensor_dataset = pd.read_csv("/home/motorai/Workstation/DomainSpecificIntelligence/gps_data1.csv", sep=",")
        frame_ids = np.unique(dataset.iloc[:, 0])



    def object_process(self):

#        csv_files = self.list_files(self.data_path)

        global_index = 0
        self.length_list=[]

#        for files in csv_files:
        dataset = pd.read_csv("/home/motorai/Workstation/DomainSpecificIntelligence/rgb_output1.csv", sep=",")
  
        frame_ids = np.unique(dataset.iloc[:, 0])

        self.length_list.append(len(frame_ids))
        for ids in frame_ids:
            x = dataset.loc[dataset[dataset.columns[0]] == ids]
            frame_data = self.frameProcess(x)
            self.all_logs[global_index].append(frame_data)

            global_index += 1

        return self.all_logs

    def sensor_process(self):

#        csv_files = self.list_files(self.data_path)

        global_index = 0

        #for files in csv_files:
        dataset = pd.read_csv("/home/motorai/Workstation/DomainSpecificIntelligence/gps_data1.csv", sep=",")
        #print("dataset",dataset)
        valid_data = dataset.loc[dataset[dataset.columns[1]] != 0]
        #print("valid_data\n",valid_data)
        speed_list=[]
        for index, row in valid_data.iterrows():

            speed_list.append(row[5])
        speed_list=[y for x in speed_list for y in (x,)*24]


        self.all_sensor_logs.append(speed_list)

        #print("speed_list",speed_list)
        speed_list=[]
#           print("len(self.all_sensor_logs)",len(self.all_sensor_logs))

        global_index += 1

        x=[(a, b[:a]) for a, b in zip(self.length_list,self.all_sensor_logs)]
        self.all_sensor_logs=[b for a,b in x]
   #    print("manipulation list",[len(x) for x in self.all_sensor_logs])
        self.all_sensor_logs = [j for i in self.all_sensor_logs for j in i]
        return self.all_sensor_logs


    def mergeObjectSensor(self, objects, sensor):
        obj_val=[]
        for d in objects.values():
           resultdict={'objects':d}
           obj_val.append(resultdict)

        speed_add=[]
        for d in sensor:
           result={'speed':d}  #Add speed values by taking from the val_list
           speed_add.append(result)


        my_list=[]
        for i in range(len(obj_val)):  #Merge object and speed tags of each frame

            my_list.append(self.merge_two_dicts(obj_val[i],speed_add[i]))

        final_dict= {k:v for k,v in zip(objects.keys(),my_list)}
        
        with open("/home/motorai/Workstation/DomainSpecificIntelligence/Object_Counts.json", 'w') as fp:
            json.dump(final_dict,fp)

        return final_dict
