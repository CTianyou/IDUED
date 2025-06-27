#generate location prompt
import json
import random
from tqdm import tqdm
import ast
temp_path="data/loc_template.json"
sample_path="data/sample.jsonl"
save_path="data/loc_prompt_sample.jsonl"
temp=json.load(open(temp_path, 'r'))
prompt_list=temp["zh"]["template"]
with open(sample_path,'r') as f:
    sample_list=[json.loads(line.strip()) for line in f.readlines()]
result_list=[]
example="""例如
输入：昨晚大雨，马沧湖路又淹水了，外面大雨家里滴雨，走道都是积水无法行走，
输出：[(马沧湖路,事件位置),(马沧湖路,道路)]
输入：盘龙城汤云海路兰江公园里门前市政路每次下暴雨都积水严重，小区居民出行艰难。
输出：[(盘龙城汤云海路兰江公园里门前市政路,事件位置),(汤云海路,道路),(兰江公园里门前市政路,道路)]
输入：光谷188小区一期门前的，高科园西路与神墩一路交汇口路面积水严重。
输出：[(光谷188小区一期门前的，高科园西路与神墩一路交汇口,事件位置),(光谷188小区一期,小区),(高科园西路,道路),(神墩一路,道路)]
输入：直接给武汉市人民政府 , 摩卡小镇北门一到下雨就淹水。
输出：[(摩卡小镇北门,事件位置),(武汉市人民政府,组织机构),(摩卡小镇北门,小区)]
"""

for sample in tqdm(sample_list):
    i=random.randint(0,19)
    prompt=prompt_list[str(i)].format(s_format="[(实体,实体类型)]",s_schema="[事件位置,小区,组织机构,道路]")
    text_sample=sample["text"]
    input=prompt+example+"[input]"+"输入："+text_sample+"\n输出："

    result_list.append({"id":sample["id"],"text":sample["text"],"input":input,"class":sample["class"],"time":sample["time"],"lon":sample["lon"],"lat":sample["lat"]})
with open(save_path,'w', encoding='utf-8') as f:
    for result in result_list:
        jsonl=json.dumps(result,ensure_ascii=False)
        f.write(jsonl+"\n")