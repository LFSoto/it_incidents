from flask import Flask, request, jsonify
from flask_cors import CORS
from kanren import Relation, facts, run, var
import sqlite3
import random
import json
import joblib
import os
import openai
from openai import OpenAI

app = Flask(__name__)
CORS(app)

model = joblib.load('aiclassificator/it_problem_classifier.pkl')
vectorizer = joblib.load('aiclassificator/vectorizer.pkl')
client = OpenAI(
    # On CMD setx OPENAI_API_KEY "your-api-key-here"
    api_key=os.environ.get("OPENAI_API_KEY"),
)

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
    data = request.get_json(force=True)
    transformed_input = vectorizer.transform([data['description']])
    prediction = model.predict(transformed_input)
    return prediction[0].strip().replace('"','')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    if data['description'].lower() == 'hello' or data['description'].lower() == 'hi':
        response = jsonify(solution=get_random_generic_from_json(True))
    else:
        response = jsonify(solution=get_solution(get_prediction(data)))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/gpt', methods=['POST'])
def gpt():
    data = request.get_json(force=True)
    prompt = data['description']

    try:
        messages = [
                {"role": "user", "content": prompt},
            ]
        response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
        formated = {
            "content": response.choices[0].message.content
        }
        return jsonify(formated), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
