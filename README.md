# DomainSpecificIntelligence
Identify Patterns in the dataset using standardized approach\
A general understanding of traffic scenarios on a given environment type\
Consideration of different traffic and environmental attributes\
Generalization by Virtual Indexing\
Unsupervised in fashion\

**Virtual Indexing**\
A statistical approach to create ranges of different traffic and self attributes\
An iterative process of finding out an optimal split in the data, which has least variance\
Each attribute is checked for ‘goodness of variance’ \
The optimal splits are indexed

**Implemented using Hierarchical Density Based Clustering (Bottom up approach)**\
Dendrogram has a fixed hardcoded value for epsilon (DBSCAN Hyperparameter)\
The dendrogram is traversed until ‘min sample’ number of samples is met \
Only one hyperparameter\

