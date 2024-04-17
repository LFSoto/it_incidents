from flask import Flask, request, jsonify
from flask_cors import CORS
from enum import Enum

app = Flask(__name__)
CORS(app)  # Enable CORS

from kanren import Relation, facts, run, var

# Crear una relación    
error_solution = Relation()

# Definir hechos (errores y soluciones)
facts(error_solution, 
      ("hardware malfunction", "check warranty and seek repairs"),
      ("cable connection lost", "check and reconnect cables"),
      ("device driver outdated", "update driver from manufacturer's website"),
      ("incorrect credentials are", "Reset or reconfigure your login credentials."),
      ("software plugin is not installed.", "Identify and install the necessary plugin."),
      ("failed to update password.", "Attempt to change the password again or contact support."),
      ("printer is malfunctioning.", "Check for paper jams, ink levels, or error messages on the printer."),
      ("printer has run out of ink.", "Replace the ink cartridges."),
      ("SAP server is currently down.", "Please wait until the server is back up or contact IT support."),
      ("server is not responding.", "Check server status and restart if necessary."),
      ("New service request is needed.", "Submit a service request form to IT support."),
      ("network switch has failed.", "Inspect the switch and replace if necessary.")
    )

# Función para consultar la solución a un error
def get_solution(error_message):
    # Variable lógica para la solución
    solution = var()
    
    # Realizar la consulta
    result = run(1, solution, error_solution(error_message, solution))
    
    # Retornar la solución si existe, de lo contrario indicar que no se encontró solución
    if result:
        return result[0]
    else:
        return "No solution found for this error. Please contact IT support."


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Transform the input using the loaded vectorizer
    print(data['description'])
    return jsonify(solution=get_solution(data['description']))

    # transformed_input = vectorizer.transform([data['description']])
    # prediction = model.predict(transformed_input)
    # response_map = {label: description for description, label in enumerate(model.classes_)}
    # response = response_map.get(prediction[0], "Unknown Issue")
    # return jsonify(solution=issue_description_and_solution(response))

if __name__ == '__main__':
    app.run(debug=True)
