"""

An example hierarchical clustering by using the OutputGenerator

"""
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from OutputGenerator import OutputGenerator
PATH = "./GMQLData/job_data2_anil_20170427_151726_MAPPED_EXT/files"



#
# desired_column = 'count_GENES_PATIENTS'
# o = OutputGenerator(PATH)
# schema_file = o._get_file("schema")
# o.read_all_meta_data()
#
# o.read_all(PATH,schema_file,desired_column)
# print o.data.head(3)
# o.to_matrix(desired_column)
# o.remove_zeros()
# print o.data.shape
# o.data.to_pickle("2d-dataframe_count_GENES_PATIENTS")

df = pd.read_pickle("2d-dataframe_count_GENES_PATIENTS")
X = df.values.transpose()
print X.shape

# perform hierarchical clustering

methods = ['single','complete','average','weighted','centroid','median','ward']
i = 0
Z = []
for m in methods:
    Z = linkage(X, m, 'euclidean')  # cosine divides by length, use euclidean

    # calculate full dendrogram
    plt.figure(i)
    plt.title(m)
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.  # rotates the x axis labels
    )
    i = i + 1
    
plt.show()

