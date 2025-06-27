#clustering
import os
import pandas as pd
import torch
import numpy as np
from pyproj import Transformer
from incstdbscan.incrementaldbscan import IncrementalSTDBSCAN

save_path="data/urbanevent/raw"
embedding_save_path="model/GraphCL_embedding.pt"
embedding_list=torch.load(embedding_save_path)
with open(os.path.join(save_path,"urbanevent_graph_id.txt"),"r") as f:
    data=f.readlines()
embedding_dict={}
for line in data:
    graph_id,case_id=line.strip().split(",")
    embedding_dict[case_id]=int(graph_id)
for month in range(1,13):
    combined_dataframe =pd.read_csv("data/blocks/blocks_{}.csv".format(month))
    combined_dataframe_sorted = combined_dataframe.sort_values(by='time', ascending=True)

    embeddings=[]
    points=[]
    for index,row in combined_dataframe_sorted.iterrows():
        case_id=row["id"]
        graph_id=embedding_dict[str(case_id)]-1
        embedding=embedding_list[graph_id]
        embeddings.append(embedding)
        points.append((row['lat'],row['lon']))
        
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32649")
    pointstra=transformer.itransform(points)
    pointstra_list=[]
    for pt in pointstra:
        if np.isnan(pt[0]):
            pointstra_list.append((0.0,0.0))
        else:
            pointstra_list.append(pt)

    data=[]
    for embedding,(x,y) in zip(embeddings,pointstra_list):
        values_to_add=np.array([x,y])
        new_vector = np.append(embedding, values_to_add)
        data.append(new_vector)
    data=np.array(data)
    clusterer =IncrementalSTDBSCAN(eps=0.2,spatial_eps=5000, min_pts=2)
    clusterer.insert(X=data[:,:-2],points=data[:,-2:])
    labels = clusterer.get_cluster_labels(data[:,:-2],data[:,-2:]) 
    i=-1
    new_label=[]
    for label in labels:
        if label==-1:
            new_label.append(i)
            i-=1
        else:
            new_label.append(label)
    combined_dataframe_sorted['label']=new_label
    combined_dataframe_sorted.to_excel("data/saved/cluster_{}.xlsx".format(month), index=False, engine='openpyxl')