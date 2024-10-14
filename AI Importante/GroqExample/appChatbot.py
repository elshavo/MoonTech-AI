from groq import Groq
import streamlit as st

client = Groq(api_key="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")

def get_ai_response(messages):
    # Define el mensaje del sistema
    system_message = {
        "role": "system",
        "content": """
Eres un experto en inteligencia artificial que está ayudando con la 
preventa de software para una empresa. Tienes conocimiento sobre historias 
de usuario, requisitos funcionales y no funcionales, estimación de esfuerzo,
 generación de propuestas y dependencias de tareas. """
    }
    
    # Inserta el mensaje del sistema al inicio de la lista de mensajes
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

    with st.form(key="chat_form", clear_on_submit=True):
        st.text_input("Tu: ", key="user_input")
        submit_button = st.form_submit_button(label="Enviar", on_click=submit)

if __name__ == "__main__":
    chat()