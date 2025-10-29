import pandas as pd
import os 
#from modules.language_detect.language_detectors import Langdetect_Fasttext
#from language_detectors import Langdetect_Fasttext
import fasttext
import json
from collections import defaultdict
from tqdm import tqdm 

# Load the pre-trained language detection model

# Class
class Langdetect_Fasttext:
    def __init__(self):
        #model_path = "models/fasttext/lid.176.bin"
        model_path = "/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/models/fasttext/lid.176.bin"
        self.model = fasttext.load_model(model_path)
        self.k = 3
    
    def predict_lang(self,text):
        predictions = self.model.predict(text,self.k)
        return predictions
    

from tqdm import tqdm 

if __name__ == "__main__":

    # Define path for msmarco and amazonshop
    #DATA_PATH = r"C:\Users\mehtarahul\OneDrive - Microsoft\Desktop\Research\codemixedQAS\datasets\raw\msmarco"
    DATA_PATH = "/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/datasets/msmarco"
    df = pd.read_csv(os.path.join(DATA_PATH,"queries_train.tsv"),sep="\t",header=None,usecols=[1,2])
    op_path = "/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/datasets/master/msmacro/fasttext"
    output_file = open(os.path.join(op_path,"msmarco_detect_train.jsonl"), 'w', encoding='utf-8')


    # DATA_PATH = "/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/datasets/amazon-kdd22-t2/data/processed/public/task_2_multiclass_product_classification"
    # df = pd.read_csv(os.path.join(DATA_PATH,"train-v0.3.csv"),usecols=[1,3])
    # op_path = "/Users/rahulmehta/Desktop/RESEARCH/QAS-codemix/datasets/master/amazonshop/fasttext"
    # output_file = open(os.path.join(op_path,"amazontask2_detect_train.jsonl"), 'w', encoding='utf-8')

    df.columns = ['query','query_locale']
    print(df.head(3))

    # Run detector on all queries
    lang_detect = Langdetect_Fasttext()
    print(lang_detect)
  

    queries = df['query'].tolist()
    queries = list(set(queries))

    print("Total queries:",len(queries))

    #pred_dict = defaultdict()
   
   
    for query in tqdm(queries):
        if isinstance(query,float) or '\n' in query :
            continue

        lang,scores = lang_detect.predict_lang(query)
        lang = list(lang)
        lang = [l.replace("__label__","")for l in lang] 

        #print(query,lang,scores)
        #pred_dict[query] = {'lang':list(lang),'scores':scores}
        output_file.write(json.dumps({"query": query, "lang": lang, "scores": scores.tolist()},ensure_ascii=False) + "\n")

    output_file.close()



