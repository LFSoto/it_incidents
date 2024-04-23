import pandas as pd
import nltk
import random
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def synonym_replacement(sentence, n=1):
    words = sentence.split()
    random_words = list(set([word for word in words if word not in nltk.corpus.stopwords.words('english')]))
    random.shuffle(random_words)
    num_replaced = 0
    for random_word in random_words:
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            words = [synonym if word == random_word else word for word in words]
            num_replaced += 1
        if num_replaced >= n:  # only replace up to n words
            break

    return ' '.join(words)

def augment_data(dataframe, augment_func, num_augments=1):
    augmented_rows = []
    for _, row in dataframe.iterrows():
        for _ in range(num_augments):
            new_row = row.copy()
            new_row['description'] = augment_func(row['description'])
            new_row['caller'] = row['caller']
            new_row['issue'] = row['issue']
            augmented_rows.append(new_row)
    return pd.DataFrame(augmented_rows)


# Load data
df = pd.read_csv('aiclassificator/incidents_database.csv')
df['description'] = df['description'].astype(str)
df['caller'] = df['caller'].astype(str)
df['issue'] = df['issue'].astype(str)

augmented_df = augment_data(df, synonym_replacement, num_augments=3)  # Adjust num_augments as needed

df = pd.concat([df, augmented_df]).reset_index(drop=True)

# Display the first few rows of the dataframe
df = pd.read_csv('aiclassificator/augmented_dataset.csv')
print(df.head())
df.to_csv('aiclassificator/augmented_dataset.csv', index=False)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)

# Fit and transform the descriptions into a feature matrix
X = vectorizer.fit_transform(df['description'])

# Target variable
y = df['issue']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Initialize and train the RandomForestClassifier
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Print the classification report
print(classification_report(y_test, y_pred))

# Generate the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plotting using seaborn for better visualization
plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

# Save the model
joblib.dump(model, 'aiclassificator/it_problem_classifier.pkl')

# Save the vectorizer
joblib.dump(vectorizer, 'aiclassificator/vectorizer.pkl')
