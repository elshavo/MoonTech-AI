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
                                "InputFormat": "Envía el JSON en este formato:\n\n{\n    \"Company\": {\n        \"CompanyName\": \"company_name\",\n        \"CompanyDescription\": \"company_description\",\n        \"CompanyDetails\": {\n            \"Industry\": \"industry\",\n            \"Location\": \"location\",\n            \"Size\": \"size\"\n        }\n    },\n    \"Project\": {\n        \"ProjectName\": \"project_name\",\n        \"ProjectDescription\": \"project_description\",\n        \"ProjectDetails\": {\n            \"Budget\": \"budget\",\n            \"ProjectManager\": \"project_manager\"\n        }\n    },\n    \"Requirements\": [\n        {\n            \"RequirementID\": \"REQ-001\",\n            \"RequirementDescription\": \"requirement_1\",\n            \"Owner\": \"Owner_1\"\n        },\n        {\n            \"RequirementID\": \"REQ-002\",\n            \"RequirementDescription\": \"requirement_2\",\n            \"Owner\": \"Owner_2\"\n        },\n        {\n            \"RequirementID\": \"REQ-003\",\n            \"RequirementDescription\": \"requirement_3\",\n            \"Owner\": \"Owner_3\"\n        }\n    ],\n    \"Transcript\": \"transcript\"\n}"
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
                        "Instructions": "Cuando se te proporcione un JSON que contenga información sobre una empresa, proyecto, requerimientos y tareas, debes generar una lista de tareas con su ID y descripción en formato JSON. Responde solo con el JSON de las tareas, sin añadir nada extra.",
                        "InputFormat": "Envía tus JSON de la siguiente manera:\n\n{\n    \"Company\": {\n        \"CompanyName\": \"company_name\",\n        \"CompanyDescription\": \"company_description\",\n        \"CompanyDetails\": {\n            \"Industry\": \"industry\",\n            \"Location\": \"location\",\n            \"Size\": \"size\"\n        }\n    },\n    \"Project\": {\n        \"ProjectName\": \"project_name\",\n        \"ProjectDescription\": \"project_description\",\n        \"ProjectDetails\": {\n            \"Budget\": \"budget\",\n            \"ProjectManager\": \"project_manager\"\n        }\n    },\n    \"Requirements\": [\n        {\n            \"RequirementID\": \"REQ-001\",\n            \"RequirementDescription\": \"requirement_1\",\n            \"Owner\": \"Owner_1\"\n        },\n        {\n            \"RequirementID\": \"REQ-002\",\n            \"RequirementDescription\": \"requirement_2\",\n            \"Owner\": \"Owner_2\"\n        },\n        {\n            \"RequirementID\": \"REQ-003\",\n            \"RequirementDescription\": \"requirement_3\",\n            \"Owner\": \"Owner_3\"\n        }\n    ],\n    \"Transcript\": \"transcript\",\n    \"Tasks\": [\n        {\n            \"TaskID\": \"T-001\",\n            \"TaskDescription\": \"task_1\"\n        },\n        {\n            \"TaskID\": \"T-002\",\n            \"TaskDescription\": \"task_2\"\n        },\n        {\n            \"TaskID\": \"T-003\",\n            \"TaskDescription\": \"task_3\"\n        }\n    ]\n}"
                }"""
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
