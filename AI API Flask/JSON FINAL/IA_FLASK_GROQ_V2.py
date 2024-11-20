from flask import Flask, request, jsonify
from groq import Groq
import json
import requests
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar Groq API key
groq_api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=groq_api_key)

# Inicializar Flask
app = Flask(__name__)

# Función para sanitizar el JSON
def sanitize_json(json_data):
    """
    Limpia las cadenas de texto en el JSON para evitar problemas de formato.
    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, str):
                json_data[key] = value.replace("\n", " ").strip()
            elif isinstance(value, dict):
                sanitize_json(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        sanitize_json(item)
    return json_data

@app.route('/ai/getAIRequirement', methods=['POST'])
def get_ai_requirement():
    # Obtener datos del request
    data = request.get_json()

    # Obtener el token Authorization desde los headers
    authorization_token = request.headers.get('Authorization')
    if not authorization_token:
        return jsonify({
            "error": "Authorization token is missing"
        }), 401

    # Convertir los datos a un string JSON válido
    data_as_string = '"' + json.dumps(data) + '"'

    # Llamar a la IA para generar el JSON
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                {
                    "Context": {
                        "Role": "Eres un experto en inteligencia artificial especializado en la creación de requerimientos para proyectos de software en el contexto de preventa. Solo debes generar un requerimiento claro, conciso y alineado con las mejores prácticas de la industria.",
                        "Instructions": "Cuando generes el JSON, asegúrate de que todas las cadenas sean válidas y no contengan saltos de línea no escapados. Las descripciones deben estar en una sola línea o usar '\\n' para representar saltos de línea. Respeta el orden del formato.",
                        "OutputFormat": {
                                            "ProjectID": 2,
                                            "OwnerID": 1,
                                            "RequirementDescription": "La aplicación móvil debe permitir a los clientes realizar pedidos de cemento de manera fácil y rápida, gestionar entregas y consultar facturas a través de una interfaz de usuario intuitiva y fácil de navegar.",
                                            "approved": false
                                        }
                    }
                }
                """
            },
            {
                "role": "user",
                "content": data_as_string
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.1,
        max_tokens=1024
    )

    # Obtener JSON generado por la IA
    ai_generated_json = json.loads(chat_completion.choices[0].message.content)

    # Sanitizar el JSON generado para evitar problemas de formato
    ai_generated_json = sanitize_json(ai_generated_json)

    # Log de los datos enviados
    print("Enviando JSON al backend:", ai_generated_json)
    print("Enviando encabezado Authorization:", authorization_token)

    # Realizar el POST al backend con el token dinámico
    try:
        response = requests.post(
            "http://localhost:8080/createRequirement",
            json=ai_generated_json,
            headers={"Authorization": authorization_token}
        )
        response.raise_for_status()

        # Respuesta del backend
        return jsonify({
            "ai_generated_json": ai_generated_json,
            "backend_response": response.json()
        })
    except requests.exceptions.RequestException as e:
        # Manejo de errores
        return jsonify({
            "error": "Failed to send data to backend.",
            "details": str(e),
            "ai_generated_json": ai_generated_json
        }), 500



@app.route('/ai/getAITasks', methods=['POST'])
def get_ai_tasks():
    data = request.get_json()

    # Convertir el diccionario a un JSON *string* con comillas
    data_as_string = '"' + json.dumps(data) + '"'

    # Responder con el *string*
    jsonify({"data": data_as_string})
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """{
                    "Context": {
                        "Role": "Eres un experto en inteligencia artificial que está ayudando con la preventa de software para una empresa. Tienes conocimiento sobre historias de usuario, requisitos funcionales y no funcionales, estimación de esfuerzo, generación de propuestas y dependencias de tareas.",
                        "Instructions": "Cuando se te proporcione un JSON que contenga información sobre una empresa, proyecto y requerimientos, debes generar una lista de tareas con su ID, nombre, descripción, área de equipo responsable, tiempo estimado y costo en formato JSON. Responde solo con el JSON de las tareas, sin añadir nada extra.",
                        "InputFormat": "Envía tus JSON de la siguiente manera: \n\n { \n \"Company\": { \n \"CompanyName\": \"Nombre de la Empresa\", \n \"CompanyDescription\": \"Breve descripción de la empresa\", \n \"CompanyDetails\": { \n \"Industry\": \"Sector de la empresa\", \n \"Location\": \"Ubicación de la empresa\", \n \"Size\": \"Tamaño de la empresa\" \n } \n }, \n \"Project\": { \n \"ProjectName\": \"Nombre del proyecto\", \n \"ProjectDescription\": \"Descripción general del proyecto\", \n \"ProjectDetails\": { \n \"Budget\": \"Presupuesto disponible\", \n \"Deadline\": \"Fecha límite\", \n \"ProjectManager\": \"Nombre del gerente del proyecto\" \n } \n }, \n \"Requirements\": [ \n { \n \"RequirementID\": \"ID del requerimiento 1\", \n \"RequirementDescription\": \"Descripción del requerimiento 1\" \n }, \n { \n \"RequirementID\": \"ID del requerimiento 2\", \n \"RequirementDescription\": \"Descripción del requerimiento 2\" \n } \n ] \n } \n\n La respuesta debe ser en este formato: \n\n { \n \"Tasks\": [ \n { \n \"TaskID\": \"ID de la tarea 1\", \n \"TaskName\": \"Nombre de la tarea 1\", \n \"TaskDescription\": \"Descripción de la tarea 1\", \n \"TeamArea\": \"Área del equipo responsable\", \n \"Time\": \"Tiempo estimado\", \n \"Cost\": \"Costo estimado\" \n }, \n { \n \"TaskID\": \"ID de la tarea 2\", \n \"TaskName\": \"Nombre de la tarea 2\", \n \"TaskDescription\": \"Descripción de la tarea 2\", \n \"TeamArea\": \"Área del equipo responsable\", \n \"Time\": \"Tiempo estimado\", \n \"Cost\": \"Costo estimado\" \n } \n ] \n }
                        """
            },
            {
                "role": "user",
                "content": data_as_string
                ,
            }
        ],
        model="llama-3.1-70b-versatile",  
        temperature=0.1,
        max_tokens=1024,
    )

    return(chat_completion.choices[0].message.content)



if __name__ == "__main__":
    app.run(debug=True)
