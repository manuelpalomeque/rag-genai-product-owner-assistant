from dotenv import load_dotenv
load_dotenv()

import os
from requests.auth import HTTPBasicAuth
import requests
from pprint import pprint

email = os.getenv('JIRA_EMAIL')
api_token = os.getenv('JIRA_API_TOKEN')
base_url = os.getenv('JIRA_BASE_URL')

auth = HTTPBasicAuth(email, api_token)
headers = {"Accept": "application/json"}

print(" PASO 1: Detectando campos en tu instancia de Jira...")
print("-" * 60)

# Obtener todos los campos disponibles
fields_url = f"{base_url}/rest/api/3/field"
fields_response = requests.get(fields_url, auth=auth, headers=headers)

if fields_response.status_code != 200:
    print(f"Error al obtener campos: {fields_response.status_code}")
    exit()

all_fields = fields_response.json()

# Buscar campos por nombres comunes (español/inglés)
sprint_field_id = None
parent_link_field_id = None
epic_link_field_id = None

for field in all_fields:
    field_name = field.get('name', '').lower()
    field_id = field['id']
    
    # Buscar Sprint (varios nombres posibles)
    if any(name in field_name for name in ['sprint', 'sprint name']):
        sprint_field_id = field_id
        print(f"Sprint encontrado: {field_id} - {field['name']}")
    
    # Buscar Parent Link / Principal / Epic Link
    if any(name in field_name for name in ['principal', 'parent', 'epic link', 'epic', 'padre']):
        parent_link_field_id = field_id
        print(f"Parent/Principal/Epic encontrado: {field_id} - {field['name']}")
    
    # También buscar específicamente "Principal" en español
    if field['name'] == 'Principal':
        parent_link_field_id = field_id
        print(f"Campo 'Principal' encontrado: {field_id}")

if not sprint_field_id:
    print("No se encontró el campo Sprint - puede tener otro nombre")

if not parent_link_field_id:
    print("No se encontró el campo Principal/Epic")

print("\nPASO 2: Buscando issues del sprint en curso...")
print("-" * 60)

# URL correcta del endpoint
url = f"{base_url}/rest/api/3/search/jql"

# Parámetros de búsqueda
params = {
    "jql": "project = SCRUM AND sprint in openSprints()",
    "maxResults": 50,
    "fields": [
        "summary",
        "status", 
        "assignee",
        "priority",
        "labels",
        "issuetype"
    ]
}

# Agregar campos dinámicos si los encontramos
if sprint_field_id:
    params["fields"].append(sprint_field_id)
if parent_link_field_id:
    params["fields"].append(parent_link_field_id)

response = requests.get(url, auth=auth, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"Se encontraron {data.get('total', 0)} issues\n")
    
    for issue in data.get('issues', []):
        fields = issue['fields']
        print(f"🔹 {issue['key']}: {fields.get('summary', 'Sin título')}")
        print(f"   - Estado: {fields.get('status', {}).get('name', 'Desconocido')}")
        
        # Mostrar Sprint (con el ID correcto)
        if sprint_field_id:
            sprint_data = fields.get(sprint_field_id)
            if sprint_data:
                # El sprint puede ser objeto o lista
                if isinstance(sprint_data, dict):
                    sprint_name = sprint_data.get('name', 'Desconocido')
                    sprint_state = sprint_data.get('state', '')
                    print(f"   - Sprint: {sprint_name} ({sprint_state})")
                elif isinstance(sprint_data, list) and sprint_data:
                    sprint_name = sprint_data[0].get('name', 'Desconocido')
                    print(f"   - Sprint: {sprint_name}")
                else:
                    print(f"   - Sprint: {sprint_data}")
            else:
                print(f"   - Sprint: No asignado")
        else:
            print(f"   - Sprint: Campo no encontrado en API")
        
        # Mostrar Principal / Epic Link
        if parent_link_field_id:
            parent_data = fields.get(parent_link_field_id)
            if parent_data:
                # El parent puede ser un objeto con key o solo el key
                if isinstance(parent_data, dict):
                    parent_key = parent_data.get('key', str(parent_data))
                else:
                    parent_key = str(parent_data)
                print(f"   - Principal/Epic: {parent_key}")
            else:
                print(f"   - Principal/Epic: No asignado")
        else:
            print(f"   - Principal/Epic: Campo no encontrado en API")
        
        # Mostrar etiquetas
        labels = fields.get('labels', [])
        labels_str = ", ".join(labels) if labels else "Sin etiquetas"
        print(f"   - Etiquetas: {labels_str}")
        
        # Mostrar prioridad
        priority = fields.get('priority')
        if priority:
            print(f"   - Prioridad: {priority.get('name', 'Desconocida')}")
        
        # Mostrar asignado
        assignee = fields.get('assignee')
        if assignee:
            print(f"   - Asignado: {assignee.get('displayName', 'Desconocido')}")
        
        print()
        
        # DEBUG: Mostrar todos los campos de un issue (opcional)
        # Descomentar para ver qué campos tiene realmente
        # if issue['key'] == 'SCRUM-19':  # Solo para el issue que te interesa
        #     print("   📋 TODOS los campos disponibles:")
        #     for field_name, field_value in fields.items():
        #         if field_value:
        #             print(f"      {field_name}: {str(field_value)[:100]}")
        #     print()
        
else:
    print(f"✗ Error: {response.status_code}")
    print(f"Respuesta: {response.text}")