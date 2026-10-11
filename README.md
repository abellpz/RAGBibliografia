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
