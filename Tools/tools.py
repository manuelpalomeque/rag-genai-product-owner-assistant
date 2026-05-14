from dotenv import load_dotenv
from langchain.tools import tool
from typing import List, Dict, Optional, Any
import requests
from requests.auth import HTTPBasicAuth
import os
import json

load_dotenv()

@tool
def crear_issue_en_backlog(
    resumen: str,
    descripcion: str,
    tipo_issue: str = "Task",
    prioridad: Optional[str] = None,
    etiquetas: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Crea un issue en el backlog del proyecto Jira SCRUM.
    
    IMPORTANTE:
    - Los issues se crean automáticamente en estado "Backlog"
    - No requiere especificar sprint, se asigna al backlog por defecto
    
    EJEMPLOS DE USO:
    - User: "Crea un bug de alta prioridad llamado 'Login falla'"
      → tipo_issue="Bug", prioridad="Highest"
    
    - User: "Crea una story para mejora de UI con etiquetas frontend, ui"
      → tipo_issue="Story", etiquetas=["frontend", "ui"]
    
    PARÁMETROS:
    - resumen: Título corto (máx 255 chars). Ej: "Corregir error en login"
    - descripcion: Texto largo opcional. Soporta Markdown.
    - tipo_issue: Task|Bug|Story|Epic (default: Task)
    - prioridad: Highest|High|Medium|Low|Lowest (default: None = sin prioridad)
    - etiquetas: Lista de strings. Ej: ["frontend", "backend", "urgente"]
    """

    # =========================
    # Validar configuración
    # =========================

    jira_url = os.getenv("JIRA_BASE_URL")
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")

    if not jira_url or not email or not api_token:
        return {
            "success": False,
            "message": "Faltan variables de entorno de Jira.",
            "data": None,
        }

    # =========================
    # Configuración Jira
    # =========================

    proyecto_key = "SCRUM"

    endpoint = f"{jira_url}/rest/api/3/issue"

    # =========================
    # Payload
    # =========================

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
                                "text": descripcion or "Sin descripción"
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

    # Prioridad
    if prioridad:
        payload["fields"]["priority"] = {
            "name": prioridad
        }

    # Etiquetas
    if etiquetas:
        payload["fields"]["labels"] = etiquetas

    # =========================
    # Request
    # =========================

    auth = HTTPBasicAuth(email, api_token)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            auth=auth,
            json=payload,
            timeout=15,
        )

        # =========================
        # Éxito
        # =========================

        if response.status_code == 201:
            issue_data = response.json()

            issue_key = issue_data.get("key")

            return {
                "success": True,
                "message": f"Issue {issue_key} creado exitosamente.",
                "data": {
                    "key": issue_key,
                    "id": issue_data.get("id"),
                    "url": f"{jira_url}/browse/{issue_key}",
                },
            }

        # =========================
        # Error Jira
        # =========================

        error_detail = response.text

        try:
            error_json = response.json()
            error_detail = error_json
        except Exception:
            pass

        return {
            "success": False,
            "message": f"Error al crear issue en Jira. Status: {response.status_code}",
            "data": error_detail,
        }

    # =========================
    # Error conexión
    # =========================

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "Timeout al conectar con Jira.",
            "data": None,
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Error de conexión con Jira: {str(e)}",
            "data": None,
        }
    
# ---
from dotenv import load_dotenv

load_dotenv()

from langchain_core.tools import tool

import os
import requests

from requests.auth import HTTPBasicAuth


# =========================================================
# CONFIG
# =========================================================

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
BASE_URL = os.getenv("JIRA_BASE_URL")


auth = HTTPBasicAuth(EMAIL, API_TOKEN)

headers = {
    "Accept": "application/json"
}


# =========================================================
# HELPERS
# =========================================================

def extract_text_from_adf(adf_content: dict) -> str:
    """
    Convierte contenido ADF de Jira a texto plano.
    """

    if not adf_content:
        return ""

    text_parts = []

    def process_node(node):

        if isinstance(node, dict):

            if node.get("type") == "text":
                text_parts.append(node.get("text", ""))

            for child in node.get("content", []):
                process_node(child)

        elif isinstance(node, list):

            for item in node:
                process_node(item)

    process_node(adf_content)

    return " ".join(text_parts)


def jira_get(url: str, params: dict | None = None) -> dict:
    """
    Ejecuta requests GET a Jira.
    """

    response = requests.get(
        url,
        headers=headers,
        auth=auth,
        params=params
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# TOOL
# =========================================================

@tool
def get_issues_by_label(label: str) -> list[dict]:
    """
    Busca issues del sprint activo filtrando por una etiqueta.
    
    Args:
        label: Etiqueta de Jira.
    
    Returns:
        Lista de issues.
    """

    try:

        url = f"{BASE_URL}/rest/api/3/search/jql"

        params = {
            "jql": (
                f"project = SCRUM "
                f"AND sprint in openSprints() "
                f"AND labels = {label}"
            ),
            "maxResults": 20,
            "fields": [
                "summary",
                "description",
                "status",
                "assignee",
                "priority",
                "labels",
                "issuetype"
            ]
        }

        data = jira_get(url, params)

        issues_result = []

        for issue in data.get("issues", []):

            fields = issue.get("fields", {})

            # =========================================
            # DESCRIPTION
            # =========================================

            description = fields.get("description")

            if isinstance(description, dict):
                description = extract_text_from_adf(description)

            elif description is None:
                description = ""

            else:
                description = str(description)

            # Truncar descripción larga
            if len(description) > 300:
                description = description[:300] + "..."

            # =========================================
            # ISSUE DATA
            # =========================================

            issue_data = {
                "key": issue.get("key"),

                "summary": fields.get("summary"),

                "status": (
                    fields.get("status", {})
                    .get("name")
                ),

                "assignee": (
                    fields.get("assignee", {})
                    .get("displayName")
                    if fields.get("assignee")
                    else "Sin asignar"
                ),

                "priority": (
                    fields.get("priority", {})
                    .get("name")
                    if fields.get("priority")
                    else "Sin prioridad"
                ),

                "issue_type": (
                    fields.get("issuetype", {})
                    .get("name")
                ),

                "labels": fields.get("labels", []),

                "description": description
            }

            issues_result.append(issue_data)

        return issues_result

    except Exception as e:

        return [
            {
                "error": str(e)
            }
        ]
