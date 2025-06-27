#split data into blocks and generate graph
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
import pandas as pd
import json
import re
import ast
from tqdm import tqdm
from text2vec import SentenceModel
import requests
from datetime import datetime, timedelta, date

read_path="data/llm_result.csv"
save_dir="data/blocks"
start_time = '2022-01-01 00:00:00'
df=pd.read_csv(read_path)
df['time'] = pd.to_datetime(df['time'])
current_date =  datetime(2022, 2, 1)
i=1
# split data into blocks,each block contains 0-n blocks of records 
while current_date <=  datetime(2023, 1, 1):
    filtered_df = df[(df['time'] >= start_time) & (df['time'] < current_date)]
    
    filtered_df.to_csv(save_dir+"/blocks_{}.csv".format(i),index=False)

    try:
        next_date = current_date.replace(month=current_date.month + 1)
    except:
        next_date = datetime(2023, 1, 1)
    # Update the current date to the first day of the next month
    current_date = next_date 
    i+=1

# generate graph
save_path="data/urbanevent/raw"
node_list=[]
node_type_list=[]
id_list=[]
filtered_df_list=[]
for i in range(1,13):
    df=pd.read_csv("data/blocks/blocks_{}.csv".format(i))
    filtered_df_list.append(df)
filtered_df =pd.concat(filtered_df_list, ignore_index=True)
filtered_df = filtered_df.drop_duplicates(subset='id', keep='first', inplace=False)
for index,row in filtered_df.iterrows():
    id_list.append(row["id"])
    row_list=[]
    row_type_list=[]
    text=row["text"]
    class_text=row["class"]
    loc_entity=ast.literal_eval(row["loc_entity"])
    loc_entity_list=[]
    for entity in loc_entity:
        if entity["entity_type"] in ["事件位置","小区","组织机构","道路"]:
            loc_entity_list.append((entity["entity"],entity["entity_type"]))   
    event_entity=ast.literal_eval(row["entity"])
    event_entity_list=[]
    for entity in event_entity:
        if entity["entity_type"] in ["事件行为","事件结果","事件主体","事件原因"]:
            event_entity_list.append((entity["entity"],entity["entity_type"]))
    row_list.append(text)
    row_list.append(class_text)
    row_list.extend([entity[0] for entity in loc_entity_list])
    row_list.extend([entity[0] for entity in event_entity_list])
    node_list.append(row_list)

    row_type_list.append("text")
    row_type_list.append("class")
    row_type_list.extend([entity[1] for entity in loc_entity_list])
    row_type_list.extend([entity[1] for entity in event_entity_list])
    node_type_list.append(row_type_list)
with open(os.path.join(save_path,"urbanevent_graph_id.txt"),"w") as f:
    i=1
    # f.write("graphid,caseid"+"\n")
    for j,row in enumerate(node_list):
        f.write(str(i)+","+str(id_list[j])+"\n")
        i+=1
# Write the graph number to which each node belongs
with open(os.path.join(save_path,"urbanevent_graph_indicator.txt"),"w") as f:
    i=1
    for row in node_list:
        for entity in row:
            f.write(str(i)+"\n")
        i+=1
# Write the class number of each node
with open(os.path.join(save_path,"urbanevent_graph_labels.txt"),"w") as f:
    i=1
    for row in node_list:
        for entity in row:
            f.write(str(i)+"\n")
        i+=1
# Write all edges
with open(os.path.join(save_path,"urbanevent_A.txt"),"w") as f:
    i=1
    for row in node_list:
        temp=i
        i+=1
        text=row[0]
        for entity in row[1:]:
            f.write(str(temp)+","+str(i)+"\n")
            i+=1
# Write the labels of all edges 
type_dict={"class":1,"小区":2,"道路":3,"组织机构":4,"事件行为":5,"事件结果":6,"事件主体":7,"事件原因":8,"事件位置":9}
with open(os.path.join(save_path,"urbanevent_edge_labels.txt"),"w") as f:
    i=1
    for j,row in enumerate(node_list):
        temp=i
        i+=1
        text=row[0]
        for k,entity in enumerate(row[1:]):
            k=k+1
            type_label=type_dict[node_type_list[j][k]]
            f.write(str(type_label)+"\n")
            i+=1
# Write the embedding for each node
m = SentenceModel("shibing624/text2vec-base-chinese-sentence")
with open(os.path.join(save_path,"urbanevent_graph_embedding.txt"),"w") as f:
    for i,row in tqdm(enumerate(node_list),total=len(node_list)):
        for j,entity in enumerate(row):
                # continue
                f.write(str(m.encode(entity).tolist())+"\n")
print("read file...")
with open(os.path.join(save_path,"urbanevent_graph_embedding.txt"),"r") as f:
    lines=f.readlines()
embeddings=[]
for line in tqdm(lines):
    embeddings.append(ast.literal_eval(line.strip()))
with open(os.path.join(save_path,"urbanevent_node_attributes.txt"),"w") as f:
    for embedding in tqdm(embeddings):
        f.write(",".join(str(e) for e in embedding))
        f.write("\n")