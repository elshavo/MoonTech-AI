from flask import Flask, request, jsonify
from groq import Groq
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Obtener la API key desde el entorno
groq_api_key = os.getenv('GROQ_API_KEY')

# Inicializar el cliente Groq con la API key
client = Groq(api_key=groq_api_key)

app = Flask(__name__)
client = Groq(api_key=groq_api_key)


@app.route('/ai/getAIRequirements', methods=['POST'])
def get_ai_requirements():
    data = request.get_json()

    # Convertir el diccionario a un JSON *string* con comillas
    data_as_string = '"' + json.dumps(data) + '"'

    # Responder con el *string*
    jsonify({"data": data_as_string})
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": 
                """
                {
                "Context": {
                    "Role": "Eres un experto en inteligencia artificial especializado en la ingeniería de requerimientos para proyectos de software en el contexto de preventa. Tienes amplio conocimiento sobre la recopilación y análisis de requisitos funcionales y no funcionales, estimación de tiempos y esfuerzos, prioridades, y estándares como IEEE 830 y UML. Tu objetivo es ayudar a generar requerimientos claros, concisos y detallados, asegurando que sean técnicamente viables y alineados con los objetivos del negocio y las mejores prácticas de la industria.",
                    "Instructions": "Cuando se te proporcione un JSON que contenga información sobre una empresa, un proyecto y una transcripción de una reunión, debes generar una lista de requerimientos funcionales y no funcionales en formato JSON. Responde solo con el JSON de los requerimientos, sin añadir nada extra.",
                    "InputFormat": "Envía el JSON en este formato: \n\n { \n "Company": { \n "CompanyName": "Nombre de la Empresa", \n "CompanyDescription": "Breve descripción de la empresa", \n "CompanyDetails": { \n "Industry": "Sector de la empresa", \n "Location": "Ubicación de la empresa", \n "Size": "Tamaño de la empresa" \n } \n }, \n "Project": { \n "ProjectName": "Nombre del proyecto", \n "ProjectDescription": "Descripción general del proyecto", \n "ProjectDetails": { \n "Budget": "Presupuesto disponible", \n "Deadline": "Fecha límite", \n "ProjectManager": "Nombre del gerente del proyecto" \n } \n }, \n "Requirements": \n { \n \"RequirementID\": \"ID del requerimiento 1\", \n \"RequirementDescription\": \"Descripción del requerimiento 1\" \n }, \n { \n \"RequirementID\": \"ID del requerimiento 2\", \n \"RequirementDescription\": \"Descripción del requerimiento 2\" \n } \n, \n "Transcript": "Texto de la transcripción aquí" 
                        }
                    }
                }
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
