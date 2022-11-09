from rbm import RBM
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np

def process(final_indexed_data):

    cluster_labels = pd.DataFrame(final_indexed_data['cluster_labels'])
    
    cluster_labels = cluster_labels[cluster_labels.cluster_labels != -1]
   
    onehot_encoded = OneHotEncoder(handle_unknown='ignore')
    onehot_cluster_index = onehot_encoded.fit_transform(cluster_labels).toarray()
#    print("onehot_cluster_index in list length",len(onehot_cluster_index.tolist()))
#
#    print("onehot_encoded.inverse_transform(onehot_cluster_index) list",onehot_encoded.inverse_transform(onehot_cluster_index).tolist())
#    print("onehot_cluster_index list",onehot_cluster_index.tolist())
#    print("onehot_cluster_index.shape[1]",onehot_cluster_index.shape[1])
#    print("onehot_cluster_index.shape[0]",onehot_cluster_index.shape[0])
    r = RBM(num_visible = onehot_cluster_index.shape[1], num_hidden = 1)

    r.train(onehot_cluster_index, max_epochs = 3000)
    
    weights = list(r.weights)
    print("weights",weights)
    
#    visible = r.run_hidden( np.array([[weights[0][1]]]) )
#    print("visible",visible)
    
    return weights    
#    user = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]])
#    print("r.run_visible(user)[7]",r.run_visible(user))
#    user1=np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]])
#    print("r.run_visible(user)[5]",r.run_visible(user1))
    