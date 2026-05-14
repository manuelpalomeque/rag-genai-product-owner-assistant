# 🤖 Asistente IA para Product Owners

Un sistema multi-agente basado en IA diseñado para asistir a Product Owners en tareas de gestión ágil Scrum y  consulta operativa sobre Jira Cloud.

El proyecto está construido utilizando una arquitectura de orquestación con **LangGraph**, integrando agentes especializados, herramientas externas y capacidades RAG (Retrieval-Augmented Generation).

---

# 🚀 Objetivos del Proyecto

Este asistente busca resolver dos grandes necesidades dentro de equipos ágiles:

* **Asistencia conceptual y mentoring ágil**

  * Scrum
  * Ceremonias ágiles
  * Buenas prácticas
  * Gestión de backlog


* **Acceso operativo automatizado**

  * Crear Issues en Jira Cloud de manera asistida por IA
  * Estado de sprints
  * Issues bloqueantes
  * Filtrar Issues del sprint en curso por una etiqueta
  * Generación de reportes para stakeholders


---

# 🧠 Arquitectura General

El sistema sigue una arquitectura de:

## Orquestador Multi-Agente

Donde un agente supervisor analiza la intención del usuario y delega la tarea al subagente más adecuado.

```text
Usuario
   │
   ▼
┌─────────────────────┐
│ Agente Orquestador  │
│    (LangGraph)      │
└─────────┬───────────┘
          │
 ┌────────┼────────┐
 ▼                ▼
Mentor           Jira
Agent            Agent
```

---

# 🧩 Componentes Principales

## 1. Agente Orquestador (Supervisor)

Responsabilidades:

* Analizar la intención del usuario
* Mantener el estado conversacional
* Decidir qué subagente ejecutar
* Coordinar herramientas
* Consolidar respuestas

Tecnología principal:

* LangGraph
* StateGraph
* Conditional Edges

---

## 2. Subagente Mentor (Scrum & Documentación)

Especializado en:

* Scrum Guide
* Buenas prácticas ágiles


Herramientas:

* RAG sobre PDFs
* HuggingFace Embeddings 
* Modelo local: sentence-transformers/all-MiniLM-L6-v2
* ChromaDB


Ejemplos:

```text
¿Qué ceremonia sirve para alinear dependencias?
¿Cómo debería priorizar un backlog?
¿Qué diferencia hay entre épicas y features?
```

---

## 3. Subagente Jira Cloud

Especializado en consultas operativas.

Capacidades:

* Ejecutar queries JQL
* Obtener issues
* Consultar sprints
* Leer tableros Scrum 
* Analizar estados
* Crear historias de usuario
* Crear tareas
* Crear bugs
* Asistir mediante IA en la generación de contenido para issues
* Crear automáticamente issues reales en Jira Cloud
* Filtrar issues del sprint activo mediante etiquetas
* Generar reportes ejecutivos para stakeholders

Tecnologías:

* REST API Jira Cloud
* Requests
* LangChain

Ejemplos:

```text
¿Cuáles son los tickets bloqueantes?
Muéstrame los issues del sprint actual.
¿Qué tickets están en QA hace más de 5 días?
```


---
## 4. Futuras Integraciones Documentales

El roadmap contempla incorporar conectores documentales empresariales.

Próximas integraciones:
* Confluence
* Agregar observabilidad con LangSmith
* Ingesta documental 
* Indexación automática para RAG
* Consulta contextual sobre documentación funcional y técnica

---

# ⚙️ Stack Tecnológico

| Categoría            | Tecnología                       |
| -------------------- | -------------------------------- |
| Lenguaje             | Python                           |
| Framework de agentes | LangGraph                        |
| Framework IA         | LangChain                        |
| Modelos LLM          | Groq/ Gemini                     |
| Embeddings           | HuggingFace Embeddings           |
| Vector Store         | ChromaDB                         |
| APIs                 | Jira Cloud REST API / Notion API |
| Gestión de entorno   | python-dotenv                    |

---

# 📂 Estructura del Proyecto

```text
project/
│      
├── Agents/
│   ├── mentor/
│   ├── jira/
│   └── orchestrator/
│
├── App/
│   │
│   ├── rag/
│   │   │
│   │   ├── Documents/
│   │   │
│   │   ├── ingesta/
│   │   │   ├── cargadores.py
│   │   │   ├── chunking.py
│   │   │   ├── embeddings.py
│   │   │   ├── metadata.py
│   │   │   └── pipeline_de_ingesta.py
│   │   │
│   │   ├── recuperacion/
│   │   │   ├── busqueda_por_similitud.py
│   │   │   └── retriever.py
│   │   │
│   │   └── vectores/
│   │       └── chroma_store.py
│   │
│   └── scripts/
│       └── streamlit_app.py
│
├── Config/
│   ├── modelos.py
│
├── data_chroma_db/
│   └── chroma.sqlite3
│
├── Prompts/
│   ├── agente_1_mentor_rag_scrum.py
│   ├── prompt_agente_2_jira.py
│
├── Tools/
│   └── tools.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt

```

---
# 🧪 Entorno Jira de Pruebas

El proyecto incluye un entorno real de Jira Cloud utilizado para pruebas end-to-end de los agentes.

Este entorno permite validar:
* Creación automática de historias, bugs y tareas
* Ejecución real de queries JQL
* Lectura de sprints activos
* Filtrado por labels
* Generación de reportes automáticos
* Interacción real entre el agente y Jira Cloud

---

# 🛠️ Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/manuelpalomeque/rag-genai-product-owner-assistant
cd rag-genai-product-owner-assistant
```

## 2. Crear entorno virtual

```bash
python -m venv .venv
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

Crear archivo:

```text
.env
```

---

## 5. Ejecutar aplicación

```bash
python streamlit_app.py
```

---

# 📚 Roadmap

## MVP

* [x] Orquestador básico
* [x] Routing entre agentes
* [x] Integración Jira Cloud
* [x] RAG básico
* [ ] Integración Notion
* [ ] Persistencia de memoria
* [ ] Observabilidad completa con LangSmith

## Próximas mejoras

* [ ] Memoria conversacional persistente
* [ ] Multiusuario
* [ ] Dashboard analítico
* [ ] Agente de métricas ágiles
* [ ] Integración Slack/Discord
* [ ] Generación automática de retrospectivas
* [ ] Evaluación automática de prompts
* [ ] Testing de agentes

---


# 📖 Buenas Prácticas Implementadas

* Arquitectura desacoplada
* Separación entre agentes y tools
* Uso de herramientas tipadas
* Manejo explícito de estado
* Variables de entorno seguras
* Observabilidad integrada
* Prompts modulares
* Diseño escalable basado en grafos

---

# 🤝 Contribuciones

Las contribuciones son bienvenidas.

Sugerencias:

* Nuevos subagentes
* Mejoras en prompts
* Integraciones adicionales
* Optimización del routing
* Nuevas tools para Jira/Notion

---

# 📄 Licencia

MIT License

---

# 👨‍💻 Autor

**Jonathan Manuel Palomeque – Data Scientist & AI Developer**

Proyecto desarrollado como iniciativa de investigación y desarrollo sobre arquitecturas multi-agente aplicadas a Product Ownership y Agile Management.
