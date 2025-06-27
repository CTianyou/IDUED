#generate evet prompt
import re
import json
import random
from tqdm import tqdm
temp_path="./data/event_template.json"
sample_path="./data/sample.jsonl"
save_path="./data/event_prompt_sample.jsonl"

example="""例如
输入：中建壹品澜郡小区春节到了，物业收取业主们的装修建筑垃圾清理费每平方十元，现在快春节了小区里的建筑垃圾堆积如山。
输出：[(建筑垃圾,事件主体),(中建壹品澜郡小区 ,事件地点),(堆积如山,事件行为)]
输入：青山区厂前街铁路山菜场对面中通快递旁边，有一棵树断了，压到了电线，存在安全隐患，请核实处理。
输出：[(青山区厂前街铁路山菜场对面中通快递 ,事件地点),(树,事件主体),(断了,事件行为),(压到了电线,事件结果)]
输入：洪山区八叠山公墓的男女公厕没人清理，非常脏，而且没有自来水，有损武汉城市形象和市民感受，请有关部门督促解决。
输出：[(洪山区八叠山公墓, 事件地点), (男女公厕, 事件主体), (没人清理, 事件行为), (非常脏, 事件结果), (没有自来水, 事件结果), (有损武汉城市形象和市民感受, 事件原因)]
"""

eet_temp=json.load(open(temp_path, 'r'))
prompt_list=eet_temp["zh"]["template"]
with open(sample_path,'r') as f:
    sample_list=[json.loads(line.strip()) for line in f.readlines()]

result_list=[]
for sample in tqdm(sample_list):
    i=random.randint(0,19)
    prompt=prompt_list[str(i)].format(s_format="[(事件触发词,事件类型)]",s_schema="[事件主体,事件行为,事件结果,事件原因,事件地点]")
    input=prompt+example+"[input]"+"输入："+sample["text"]+"\n输出："
    result_list.append({"id":sample["id"],"text":sample["text"],"input":input,"class":sample["class"],"time":sample["time"],"lon":sample["lon"],"lat":sample["lat"]})

with open(save_path,'w', encoding='utf-8') as f:
    for result in result_list:
        jsonl=json.dumps(result,ensure_ascii=False)
        f.write(jsonl+"\n")