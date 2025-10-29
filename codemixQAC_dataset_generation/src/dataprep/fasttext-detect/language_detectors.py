# Run langauge detector 
import fasttext

# Load the pre-trained language detection model

# Class
class Langdetect_Fasttext:
    def __init__(self):
        model_path = "../../models/fasttext/lid.176.bin"
        self.model = fasttext.load_model(model_path)
        self.k = 3
    
    def predict_lang(self,text):
        predictions = self.model.predict(text,self.k)
        return predictions
    
#class Langdetect_CLD3:
