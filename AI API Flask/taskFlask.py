from flask import Flask, request, jsonify
from groq import Groq
import json

client = Groq(api_key="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")

app = Flask(__name__)

@app.route('/ai/getAITasks', methods=['POST'])
def get_ai_tasks():
    # Obtener el texto de la solicitud
    data = request.get_json()
    print(data)



    # Devolver las tareas en formato JSON
    return jsonify({"tasks": tasks})

if __name__ == '__main__':
    app.run(debug=True)