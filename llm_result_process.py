# result process
import json
import os
import re
import pandas as pd

def find_last_comma(s):
    match = re.search(r',(?!.*,)', s)
    return match and match.start() + 1
def process(result):
    result_list=[]
    for index,row in result.iterrows():
        res=row["result"]
        res=res.replace(' ',"").replace('，',",")
        matches = re.findall(r'\[(.*?)\]', res)
        entity_result=[]
        for match in matches:
            _matches = match.split("),(")
            for _match in _matches:
                if "," not in _match:
                    # print("_match",_match,res)
                    continue
                last_comma_position = find_last_comma(_match)
                match_list=[_match[:last_comma_position-1],_match[last_comma_position:]]
                # match_list=_match.split(",")
                if len(match_list)%2==0:
                    for sing_match in match_list:
                        entity_result.append(sing_match.strip("(").strip(")").replace('"',"").replace("'",""))
                else:
                    print("res",res)
        entity_list=[]
        for i in range(0,len(entity_result),2):
            entity_list.append({'entity':entity_result[i], 'entity_type':entity_result[i+1]})
        # result_list.append({"id":row["id"],"text":row["text"],"class":sample["class"],"time":sample["time"],"entity":entity_list})
        result_list.append(entity_list)
    result["entity"]=result_list
    return result
event_path="data/event_result.csv"
loc_path="data/loc_result.csv"
event_result=pd.read_csv(event_path)
loc_result=pd.read_csv(loc_path)
event_result=process(event_result)
loc_result=process(loc_result)
loc_result["loc_entity"]=loc_result["entity"]
merged_df = pd.concat([event_result, loc_result[["loc_entity"]]], axis=1, join='inner')
merged_df.to_csv("./data/llm_result.csv",index=False)