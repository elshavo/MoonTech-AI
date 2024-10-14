from groq import Groq
import streamlit as st
import json
import datetime

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
        stream=True,
    )
    
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

def chat():
    st.title("Chat con llama3.1 con Groq")
    st.write("Bienvenido al chat de llama3.1 con Groq, escribe exit para terminar la conversación.")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = []

    # Formulario para crear el JSON
    with st.form(key="json_form", clear_on_submit=True):
        st.subheader("Completa la información de la empresa y el proyecto")
        
        company_name = st.text_input("Nombre de la Empresa:", "Tech Innovations S.A.")
        company_description = st.text_area("Descripción de la Empresa:", "Una empresa dedicada al desarrollo de soluciones tecnológicas innovadoras.")
        industry = st.text_input("Sector:", "Tecnología")
        location = st.text_input("Ubicación:", "Ciudad de México, México")
        size = st.selectbox("Tamaño:", ["Pequeña", "Mediana", "Grande"])
        
        project_name = st.text_input("Nombre del Proyecto:", "Desarrollo de Plataforma de E-commerce")
        project_description = st.text_area("Descripción del Proyecto:", "Proyecto para desarrollar una plataforma de e-commerce que permita a los usuarios comprar productos en línea.")
        budget = st.text_input("Presupuesto:", "50000 USD")
        deadline = st.date_input("Fecha Límite:", value=datetime.date(2024, 12, 31))  # Corrigiendo el valor predeterminado
        project_manager = st.text_input("Nombre del Gerente del Proyecto:", "Juan Pérez")

        requirement_1 = st.text_area("Requerimiento 1:", "El sistema debe permitir el registro de nuevos usuarios.")
        requirement_2 = st.text_area("Requerimiento 2:", "El sistema debe incluir un carrito de compras.")
        requirement_3 = st.text_area("Requerimiento 3:", "El sistema debe procesar pagos a través de tarjeta de crédito y PayPal.")

        # Crear botón de envío
        submit_button = st.form_submit_button(label="Enviar")

        if submit_button:
            # Crear el JSON a partir de los datos del formulario
            json_data = {
                "Company": {
                    "CompanyName": company_name,
                    "CompanyDescription": company_description,
                    "CompanyDetails": {
                        "Industry": industry,
                        "Location": location,
                        "Size": size
                    }
                },
                "Project": {
                    "ProjectName": project_name,
                    "ProjectDescription": project_description,
                    "ProjectDetails": {
                        "Budget": budget,
                        "Deadline": str(deadline),  # Convertir a string para JSON
                        "ProjectManager": project_manager
                    }
                },
                "Requirements": [
                    {
                        "RequirementID": "REQ-001",
                        "RequirementDescription": requirement_1
                    },
                    {
                        "RequirementID": "REQ-002",
                        "RequirementDescription": requirement_2
                    },
                    {
                        "RequirementID": "REQ-003",
                        "RequirementDescription": requirement_3
                    }
                ]
            }

            # Añadir el JSON al estado de mensajes
            st.session_state["messages"].append({"role": "user", "content": json.dumps(json_data, ensure_ascii=False)})

            with st.spinner("Obteniendo respuesta..."):
                ai_response = get_ai_response(st.session_state["messages"])
                st.session_state["messages"].append({"role": "assistant", "content": ai_response})

                # Procesar la respuesta para extraer las tareas
                ai_tasks = json.loads(ai_response).get("Tasks", [])
                st.session_state["tasks"] = ai_tasks  # Almacenar tareas en el estado

    # Mostrar mensajes en el chat
    for message in st.session_state["messages"]:
        role = "Tu" if message["role"] == "user" else "Bot"
        st.write(f"**{role}**: {message['content']}")

    # Mostrar tarjetas de tareas si hay respuesta de AI
    if st.session_state["tasks"]:
        st.subheader("Tareas Generadas")
        for task in st.session_state["tasks"]:
            with st.container():  # Usar container en lugar de card
                st.subheader(f"Tarea: {task['TaskName']}")
                st.write(f"**ID de Tarea:** {task['TaskID']}")
                st.write(f"**Descripción:** {task['TaskDescription']}")
                st.write(f"**Área del Equipo:** {task['TeamArea']}")
                st.write(f"**Tiempo Estimado:** {task['Time']}")
                st.write(f"**Costo:** {task['Cost']}")
                st.markdown("---")  # Línea divisoria entre tareas


if __name__ == "__main__":
    chat()
