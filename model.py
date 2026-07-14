import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load data
data = pd.read_csv("dataset.csv")

# Encode categorical data
le_skill = LabelEncoder()
le_interest = LabelEncoder()
le_career = LabelEncoder()

data['skills'] = le_skill.fit_transform(data['skills'])
data['interest'] = le_interest.fit_transform(data['interest'])
data['career'] = le_career.fit_transform(data['career'])

X = data[['skills', 'interest', 'marks']]
y = data['career']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save everything
pickle.dump((model, le_skill, le_interest, le_career), open("model.pkl", "wb"))

print("Model trained!")