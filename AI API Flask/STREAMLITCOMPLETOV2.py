import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="Gestión de Requerimientos y Tareas", layout="wide")

# Inicializar los datos en el estado de sesión
if 'requirements' not in st.session_state:
    st.session_state.requirements = []

if 'tasks' not in st.session_state:
    st.session_state.tasks = {}

# URLs de la API
API_BASE_URL = "http://localhost:5000"  # Asegúrate de que esta URL esté correcta
REQUIREMENTS_API_URL = f"{API_BASE_URL}/ai/getAIRequirements"
TASKS_API_URL = f"{API_BASE_URL}/ai/getAITasks"

# Funciones para llamar al API
def get_ai_requirements(input_data):
    try:
        response = requests.post(REQUIREMENTS_API_URL, json=input_data)
        response.raise_for_status()
        ai_response = json.loads(response.text)  # Convertir la respuesta de texto a JSON
        return ai_response  # Se espera que sea un diccionario con los requerimientos generados
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API de requerimientos: {e}")
        return None

def get_ai_tasks(input_data):
    try:
        response = requests.post(TASKS_API_URL, json=input_data)
        response.raise_for_status()
        ai_response = json.loads(response.text)  # Convertir la respuesta de texto a JSON
        return ai_response  # Se espera que sea un diccionario con las tareas generadas
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API de tareas: {e}")
        return None

# Función para mostrar requerimientos
def render_requirements():
    st.header("Requerimientos")

    if st.session_state.requirements:
        for idx, req in enumerate(st.session_state.requirements):
            with st.expander(f"{req['RequirementID']}: {req['RequirementDescription']}"):
                if st.button("Editar Requerimiento", key=f"edit_req_{idx}"):
                    st.session_state.editing_requirement_idx = idx
                if st.button("Ver Tareas", key=f"view_tasks_{idx}"):
                    st.session_state.selected_requirement_idx = idx
    else:
        st.info("No hay requerimientos. Por favor, agrega uno.")

# Función para agregar requerimiento
def add_requirement():
    st.subheader("Agregar Requerimiento")

    with st.form("add_requirement_form"):
        company_name = st.text_input("Nombre de la Empresa")
        project_name = st.text_input("Nombre del Proyecto")
        requirement_description = st.text_area("Descripción del Requerimiento")
        use_ai = st.checkbox("Generar con IA")

        submitted = st.form_submit_button("Agregar")

        if submitted:
            input_data = {
                "Company": {
                    "CompanyName": company_name,
                    "CompanyDescription": "",
                    "CompanyDetails": {
                        "Industry": "",
                        "Location": "",
                        "Size": ""
                    }
                },
                "Project": {
                    "ProjectName": project_name,
                    "ProjectDescription": "",
                    "ProjectDetails": {
                        "Budget": "",
                        "ProjectManager": ""
                    }
                },
                "Requirements": [],
                "Transcript": ""
            }

            if use_ai:
                # Generar requerimientos con IA
                ai_response = get_ai_requirements(input_data)
                if ai_response:
                    st.session_state.requirements.extend(ai_response.get("Requirements", []))
                    st.success("Requerimiento(s) agregado(s) con IA.")
            else:
                # Agregar requerimiento manualmente
                new_req = {
                    "RequirementID": f"REQ-{len(st.session_state.requirements)+1:03}",
                    "RequirementDescription": requirement_description,
                    "Owner": ""
                }
                st.session_state.requirements.append(new_req)
                st.success("Requerimiento agregado manualmente.")

# Función para editar requerimiento
def edit_requirement(idx):
    st.subheader("Editar Requerimiento")

    requirement = st.session_state.requirements[idx]

    with st.form(f"edit_requirement_form_{idx}"):
        requirement_description = st.text_area("Descripción del Requerimiento", value=requirement["RequirementDescription"])
        submitted = st.form_submit_button("Guardar Cambios")

        if submitted:
            st.session_state.requirements[idx]["RequirementDescription"] = requirement_description
            st.success("Requerimiento actualizado.")

# Función para mostrar tareas
def render_tasks(requirement_idx):
    requirement = st.session_state.requirements[requirement_idx]
    st.header(f"Tareas para {requirement['RequirementID']}")

    requirement_id = requirement['RequirementID']
    tasks = st.session_state.tasks.get(requirement_id, [])

    if tasks:
        for idx, task in enumerate(tasks):
            with st.expander(f"{task['TaskID']}: {task['TaskDescription']}"):
                if st.button("Editar Tarea", key=f"edit_task_{requirement_id}_{idx}"):
                    st.session_state.editing_task = {'requirement_id': requirement_id, 'task_idx': idx}
    else:
        st.info("No hay tareas para este requerimiento.")

    if st.button("Agregar Tarea", key=f"add_task_{requirement_id}"):
        st.session_state.adding_task_requirement_id = requirement_id

    if st.button("Volver a Requerimientos"):
        st.session_state.selected_requirement_idx = None

# Función para agregar tarea
def add_task(requirement_id):
    st.subheader("Agregar Tarea")

    with st.form(f"add_task_form_{requirement_id}"):
        task_description = st.text_area("Descripción de la Tarea")
        use_ai = st.checkbox("Generar con IA")

        submitted = st.form_submit_button("Agregar")

        if submitted:
            input_data = {
                "Company": {},
                "Project": {},
                "Requirements": [req for req in st.session_state.requirements if req['RequirementID'] == requirement_id],
                "Tasks": [],
                "Transcript": ""
            }

            if use_ai:
                ai_response = get_ai_tasks(input_data)
                if ai_response:
                    tasks = st.session_state.tasks.get(requirement_id, [])
                    tasks.extend(ai_response.get("Tasks", []))
                    st.session_state.tasks[requirement_id] = tasks
                    st.success("Tarea(s) agregada(s) con IA.")
            else:
                tasks = st.session_state.tasks.get(requirement_id, [])
                new_task = {
                    "TaskID": f"T-{len(tasks)+1:03}",
                    "TaskDescription": task_description
                }
                tasks.append(new_task)
                st.session_state.tasks[requirement_id] = tasks
                st.success("Tarea agregada manualmente.")

# Función para editar tarea
def edit_task(requirement_id, idx):
    st.subheader("Editar Tarea")

    task = st.session_state.tasks[requirement_id][idx]

    with st.form(f"edit_task_form_{requirement_id}_{idx}"):
        task_description = st.text_area("Descripción de la Tarea", value=task["TaskDescription"])
        submitted = st.form_submit_button("Guardar Cambios")

        if submitted:
            st.session_state.tasks[requirement_id][idx]["TaskDescription"] = task_description
            st.success("Tarea actualizada.")

# Función principal
def main():
    st.title("Gestión de Requerimientos y Tareas")

    # Menú lateral
    st.sidebar.title("Menú")
    menu_options = ["Ver Requerimientos", "Agregar Requerimiento"]
    choice = st.sidebar.selectbox("Seleccione una opción", menu_options)

    if choice == "Ver Requerimientos":
        render_requirements()
    elif choice == "Agregar Requerimiento":
        add_requirement()

    # Mostrar tareas si se seleccionó un requerimiento
    if 'selected_requirement_idx' in st.session_state and st.session_state.selected_requirement_idx is not None:
        render_tasks(st.session_state.selected_requirement_idx)

if __name__ == "__main__":
    main()
