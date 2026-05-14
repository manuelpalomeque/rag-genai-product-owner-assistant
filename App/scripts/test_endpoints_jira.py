from dotenv import load_dotenv
load_dotenv()

import os
from requests.auth import HTTPBasicAuth
import requests
from pprint import pprint

email = os.getenv('JIRA_EMAIL')
api_token = os.getenv('JIRA_API_TOKEN')
base_url = os.getenv('JIRA_BASE_URL')

# Endpoint para verificar autenticación ------------------------------------------------
url = f"{base_url}/rest/api/3/serverInfo"

response = requests.get(
    url,
    auth=HTTPBasicAuth(email, api_token),
    headers={"Accept": "application/json"}
)

print(f"Código de estado: {response.status_code}")

if response.status_code == 200:
    print(" Autenticación exitosa")
    pprint(response.json())
else:
    print(f"✗ Error: {response.status_code}")
    print(f"Respuesta: {response.text}")


# Endpoint para verificar información de usuario ----------------------------------------
url = f"{base_url}/rest/api/3/myself"

response = requests.get(
    url,
    auth=HTTPBasicAuth(email, api_token),
    headers={"Accept": "application/json"}
)
print(f"ENDPOINT INFO USUARIO")
print(f"Código de estado: {response.status_code}")

if response.status_code == 200:
    print("Informacion del usuario")
    pprint(response.json())
else:
    print(f"✗ Error: {response.status_code}")
    print(f"Respuesta: {response.text}")

# Endpoint proyectos  ------------------------------------------------
# a) Obtener todos los proyectos
url = f"{base_url}/rest/api/3/project"

response = requests.get(
    url,
    auth=HTTPBasicAuth(email, api_token),
    headers={"Accept": "application/json"}
)
print(f"ENDPOINT TODOS LOS PROYECTOS")
print(f"Código de estado: {response.status_code}")

if response.status_code == 200:
    print("Informacion de proyectos")
    pprint(response.json())
else:
    print(f"✗ Error: {response.status_code}")
    print(f"Respuesta: {response.text}")

# B) Obtener un proyecto específico por su clave
url = f"{base_url}/rest/api/3/project/SCRUM"

response = requests.get(
    url,
    auth=HTTPBasicAuth(email, api_token),
    headers={"Accept": "application/json"}
)
print(f"ENDPOINT PROYECTO SCRUM")
print(f"Código de estado: {response.status_code}")

if response.status_code == 200:
    print("Informacion de proyectos")
    pprint(response.json())
else:
    print(f"✗ Error: {response.status_code}")
    print(f"Respuesta: {response.text}")

# Endpoint Issues (tareas, historias, bugs)  ------------------------------------------------

# Obtener un issue específico por su ID
issueIdOrKey = "SCRUM-1"
url = f"{base_url}/rest/api/3/issue/{issueIdOrKey}"

response = requests.get(
    url,
    auth=HTTPBasicAuth(email, api_token),
    headers={"Accept": "application/json"}
)
print(f"Obtener un issue específico por su ID")
print(f"Código de estado: {response.status_code}")

if response.status_code == 200:
    print("Obtener un issue específico por su ID")
    pprint(response.json())
else:
    print(f"✗ Error: {response.status_code}")
    print(f"Respuesta: {response.text}")


# Buscar issues con JQL (Jira Query Language)
url = f"{base_url}/rest/api/3/search/jql?jql=project=SCRUM"
# Parámetros comunes: 
# - jql: consulta de búsqueda
# - maxResults: cantidad máxima (default 50)
# - fields: qué campos devolver

response = requests.get(
    url,
    auth=HTTPBasicAuth(email, api_token),
    headers={"Accept": "application/json"}
)
print(f"Buscar issues con JQL (Jira Query Language)")
print(f"Código de estado: {response.status_code}")

if response.status_code == 200:
    print("Buscar issues con JQL (Jira Query Language)")
    pprint(response.json())
else:
    print(f"✗ Error: {response.status_code}")
    print(f"Respuesta: {response.text}")