from flask import Flask, request, jsonify
from groq import Groq
import json

app = Flask(__name__)
client = Groq(api_key="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")

def get_ai_response(messages):
    system_message = {
        "role": "system",
        "content": """{
  "Context": {
    "Role": "Eres un experto en inteligencia artificial que está ayudando con la preventa de software para una empresa. Tienes conocimiento sobre historias de usuario, requisitos funcionales y no funcionales, estimación de esfuerzo, generación de propuestas y dependencias de tareas.",
    "Instructions": "Cuando se te proporcione un JSON que contenga información sobre una empresa, proyecto y requerimientos, debes generar una lista de tareas con su ID, nombre, descripción, área de equipo responsable, tiempo estimado y costo en formato JSON. Responde solo con el JSON de las tareas, sin añadir nada extra.",
    "InputFormat": "Envía tus JSON de la siguiente manera: \n\n { \n \"Company\": { \n \"CompanyName\": \"Nombre de la Empresa\", \n \"CompanyDescription\": \"Breve descripción de la empresa\", \n \"CompanyDetails\": { \n \"Industry\": \"Sector de la empresa\", \n \"Location\": \"Ubicación de la empresa\", \n \"Size\": \"Tamaño de la empresa\" \n } \n }, \n \"Project\": { \n \"ProjectName\": \"Nombre del proyecto\", \n \"ProjectDescription\": \"Descripción general del proyecto\", \n \"ProjectDetails\": { \n \"Budget\": \"Presupuesto disponible\", \n \"Deadline\": \"Fecha límite\", \n \"ProjectManager\": \"Nombre del gerente del proyecto\" \n } \n }, \n \"Requirements\": [ \n { \n \"RequirementID\": \"ID del requerimiento 1\", \n \"RequirementDescription\": \"Descripción del requerimiento 1\" \n }, \n { \n \"RequirementID\": \"ID del requerimiento 2\", \n \"RequirementDescription\": \"Descripción del requerimiento 2\" \n } \n ] \n } \n\n La respuesta debe ser en este formato: \n\n { \n \"Tasks\": [ \n { \n \"TaskID\": \"ID de la tarea 1\", \n \"TaskName\": \"Nombre de la tarea 1\", \n \"TaskDescription\": \"Descripción de la tarea 1\", \n \"TeamArea\": \"Área del equipo responsable\", \n \"Time\": \"Tiempo estimado\", \n \"Cost\": \"Costo estimado\" \n }, \n { \n \"TaskID\": \"ID de la tarea 2\", \n \"TaskName\": \"Nombre de la tarea 2\", \n \"TaskDescription\": \"Descripción de la tarea 2\", \n \"TeamArea\": \"Área del equipo responsable\", \n \"Time\": \"Tiempo estimado\", \n \"Cost\": \"Costo estimado\" \n } \n ] \n }"""
    }
    
    messages.insert(0, system_message)
    
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )
    """print("PARSING INFORMATION")
    for chunk in completion:
        print(chunk)
    for i in chunk[1]:
        print(i)
    # print(completion[0][1])

    #return "response"
"""
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

@app.route('/ai/getAITasks', methods=['POST'])
def generate_tasks():
    data = request.json
    
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    
    # Crear el mensaje con el JSON recibido
    messages = [{"role": "user", "content": json.dumps(data, ensure_ascii=False)}]
    
    # Obtener la respuesta de la IA
    ai_response = get_ai_response(messages)

    return ai_response

    """
    # Procesar la respuesta para devolverla como JSON
    try:
        tasks = json.loads(ai_response).get("Tasks", [])
        return jsonify({"Tasks": tasks}), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Error processing AI response"}), 500
    """
        
if __name__ == "__main__":
    app.run(debug=True)
