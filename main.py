
import igraph as ig
import leidenalg as la
import pandas as pd
from pprint import pprint

RES=1
# RES=0.01
# RES=0.001

data_files = {'bio_data_file':'./data/bio_50_000.csv'}

for filename, filepath in data_files.items():

    # get data from CSV file format
    data= pd.read_csv(filepath, low_memory=False)
    data_frame = pd.DataFrame(data, columns=['Source', 'Target'])

    G = ig.Graph.TupleList(data_frame.values, weights=False)

    partition = la.find_partition(G, la.CPMVertexPartition, resolution_parameter=RES)

    # to access graph cliques use `partition.graph.cliques()`
    print(f'{filename} Cliques : ')
    pprint(partition.graph.cliques())

    # print CPM value
    print(f'{filename} CPM of this partition: ', partition.q)

    pm = ig.Graph.community_leiden(G, objective_function="modularity", resolution=1)
    pm = la.find_partition(G, la.ModularityVertexPartition)
    print("Modularity of this partition: ", ig.Graph.modularity(G, pm), '\n')

    ig.plot(partition).save(f'{filename}-Leiden_with_CPM.png')

