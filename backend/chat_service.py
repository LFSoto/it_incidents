from flask import Flask, request, jsonify
from flask_cors import CORS
from kanren import Relation, facts, run, var
import sqlite3
import random
import json
import joblib

app = Flask(__name__)
CORS(app)
error_solution = Relation()

model = joblib.load('../aiclassificator/it_problem_classifier.pkl')
vectorizer = joblib.load('../aiclassificator/vectorizer.pkl')


def get_random_generic_from_json(isGreeting=None, isIntroduccion=None):
    with open("./generics.json", 'r') as file:
        data = json.load(file)
    if isGreeting:
        return random.choice(data['greetings'])
    if isIntroduccion:
        return random.choice(data['introductions'])


def load_knowledge_base():
    conn = sqlite3.connect('it_support.db')
    cursor = conn.cursor()
    cursor.execute('SELECT error, solution FROM solutions')
    db_facts = cursor.fetchall()
    facts(error_solution, *db_facts)
    conn.close()
    return error_solution


def get_solution(error_message):
    if error_message.lower() == 'hello' or error_message.lower() == 'hi':
        return get_random_generic_from_json(True)
    error_solution = load_knowledge_base()
    solution = var()
    result = run(1, solution, error_solution(error_message.lower(), solution))
    if result:
        return get_random_generic_from_json(isIntroduccion=True) + result[0]
    else:
        return "No solution found for this error. Please contact IT support."


@app.route('/predict', methods=['POST'])
def predict():
    # Transform the input using the loaded vectorizer
    transformed_input = vectorizer.transform([data['description']])
    prediction = model.predict(transformed_input)
    print(prediction[0])
    data = request.get_json(force=True)
    return jsonify(solution=get_solution(data['description']))

if __name__ == '__main__':
    app.run(debug=True)
