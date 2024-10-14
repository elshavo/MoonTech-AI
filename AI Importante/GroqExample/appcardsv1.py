from groq import Groq
import streamlit as st
import json  # Asegúrate de importar json

client = Groq(api_key="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")

def get_ai_response(messages):
    system_message = {
        "role": "system",
        "content": """{
  "Context": {
    "Role": "Eres un experto en inteligencia artificial que está ayudando con la preventa de software para una empresa. Tienes conocimiento sobre historias de usuario, requisitos funcionales y no funcionales, estimación de esfuerzo, generación de propuestas y dependencias de tareas.",
    "Instructions": "Cuando se te proporcione un JSON que contenga información sobre una empresa, proyecto y requerimientos, debes generar una lista de tareas con su ID, nombre, descripción, área de equipo responsable, tiempo estimado y costo en formato JSON. Responde solo con el JSON de las tareas, sin añadir nada extra.",
    "InputFormat": "Envía tus JSON de la siguiente manera: \n\n { \n \"Company\": { \n \"CompanyName\": \"Nombre de la Empresa\", \n \"CompanyDescription\": \"Breve descripción de la empresa\", \n \"CompanyDetails\": { \n \"Industry\": \"Sector de la empresa\", \n \"Location\": \"Ubicación de la empresa\", \n \"Size\": \"Tamaño de la empresa\" \n } \n }, \n \"Project\": { \n \"ProjectName\": \"Nombre del proyecto\", \n \"ProjectDescription\": \"Descripción general del proyecto\", \n \"ProjectDetails\": { \n \"Budget\": \"Presupuesto disponible\", \n \"Deadline\": \"Fecha límite\", \n \"ProjectManager\": \"Nombre del gerente del proyecto\" \n } \n }, \n \"Requirements\": [ \n { \n \"RequirementID\": \"ID del requerimiento 1\", \n \"RequirementDescription\": \"Descripción del requerimiento 1\" \n }, \n { \n \"RequirementID\": \"ID del requerimiento 2\", \n \"RequirementDescription\": \"Descripción del requerimiento 2\" \n } \n ] \n } \n\n La respuesta debe ser en este formato: \n\n { \n \"Tasks\": [ \n { \n \"TaskID\": \"ID de la tarea 1\", \n \"TaskName\": \"Nombre de la tarea 1\", \n \"TaskDescription\": \"Descripción de la tarea 1\", \n \"TeamArea\": \"Área del equipo responsable\", \n \"Time\": \"Tiempo estimado\", \n \"Cost\": \"Costo estimado\" \n }, \n { \n \"TaskID\": \"ID de la tarea 2\", \n \"TaskName\": \"Nombre de la tarea 2\", \n \"TaskDescription\": \"Descripción de la tarea 2\", \n \"TeamArea\": \"Área del equipo responsable\", \n \"Time\": \"Tiempo estimado\", \n \"Cost\": \"Costo estimado\" \n } \n ] \n }"
  }
}"""
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

    def submit():
        user_input = st.session_state.user_input
        if user_input.lower() == "exit":
            st.write("Gracias por chatear! Adios.")
            st.stop()

        st.session_state["messages"].append({"role": "user", "content": user_input})

        with st.spinner("Obteniendo respuesta..."):
            ai_response = get_ai_response(st.session_state["messages"])
            st.session_state["messages"].append({"role": "assistant", "content": ai_response})

        st.session_state.user_input = ""

    for message in st.session_state["messages"]:
        role = "Tu" if message["role"] == "user" else "Bot"
        st.write(f"**{role}**: {message['content']}")

    # Mostrar tarjetas de tareas si hay respuesta de AI
    if st.session_state["messages"] and st.session_state["messages"][-1]["role"] == "assistant":
        ai_response = json.loads(st.session_state["messages"][-1]["content"])  # Convertir la respuesta a JSON
        tasks = ai_response.get("Tasks", [])

        st.subheader("Tareas Generadas")
        for task in tasks:
            with st.container():  # Usar container en lugar de card
                st.subheader(f"Tarea: {task['TaskName']}")
                st.write(f"**ID de Tarea:** {task['TaskID']}")
                st.write(f"**Descripción:** {task['TaskDescription']}")
                st.write(f"**Área del Equipo:** {task['TeamArea']}")
                st.write(f"**Tiempo Estimado:** {task['Time']}")
                st.write(f"**Costo:** {task['Cost']}")
                st.markdown("---")  # Línea divisoria entre tareas


    with st.form(key="chat_form", clear_on_submit=True):
        st.text_input("Tu: ", key="user_input")
        submit_button = st.form_submit_button(label="Enviar", on_click=submit)

if __name__ == "__main__":
    chat()
