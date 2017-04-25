"""

An example hierarchical clustering by using the OutputGenerator

"""

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from OutputGenerator import OutputGenerator
PATH = "./GMQLData/pietro_query_full/files"




desired_columns = ['gene_symbol','count_GENES_PATIENTS']
o = OutputGenerator(PATH)
schema_file = o._get_file("schema")
o.read_all(PATH,schema_file,desired_columns)
print o.data.head(3)
o.to_matrix('count_GENES_PATIENTS','gene_symbol')
o.remove_zeros()
print o.data.shape
X = o.data.values.transpose()
print X.shape

# perform hierarchical clustering
Z = linkage(X, 'ward')

# calculate full dendrogram
plt.figure()
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.  # rotates the x axis labels
)
plt.show()

