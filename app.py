import json
import pickle
import random
import numpy as np
from flask import Flask , render_template , request , jsonify
from keras.models import load_model
from flask_sqlalchemy import SQLAlchemy
import nltk
nltk.download('wordnet')
# nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
app = Flask(__name__)
lm=WordNetLemmatizer()
model=load_model(r'static\model.h5',compile=False)
words = pickle.load(open(r'static\wordsqqq.pkl','rb'))
dataset=json.load(open(r'static\dataset.json','rb'))
cls = pickle.load(open(r'static\classes.pkl','rb'))

def clean_text(text):
  tokens = nltk.word_tokenize(text)
  tokens = [lm.lemmatize(word) for word in tokens]
  return tokens
def css():
    return render_template('static\style2.css')
# def bag_of_words(text, vocab):
#   tokens = clean_text(text)

def bag_of_words(sentence):
   sentence_words=clean_text(sentence)
   bag=[0]*len(words)
   for w in  sentence_words:
     for i,word in enumerate(words):
       if word==w:
         bag[i]=1
     return np.array(bag)

def predict_class(sentence):
  bow=bag_of_words(sentence)
  res=model.predict(np.array([bow]))[0]
  er=0.25
  results=[[i,r] for i,r in enumerate(res) if r> er]
  results.sort(key=lambda x:x[1],reverse=True)
  return_list=[]
  for r in results:
    return_list.append({'intent':cls[r[0]],'probability':str(r[1])})
  return return_list

def get_response(intents_list,intents_json):
  tag=intents_list[0]['intent']
  list_of_intents=intents_json['intents']
  result='data not found'
  for i in list_of_intents:
    if i['tag']==tag:
      result=random.choice(i['responses'])
      break
  return result

# while True:
#     msg=input("Enter your message: ")
#     clas=predict_class(msg)
#     answer=get_response(clas,dataset)
#     print(answer)

# @app.route('/'):
# def refresh():
#     print("Hello")
#     if request.method=='POST':
#         # answer
#
#     return render_template("index.html")
#
# @app.route('/predict',methods=['POST','GET'])
# def predict():
#     pass
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict():

    userMsg=request.get_json().get('message')
    print(userMsg)
    class_output=predict_class(userMsg)
    respond=get_response(class_output,dataset)
    # create json/ dictionary so that
    msg={'answer':respond}
    print(msg)
    return jsonify(msg)




if __name__ =="__main__":
    app.run(debug=True)