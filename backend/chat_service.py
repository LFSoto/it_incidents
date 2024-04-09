from flask import Flask, request, jsonify
from flask_cors import CORS
from enum import Enum
import joblib

app = Flask(__name__)
CORS(app)  # Enable CORS

model = joblib.load('../aimodel/it_problem_classifier.pkl')
vectorizer = joblib.load('../aimodel/vectorizer.pkl')

def issue_description_and_solution(issue):
    issues_map = {
        0: ("Hardware has malfunctioned.", "Please check the device's warranty and seek repairs."),
        1: ("A cable connection has been lost.", "Check all related cables and reconnect them."),
        2: ("The device driver is outdated.", "Update the driver software from the manufacturer's website."),
        3: ("Login credentials are incorrect.", "Reset or reconfigure your login credentials."),
        4: ("Required software plugin is not installed.", "Identify and install the necessary plugin."),
        5: ("Failed to update password.", "Attempt to change the password again or contact support."),
        6: ("The printer is malfunctioning.", "Check for paper jams, ink levels, or error messages on the printer."),
        7: ("The printer has run out of ink.", "Replace the ink cartridges."),
        8: ("The SAP server is currently down.", "Please wait until the server is back up or contact IT support."),
        9: ("Server is not responding.", "Check server status and restart if necessary."),
        10: ("A new service request is needed.", "Submit a service request form to IT support."),
        11: ("Network switch has failed.", "Inspect the switch and replace if necessary.")
    }
    print(issue)
    description, solution = issues_map.get(issue, ("Unknown issue.", "No solution available."))
    return f"Issue: {description} Solution: {solution}"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Transform the input using the loaded vectorizer
    transformed_input = vectorizer.transform([data['description']])
    prediction = model.predict(transformed_input)
    response_map = {label: description for description, label in enumerate(model.classes_)}
    response = response_map.get(prediction[0], "Unknown Issue")
    return jsonify(solution=issue_description_and_solution(response))

if __name__ == '__main__':
    app.run(debug=True)
