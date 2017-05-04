"""

An example hierarchical clustering by using the OutputGenerator

"""
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from OutputGenerator import OutputGenerator
from scipy.cluster.hierarchy import fcluster
PATH = "./GMQLData/job_data2_anil_20170427_151726_MAPPED_EXT/files"
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
import operator


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

o = OutputGenerator(PATH)
schema_file = o._get_file("schema")
o.read_all_meta_data()
meta = o.meta_data
df = pd.read_pickle("2d-dataframe_count_GENES_PATIENTS")
X = df.values.transpose()
print X.shape

# perform hierarchical clustering

methods = ['ward','single','complete','average','weighted','centroid','median']
methods = ['ward']
i = 0
Z = []
cluster_index = []
for m in methods:
    Z = linkage(X, m, 'euclidean')  # cosine divides by length, use euclidean
    max_d = 17
    cluster_index = fcluster(Z, max_d, criterion='distance')
    print cluster_index
    #calculate full dendrogram
    plt.figure(i)
    plt.title(m)
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.  # rotates the x axis labels
    )
    i = i + 1



def calculate_jaccard(meta, metadata_key, cluster_index, sample_size):
    TP = FP = TN = FN = 0.0
    # pair-wise comparison
    all_samples = range(0, sample_size)
    unvisited_samples = range(0, sample_size)
    for x_i in all_samples:  # for each sample
        unvisited_samples.remove(x_i)
        try:
            for x_j in unvisited_samples:  # for each other sample
                if cluster_index[x_i] == cluster_index[x_j] and meta[x_i][metadata_key] == meta[x_j][metadata_key]:
                    TP = TP + 1
                elif cluster_index[x_i] == cluster_index[x_j] and meta[x_i][metadata_key] != meta[x_j][metadata_key]:
                    FP = FP + 1
                elif cluster_index[x_i] != cluster_index[x_j] and meta[x_i][metadata_key] == meta[x_j][metadata_key]:
                    FN = FN + 1
                else:
                    TN = TN + 1
        except:
            continue
    try:
        jaccard_score = TP / (TP + FP + FN)
    except:
        jaccard_score = 0
    return jaccard_score

jaccard_scores = {}
for key, value in meta[0].iteritems():
    print "jaccard score for " + key + ":"
    res = calculate_jaccard(meta, key, cluster_index, X.shape[0])
    jaccard_scores[key] = res

sorted_dict_view = sorted(jaccard_scores.items(), key=operator.itemgetter(1), reverse=True)

print sorted_dict_view
jaccard_file = open('jaccard_scores.txt', 'a')
for item in sorted_dict_view:
    print>> jaccard_file, item

plt.show()