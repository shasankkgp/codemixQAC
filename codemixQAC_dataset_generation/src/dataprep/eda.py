from collections import defaultdict
import pycountry
import json
import csv
import os 
def get_language_name(code):
    language = pycountry.languages.get(alpha_2=code)
    return language.name if language else code

def lang_counter(all_lst):
    lang_count = defaultdict(int)
    lang_eg = defaultdict(list)
    size_count = defaultdict(int)
    
    for lang in all_lst:
        # if len(lang['lang']) > 1 and "en" not in lang['lang']:
        land_set = "-".join({get_language_name(ln) for ln in set(lang['lang'])})
        lang_eg[land_set].append(lang['query'])
        lang_count[land_set] += 1
        size_count[len(set(lang['lang']))] += 1
    
    return lang_count, lang_eg, size_count


if __name__ == "__main__":
    
    #path_json = "lang_lst_train.jsonl"
    # Enter your input file path

    #input_file = "amazontask2_detect_train.jsonl"

    path_json = ""
    input_file = "msmarco_detect_train.jsonl"

    op_file = input_file.split(".")[0]
    with open(os.path.join(path_json,input_file), 'r',encoding='utf-8') as f:
        lang_lst_train = [json.loads(line) for line in f]
    
    lang_count, lang_eg, size_count = lang_counter(lang_lst_train)
    
    # save the results as json lines

    with open(os.path.join(path_json,op_file+"_lang_count.csv"), 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['lang', 'count']  # Replace with your actual JSON keys
        csv_writer.writerow(header)
        for k, v in lang_count.items():
            csv_writer.writerow([k, v])  
    
    with open(os.path.join(path_json,op_file+"_lang_eg.csv"), 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['lang', 'eg']  # Replace with your actual JSON keys
        csv_writer.writerow(header)
        for k, v in lang_eg.items():
            csv_writer.writerow([k, v])  

    with open(os.path.join(path_json,op_file+"_lang_size_count.csv"), 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['lang', 'count']  # Replace with your actual JSON keys
        csv_writer.writerow(header)
        for k, v in lang_count.items():
            csv_writer.writerow([k, v]) 

        