from flask import Flask, request, jsonify
from flask_cors import CORS
from kanren import Relation, facts, run, var
import sqlite3
import random

app = Flask(__name__)
CORS(app)

error_solution = Relation()

def get_response_introduction():
    response_introductions = [
        "Thank you for sharing that, please try to ",
        "Alright, to address this issue, you should ",
        "I understand your concern, you might want to ",
        "Thank you for your patience, I suggest you ",
        "Let's sort this out, you could ",
        "I appreciate your details, it's best to ",
        "That's a good point, you may want to ",
        "Thank you for pointing that out, kindly ",
        "I see what you mean, it would be a good idea to ",
        "Thanks for explaining, I recommend you ",
        "That sounds challenging, perhaps you can ",
        "Got it, let’s try to ",
        "I can help with that, you might consider ",
        "Indeed, a suitable approach would be to ",
        "Certainly, an effective solution would be to "
    ]
    return random.choice(response_introductions)

def load_knowledge_base():
    conn = sqlite3.connect('it_support.db')
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
        return get_response_introduction() + result[0]
    else:
        return "No solution found for this error. Please contact IT support."


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    return jsonify(solution=get_solution(data['description']))

if __name__ == '__main__':
    app.run(debug=True)
