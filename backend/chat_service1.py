from flask import Flask, request, jsonify
from flask_cors import CORS
from kanren import Relation, facts, run, var
import sqlite3
import random
import json
import joblib
import os
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)
model_directory = 'aiclassificator/model'  # Adjust this path as needed

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_directory)

# Load the model
model = AutoModelForQuestionAnswering.from_pretrained(model_directory)

# model = joblib.load('aiclassificator/it_problem_classifier.pkl')
vectorizer = joblib.load('aiclassificator/vectorizer.pkl')

def get_random_generic_from_json(isGreeting=None, isIntroduccion=None):
    with open("./backend/generics.json", 'r') as file:
        data = json.load(file)
    if isGreeting:
        return random.choice(data['greetings'])
    if isIntroduccion:
        return random.choice(data['introductions'])


def load_knowledge_base():
    error_solution = Relation() 
    conn = sqlite3.connect('./backend/database/it_support.db')
    cursor = conn.cursor()
    cursor.execute('SELECT error, solution FROM solutions')
    db_facts = cursor.fetchall()
    facts(error_solution, *db_facts)
    conn.close()
    return error_solution


def get_solution(error_message):
    error_solution = load_knowledge_base()
    solution = var()
    result = run(1, solution, error_solution(error_message.lower(), solution))
    if result:
        return get_random_generic_from_json(isIntroduccion=True) + result[0]
    else:
        return "No solution found for this error. Please contact IT support."


def get_prediction(data):
    description = data['description']

    # Encode the inputs using the tokenizer
    inputs = tokenizer(description, return_tensors="pt", padding=True, truncation=True)

    # Get model output
    with torch.no_grad():  # Turn off gradients for prediction
        outputs = model(**inputs)

    # Get the most likely start and end of answer
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

    # Convert logits to probabilities (not necessary but often useful)
    answer_start = torch.argmax(answer_start_scores)  # Index of max value
    answer_end = torch.argmax(answer_end_scores) + 1  # End index is exclusive

    # Debugging outputs
    print("Start index:", answer_start)
    print("End index:", answer_end)

    # Decode the predicted answer
    answer_tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end])
    answer = tokenizer.convert_tokens_to_string(answer_tokens)

    print("Decoded answer tokens:", answer_tokens)
    print("Final answer:", answer)

    return answer.strip().replace('"', '')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    if data['description'].lower() == 'hello' or data['description'].lower() == 'hi':
        response = jsonify(solution=get_random_generic_from_json(True))
    else:
        # Use new get_prediction function
        predicted_answer = get_prediction(data)
        response = jsonify(solution=predicted_answer)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True)
