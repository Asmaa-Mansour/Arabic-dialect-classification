import re
import string
import nltk
from joblib import load
from flask import Flask, request, jsonify

app = Flask(__name__)


def delete_stop_words(mess):
    stop_words = set(nltk.corpus.stopwords.words("arabic"))
    return ' '.join(word for word in mess.split() if word not in stop_words and len(word)>1)



def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)


def remove_emojis(data):
    emoj = re.compile("["u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"  
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"  # chinese char
    u"\U00002702-\U000027B0"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u2640-\u2642" 
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"  # dingbats
    u"\u3030"
                        "]+" ,re.UNICODE)
    return re.sub(emoj, '', data)


def removeUnnecessarySpaces(text):
    return re.sub(r'[\n\t\ ]+', ' ', text)


def removeNonArabicChar(text):
    return re.sub(r'[^0-9\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD.0-9]+', ' ', text)


def processPost(text): 

    #Replace @username with empty string
    text = re.sub('@[^\s]+', ' ', text)
    
    # remove punctuations
    text= remove_punctuations(text)
    
    # normalize the tweet
    text= normalize_arabic(text)
    
    # remove repeated letters
    text=remove_repeating_char(text)

    text=remove_emojis(text)

    text = re.sub(r"\d+", "", text)

    text = re.sub('[a-zA-Z0-9_]|#|http\S+', '', text)
    text = removeUnnecessarySpaces(text)
    text = removeNonArabicChar(text)
    text = removeUnnecessarySpaces(text)
    
    return text


@app.route('/predict_api/',methods=['GET', 'POST'])
def predict_api():
    '''
    For rendering results as json and get input directly from url 
    '''
    #get data    
    txt = request.get_json()['txt']
    #preprocess data and predict
    txt = processPost(txt)
    print('[INFO]: Done preprocessing')
    predict = model.predict([txt])[0]
    print('[INFO]: Done predicting')
    return jsonify({"prediction": predict})

if __name__ == "__main__":
    model = load('ArabicDialects.joblib')
    nltk.download("stopwords") #arabic stopwords are not biult-in, so we find them by calling a set object
    arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
    english_punctuations = string.punctuation
    punctuations_list ='؟،~؛×÷'+ english_punctuations
    app.run(debug=True)