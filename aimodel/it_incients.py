import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv('Incidents_Test_Database.csv')

# Display the first few rows of the dataframe
print(df.head())

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)

# Fit and transform the descriptions into a feature matrix
X = vectorizer.fit_transform(df['description'])

# Target variable
y = df['label']


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Initialize and train the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Print the classification report
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'it_problem_classifier.pkl')

# Save the vectorizer
joblib.dump(vectorizer, 'vectorizer.pkl')
