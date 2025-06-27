# IDUED
## LLM-based event graph construction
Input construction
``` bash
python prompt_event.py
python prompt_location.py
```
LLMs inference
``` bash
python llm_inference.py --jsonl_path data/event_prompt_sample.jsonl --save_path data/event_result.csv
python llm_inference.py --jsonl_path data/loc_prompt_sample.jsonl --save_path data/loc_result.csv
python llm_result_process.py
```

## Event graph contrastive learning
Graph construction
``` bash
python event_graph_construct.py
```
Train
``` bash
python event_graph_train.py
```
Extract
```
python event_graph_extract.py
```
## Incremental daily urban event detection
clustering
``` bash
python event_detection.py
```