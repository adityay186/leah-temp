import json
import nltk
import joblib
import numpy as np

class IntentRecogniser:
    
    def __init__(self):
        # Load the intents from the JSON file
        with open('data/intents.json', 'r') as f:
            self.intents = json.load(f)['intents']

        # Load the trained model from the joblib file
        self.clf, self.vectorizer = joblib.load('saved_model/model.joblib')
    
    def predict(self, text):
        # Get the user's input text and preprocess it
        lemmatizer = nltk.stem.WordNetLemmatizer()
        words = nltk.word_tokenize(text.lower())
        words = [lemmatizer.lemmatize(word) for word in words]

        # Convert the user's input into numerical features using TF-IDF vectorization
        input_features = self.vectorizer.transform([' '.join(words)])

        # Use the trained classifier to predict the intent of the user's input
        predictions = self.clf.predict(input_features)

        # Print the predicted intent and a random response from the intent
        for intent in self.intents:
            if intent['tag'] == predictions[0]:
                return {'tag': predictions[0], 'response': np.random.choice(intent['responses'])}

print(IntentRecogniser().predict("hello"))
