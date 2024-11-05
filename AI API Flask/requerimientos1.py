from groq import Groq
import streamlit as st
import json
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Obtener la API key desde el entorno
groq_api_key = os.getenv('GROQ_API_KEY')

# Inicializar el cliente Groq con la API key
client = Groq(api_key=groq_api_key)

def get_ai_response(messages):
    system_message = {
        "role": "system",
        "content": """{
            "Context": {
                "Role": "Eres un experto en inteligencia artificial especializado en la ingeniería de requerimientos para proyectos de software en el contexto de preventa. Tienes amplio conocimiento sobre la recopilación y análisis de requisitos funcionales y no funcionales, estimación de tiempos y esfuerzos, prioridades, y estándares como IEEE 830 y UML. Tu objetivo es ayudar a generar requerimientos claros, concisos y detallados, asegurando que sean técnicamente viables y alineados con los objetivos del negocio y las mejores prácticas de la industria.",
                "Instructions": "Cuando se te proporcione un JSON que contenga información sobre una empresa, un proyecto y una transcripción de una reunión, debes generar una lista de requerimientos funcionales y no funcionales en formato JSON. Responde solo con el JSON de los requerimientos, sin añadir nada extra.",
                "InputFormat": "Envía el JSON en este formato: \n\n { \n "Company": { \n "CompanyName": "Nombre de la Empresa", \n "CompanyDescription": "Breve descripción de la empresa", \n "CompanyDetails": { \n "Industry": "Sector de la empresa", \n "Location": "Ubicación de la empresa", \n "Size": "Tamaño de la empresa" \n } \n }, \n "Project": { \n "ProjectName": "Nombre del proyecto", \n "ProjectDescription": "Descripción general del proyecto", \n "ProjectDetails": { \n "Budget": "Presupuesto disponible", \n "Deadline": "Fecha límite", \n "ProjectManager": "Nombre del gerente del proyecto" \n } \n }, \n "Requirements": \n { \n \"RequirementID\": \"ID del requerimiento 1\", \n \"RequirementDescription\": \"Descripción del requerimiento 1\" \n }, \n { \n \"RequirementID\": \"ID del requerimiento 2\", \n \"RequirementDescription\": \"Descripción del requerimiento 2\" \n } \n, \n "Transcript": "Texto de la transcripción aquí" 
                }
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
    st.title("REQUERIMIENTOS DE SOFTWARE - LLAMA3.1")
    st.write("Bienvenido al chat de Llama3.1, A continuación escriba la información solicitada para generar los requerimientos.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "requirements" not in st.session_state:
        st.session_state["requirements"] = {}

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
        deadline = st.date_input("Fecha Límite:", value=datetime.date(2024, 12, 31))
        project_manager = st.text_input("Nombre del Gerente del Proyecto:", "Juan Pérez")

        requirement_1 = st.text_area("Requerimiento 1:", "El sistema debe permitir el registro de nuevos usuarios.")
        requirement_2 = st.text_area("Requerimiento 2:", "El sistema debe incluir un carrito de compras.")
        requirement_3 = st.text_area("Requerimiento 3:", "El sistema debe procesar pagos a través de tarjeta de crédito y PayPal.")

        transcript = st.text_area("Texto de la transcripción de la reunión:", "")

        submit_button = st.form_submit_button(label="Enviar")

        if submit_button:
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
                        "Deadline": str(deadline),
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
                ],
                "Transcript": transcript
            }

            st.session_state["messages"].append({"role": "user", "content": json.dumps(json_data, ensure_ascii=False)})

            with st.spinner("Obteniendo respuesta..."):
                ai_response = get_ai_response(st.session_state["messages"])
                st.session_state["messages"].append({"role": "assistant", "content": ai_response})

                st.write("Respuesta de la IA:")
                st.write(ai_response)

                try:
                    ai_requirements = json.loads(ai_response)
                    st.session_state["requirements"] = ai_requirements
                except json.JSONDecodeError as e:
                    st.error(f"Error al procesar la respuesta de la IA: {e}")

    # Mostrar tarjetas de requerimientos si hay respuesta de AI
    if st.session_state["requirements"]:
        for key, value in st.session_state["requirements"].items():
            st.subheader(key)
            for requirement in value:
                with st.container():  
                    st.subheader(f"Requerimiento: {requirement['RequerimientoID']}")
                    st.write(f"**Descripción:** {requirement['RequerimientoDescription']}")
                    # Si hay más campos en los requerimientos, puedes agregarlos aquí
                    st.markdown("---")  

    # Botón para generar más requerimientos
    if st.button("Generar Más Requerimientos"):
        new_message = {
            "role": "user",
            "content": "Con base en la conversación anterior y el contexto, genera más requerimientos y responde solo con el JSON sin comentarios adicionales."
        }
        st.session_state["messages"].append(new_message)  
    
        with st.spinner("Generando más requerimientos..."):
            ai_response = get_ai_response(st.session_state["messages"])
            st.session_state["messages"].append({"role": "assistant", "content": ai_response})

            st.write("Respuesta de la IA:")
            st.write(ai_response)

            try:
                ai_requirements = json.loads(ai_response)
                st.session_state["requirements"] = ai_requirements
            except json.JSONDecodeError as e:
                st.error(f"Error al procesar la respuesta de la IA: {e}")

            # Mostrar las tarjetas de los requerimientos después de agregar nuevas
            if st.session_state["requirements"]:
                for key, value in st.session_state["requirements"].items():
                    st.subheader(key)
                    for requirement in value:
                        with st.container():  
                            st.subheader(f"Requerimiento: {requirement['RequerimientoID']}")
                            st.write(f"**Descripción:** {requirement['RequerimientoDescription']}")
                            # Si hay más campos en los requerimientos, puedes agregarlos aquí
                            st.markdown("---")  

if __name__ == "__main__":
    chat()