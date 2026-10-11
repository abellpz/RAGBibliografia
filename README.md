# 📚 Local RAG System for Markdown Documents with LangChain & Ollama

Sistema de Recuperación y Generación Aumentada (**RAG**) 100% local diseñado para indexar, procesar y chatear con una colección de archivos Markdown (`.md`). Utiliza **LangChain**, **ChromaDB** como base de datos vectorial y **Ollama** para ejecutar modelos de lenguaje y embeddings de forma completamente privada y sin depender de APIs externas.

---

## 🚀 Características Principales

* **100% Local y Privado:** Sin costos por API ni fugas de datos. Todo corre en tu máquina usando Ollama.
* **Procesamiento Inteligente de Markdown:** Divide los documentos respetando su jerarquía de encabezados (`#`, `##`, `###`) usando `MarkdownHeaderTextSplitter` y trozos uniformes con `RecursiveCharacterTextSplitter`.
* **Atribución de Fuentes:** Cada respuesta indica explícitamente el archivo Markdown de origen del cual se extrajo la información.
* **Persistencia Eficiencia:** Crea la base de datos vectorial en disco la primera vez y la carga automáticamente en ejecuciones posteriores.
* **Pipeline LCEL:** Construido utilizando *LangChain Expression Language* para flujos limpios, legibles y modulares.

---

## 🛠️ Requisitos Previos

1. **Python 3.10 o superior** instalado en tu sistema.
2. **Ollama** instalado y ejecutándose en tu máquina. Puedes descargarlo desde [ollama.com](https://ollama.com/).

### Modelos de Ollama necesarios
Ejecuta los siguientes comandos en tu terminal para descargar los modelos predeterminados del script:

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:7b
```
### 📦 Instalación
Clona este repositorio o copia el script en tu proyecto.

Instala las dependencias necesarias de Python:
```bash
pip install langchain langchain-community langchain-ollama chromadb
```
### 📂 Estructura del Proyecto
Asegúrate de tener una estructura de carpetas similar a esta antes de ejecutar el script:
```
mi-proyecto-rag/
│
├── RAGBibliografia.py                 # Script principal de Python
├── bibliografiamarkdown/     # Carpeta con tus archivos .md a indexar
│   ├── documento_1.md
│   └── documento_2.md
└── chroma_db_markdown/       # Base de datos vectorial persistente (se crea sola)
```

### ⚙️ Uso
Coloca tus archivos Markdown dentro de la carpeta ./bibliografiamarkdown (o modifica la ruta en la sección if __name__ == "__main__": del script).

Ejecuta el script:
```bash
python RAGBibliografia.py
```

1. Una vez inicializado el sistema y cargados los documentos, podrás interactuar mediante la consola:
```
==================================================
  Sistema RAG sobre archivos Markdown Activo
  Escribe tu pregunta o 'salir' para finalizar.
==================================================
```
Pregunta: ¿Cuáles son las conclusiones principales del estudio sobre IA?

Consultando documentos...

Respuesta:
[Fuente: documento_1.md]
Las conclusiones principales indican que...


Para salir de la sesión interactiva, simplemente escribe salir, exit o quit.

### 🔧 Personalización
Puedes modificar parámetros clave directamente en el código según tus necesidades:

Modelo LLM: Cambia el modelo en iniciar_chat_rag (por defecto usa qwen2.5:7b, pero puedes cambiarlo a llama3.2 o el que prefieras).

Tamaño de Fragmentos (Chunks): Ajusta chunk_size=1000 y chunk_overlap=150 en la función cargar_y_dividir_markdowns para cambiar la granularidad de los textos indexados.

Número de fragmentos recuperados: Modifica search_kwargs={"k": 4} para traer más o menos contexto por consulta.

### 📄 Licencia
Este proyecto está bajo la licencia MIT. Siéntete libre de usarlo, modificarlo y adaptarlo para tus proyectos de investigación o desarrollo personal.
