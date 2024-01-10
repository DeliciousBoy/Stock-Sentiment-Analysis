# -*- coding: utf-8 -*-
"""Copy of nb_stock.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-Qy8Z3ksiwGVFdAhId5J0RSXw2ziOw-N
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()

import numpy as np
import re
import nltk.corpus
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense, Embedding,Flatten,LSTM,Bidirectional
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import RandomOverSampler
import seaborn as sns
import pickle

data=pd.read_excel("/content/drive/MyDrive/Colab Notebooks/5_stock_data.xlsx")
data

duplicated_values = data.duplicated().sum()
print( "Data Duplicated: ", duplicated_values)

missing_values = data.isna().sum()
print("Missing Values:")
print(missing_values)

data = data.drop_duplicates()
data

format = r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"
text = data['Text'].astype(str)

cleaned_texts = text.str.replace(format, "", regex=True)

print(cleaned_texts)

def convert_labels_to_binary(label):
    if label == -1:
        return 0
    elif label == 1:
        return 1
labels = data['Sentiment']
labels = [convert_labels_to_binary(label) for label in labels]
labels

stop = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

texts = cleaned_texts.values

def remove_stopwords(text):
    words = word_tokenize(text)
    cleaned_words = [word for word in words if word.lower() not in stop]
    lemmatized_words = [lemmatizer.lemmatize(word) for word in cleaned_words]
    return " ".join(lemmatized_words)

cleaned_stopw = [remove_stopwords(text) for text in texts]

print(cleaned_stopw)

print(cleaned_stopw)
print(labels)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(text)

oversampler = RandomOverSampler(sampling_strategy='minority')
X_resampled, y_resampled = oversampler.fit_resample(X, labels)
y = np.array(y_resampled )
y

X_train, X_test, y_train, y_test = train_test_split(X_resampled, y , test_size=0.2, random_state=42)

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)

confusion_mat = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(confusion_mat, annot=True, fmt='d', cmap='Blues', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.xlabel('True')
plt.ylabel('Predicted')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report:")
print(classification_report(y_test, y_pred))

new_text = "Monday's relative weakness. NYX WIN TIE TAP ICE INT BMC AON C CHK BIIB"
cleaned_new_text = re.sub(format, "", new_text)
cleaned_new_text = remove_stopwords(cleaned_new_text)

new_text_seq = vectorizer.transform([cleaned_new_text])
predictions = model.predict(new_text_seq)

predicted_label = 1 if predictions > 0.5 else 0
predicted_label

import joblib
filename = 'dnaive_bayes_model.pkl'
joblib.dump(model, open(filename,'wb'))

with open('dnaive_bayes_vectorizer.pkl', 'wb') as file:
    joblib.dump(vectorizer, file)