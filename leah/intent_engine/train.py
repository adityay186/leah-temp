import json
import nltk
import joblib
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load the data from the JSON file
with open('data/intents.json', 'r') as f:
    intents = json.load(f)['intents']

# Tokenize and lemmatize the patterns, and create numerical features using TF-IDF vectorization
lemmatizer = WordNetLemmatizer()
tokens = []
labels = []
for intent in intents:
    for pattern in intent['patterns']:
        words = nltk.word_tokenize(pattern.lower())
        words = [lemmatizer.lemmatize(word) for word in words]
        tokens.append(' '.join(words))
        labels.append(intent['tag'])
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(tokens)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.1)

# Train a logistic regression classifier
clf = LogisticRegression()
clf.fit(X_train, y_train)

# Save the model as a joblib file
joblib.dump((clf, vectorizer), 'saved_model/model.joblib')