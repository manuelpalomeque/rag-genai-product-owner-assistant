# Datos a solicitar al usuario:
datos_necesarios = {
    "resumen": str,  # Título/descripción corta del issue (obligatorio)
    "descripcion": str,  # Descripción detallada (opcional pero recomendada)
    "tipo_issue": str,  # Task, Bug, Story, Epic, etc. (obligatorio)
    "prioridad": str,  # Highest, High, Medium, Low, Lowest (opcional)
    "etiquetas": list,  # Lista de etiquetas como ["backend", "python"] (opcional)
}

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import json

# Cargar variables de entorno
load_dotenv()

def crear_issue_en_backlog(
    resumen,
    descripcion="",
    tipo_issue="Task",
    prioridad=None,
    etiquetas=None
):
    """
    Crea un issue en Jira Cloud y lo guarda en el backlog del proyecto SCRUM
    
    Args:
        resumen: Título del issue
        descripcion: Descripción detallada (soporta HTML/Markdown)
        tipo_issue: Task, Bug, Story, Epic, etc.
        prioridad: Highest, High, Medium, Low, Lowest
        etiquetas: Lista de strings con etiquetas
    
    Returns:
        dict: Respuesta de la API con los datos del issue creado
    """
    
    # Configuración de autenticación
    jira_url = os.getenv("JIRA_BASE_URL")  # Ej: "https://tudominio.atlassian.net"
    email = os.getenv("JIRA_EMAIL")   # Tu email de Jira
    api_token = os.getenv("JIRA_API_TOKEN")  # Token de API de Atlassian
    
    # Endpoint para crear issues
    endpoint = f"{jira_url}/rest/api/3/issue"
    
    # Obtener el ID del proyecto SCRUM
    proyecto_key = "SCRUM"
    
    # Construir el payload del issue
    payload = {
        "fields": {
            "project": {
                "key": proyecto_key
            },
            "summary": resumen,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": descripcion if descripcion else "Sin descripción"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": tipo_issue
            }
        }
    }
    
    # Agregar prioridad si se proporciona
    if prioridad:
        payload["fields"]["priority"] = {
            "name": prioridad
        }
    
    # Agregar etiquetas si se proporcionan
    if etiquetas:
        payload["fields"]["labels"] = etiquetas
    
    # Configurar para que vaya al backlog (esto es por defecto en proyectos SCRUM)
    # Los issues nuevos se crean en estado "Backlog" automáticamente
    # Si quieres asegurarlo, puedes agregar:
    # payload["fields"]["customfield_10005"] = "Backlog"  # Esto varía por proyecto
    
    # Autenticación básica
    auth = HTTPBasicAuth(email, api_token)
    
    # Headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        # Realizar la petición POST
        response = requests.post(
            endpoint,
            data=json.dumps(payload),
            headers=headers,
            auth=auth
        )
        
        # Verificar respuesta
        if response.status_code == 201:
            issue_data = response.json()
            print(f"✅ Issue creado exitosamente!")
            print(f"🔗 Key: {issue_data['key']}")
            print(f"📋 URL: {jira_url}/browse/{issue_data['key']}")
            return issue_data
        else:
            print(f"❌ Error al crear el issue: {response.status_code}")
            print(f"Detalles: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None

# Función para solicitar datos al usuario
def solicitar_datos_usuario():
    """Solicita los datos necesarios al usuario para crear un issue"""
    print("=== Crear nuevo issue en Jira ===\n")
    
    resumen = input("Resumen del issue (obligatorio): ")
    while not resumen.strip():
        resumen = input("El resumen es obligatorio: ")
    
    descripcion = input("Descripción (opcional, Enter para omitir): ")
    
    print("\nTipos de issue disponibles: Task, Bug, Story, Epic, Sub-task")
    tipo_issue = input("Tipo de issue (default: Task): ") or "Task"
    
    print("\nPrioridades: Highest, High, Medium, Low, Lowest")
    prioridad = input("Prioridad (opcional, Enter para omitir): ") or None
    
    etiquetas_input = input("Etiquetas (separadas por coma, opcional): ")
    etiquetas = [et.strip() for et in etiquetas_input.split(",")] if etiquetas_input else None
    
    return {
        "resumen": resumen,
        "descripcion": descripcion,
        "tipo_issue": tipo_issue,
        "prioridad": prioridad,
        "etiquetas": etiquetas
    }

# Ejemplo de uso
if __name__ == "__main__":
    # Opción 1: Solicitar datos al usuario
    datos = solicitar_datos_usuario()
    
    # Crear el issue
    resultado = crear_issue_en_backlog(**datos)
    
    # Opción 2: Usar datos hardcodeados para pruebas
    # resultado = crear_issue_en_backlog(
    #     resumen="Implementar nueva funcionalidad de búsqueda",
    #     descripcion="Crear endpoint de búsqueda con filtros avanzados",
    #     tipo_issue="Task",
    #     prioridad="High",
    #     etiquetas=["backend", "search", "python"]
    # )