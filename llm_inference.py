import os
#set Hugging Face mirror site
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from transformers import AutoTokenizer, AutoModel
import json
import csv
from tqdm import tqdm
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='chatGLM3-6b')
    parser.add_argument('-j', '--jsonl_path', default="data/loc_prompt_sample.jsonl", type=str)
    parser.add_argument('-s', '--save_path', default="data/loc_result.csv", type=str)
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True, device='cuda')
    model = model.eval()

    jsonl_path=args.jsonl_path
    ie_cases_list = []
    with open(jsonl_path,"r") as f:
        sample_list=[json.loads(line.strip()) for line in f.readlines()]
    for sample in sample_list:
        ie_cases={}
        ie_cases["id"]=sample["id"]
        ie_cases["text"]=sample["text"]
        ie_cases["input"]=sample["input"].replace("[input]","")
        ie_cases["class"]=sample["class"]
        ie_cases["time"]=sample["time"]
        ie_cases["lon"]=sample["lon"]
        ie_cases["lat"]=sample["lat"]
        ie_cases_list.append(ie_cases)
    ie_cases_list=ie_cases_list[:]

    result_list=[]

    file_name =args.save_path

    field_names = ["id","text","input","result","class","time","lon","lat"]
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

    for ie_cases in tqdm(ie_cases_list):
        instruction=ie_cases["input"]
        response, history = model.chat(tokenizer, instruction, history=[])  
        # print(response)
        ie_cases["result"]=response
        result_list.append(ie_cases)
        with open(file_name, 'a', newline='', encoding='utf-8') as file:
            csv_writer = csv.DictWriter(file, fieldnames=field_names)
            csv_writer.writerow(ie_cases)

