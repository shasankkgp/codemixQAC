import pandas as pd 
import os 
import json
from tqdm import tqdm 
from collections import defaultdict,Counter
#import ijson

if __name__ == "__main__":

    # Read dataset
    # master -> msmarco -> fasttext/cld3
    # dataset = "amazonshop"
    # fl_name = "amazontask2_detect_train.jsonl"
    # fl_en_name = "amazontask2_detect_train_en.jsonl"
    
    dataset = "msmarco"  
    fl_name = "msmarco_detect_train.jsonl"
    fl_en_name = "msmarco_detect_train_en.jsonl"
    ft_path = f"/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/datasets/master/{dataset}/fasttext"
    cld_path = f"/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/datasets/master/{dataset}/cld3"
    ld_path = f"/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/datasets/master/{dataset}/langdetect" # change to langdetect
    op_path = f"/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/datasets/master-voted-1/{dataset}"
    lang_dict = {}

    # map query -> key 
    # Create master dict using Fasttext
    with open(os.path.join(ft_path,fl_name), "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
        #for line in tqdm(ijson.items(file,'item')):
            record = json.loads(line)  # Parse each line as JSON
            query = record['query']
            lang = record['lang']
            scores = record['scores']
            lang_dict[query] = {'lang_ft':lang,'scores_ft':scores}  # Store in dictionary with line number as key
    #print(lang_dict['accesorios para garmin fenix 5x'])
    print("created lang_dict of size",len(lang_dict))

    # Add CLD3
    
    with open(os.path.join(cld_path,fl_name), "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            print(i)
            record = json.loads(line)
            if record['query'] in lang_dict:
                lang_dict[record['query']]['lang_cd'] = record['lang']
                lang_dict[record['query']]['scores_cd'] = record['scores']
    print("added cld3")


    # Add langdetect - use cld3 currently and replace with fasttext
    
    with open(os.path.join(ld_path,fl_name), "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            print(i)
            record = json.loads(line)
            if record['query'] in lang_dict:
                lang_dict[record['query']]['lang_ld'] = record['lang']
                lang_dict[record['query']]['scores_ld'] = record['scores']
    print("added fasttext")

    # Majority vote of 2 
    #print(lang_dict['accesorios para garmin fenix 5x'])

    # Iterate dictionary
    cmix_mdict = {}
    en_mdict = {}

    c = 0 
    # If there is any language that is detected in 2 detectors, consider it as a common language
    for k,v in tqdm(lang_dict.items(),desc="preparing majority vote based master data"):
        #print(k,v)
        #c+=1
        # if c>5:
        #     break
        all_langs = v['lang_ft']  + v['lang_cd'] + v['lang_ld']
        lang_counter = dict(Counter(all_langs))

        # Filter if language is in 2 detector
        #print(lang_counter)
        lang_counter_gt1 =  {k: v for k,v in lang_counter.items() if v > 1}
        
        # and more than 1 langauge detected
        if len(lang_counter_gt1) > 1:
            #print(k,v,lang_counter_gt1)
            cmix_mdict[k] = v
            cmix_mdict[k]['lang_voted'] = [lang for lang,v in lang_counter_gt1.items()]

        # English only queries and atleast 2 detectors
        #print(lang_counter)
        if lang_counter.get('en', 0) > 1 and all(count < 2 for key, count in lang_counter.items() if key != 'en'):
            en_mdict[k] = v   
            en_mdict[k]['lang_voted'] = ['en']
            #print(lang_counter)
        #elif all(count < 2 for key, count in lang_counter.items() if key != 'en')

    # Write as master file 
    print("code mix dataset size: ",len(cmix_mdict))
    with open(os.path.join(op_path,fl_name), "w", encoding="utf-8") as f:
        f.write(json.dumps(cmix_mdict,ensure_ascii=False) + "\n")
    print("file written",os.path.join(op_path,fl_name))

    # Get en only dataset for synthetic data generation
    print("en only dataset size: ",len(en_mdict))
    with open(os.path.join(op_path,fl_en_name), "w", encoding="utf-8") as f:
        f.write(json.dumps(en_mdict,ensure_ascii=False) + "\n")
    print("file written en",os.path.join(op_path,fl_en_name))





