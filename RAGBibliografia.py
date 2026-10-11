import glob
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


def cargar_y_dividir_markdowns(directorio_md: str):
    """Carga archivos .md y los divide respetando la jerarquía de títulos y tamaño de bloque."""
    patron = os.path.join(directorio_md, "*.md")
    archivos = glob.glob(patron)

    print(f"Indexando {len(archivos)} archivos Markdown...")

    # Títulos de Markdown que se usarán como separadores lógicos
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150
    )

    docs_totales = []

    for filepath in archivos:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()

            # 1. División por estructura de encabezados
            md_splits = markdown_splitter.split_text(texto)

            # Preservar el nombre del archivo en los metadatos
            for doc in md_splits:
                doc.metadata["source"] = os.path.basename(filepath)

            # 2. Re-división por tamaño de caracteres para trozos homogéneos
            chunks = text_splitter.split_documents(md_splits)
            docs_totales.extend(chunks)
        except Exception as e:
            print(f"Error procesando {filepath}: {e}")

    print(f"Se crearon {len(docs_totales)} fragmentos (chunks) de texto.")
    return docs_totales


def crear_o_cargar_vectorstore(
    directorio_md: str, persist_directory: str = "./chroma_db"
):
    """Crea la base de datos vectorial en disco o la carga si ya existe."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    if os.path.exists(persist_directory):
        print("Cargando base de datos vectorial existente...")
        vectorstore = Chroma(
            persist_directory=persist_directory, embedding_function=embeddings
        )
    else:
        print("Creando nueva base de datos vectorial con ChromaDB...")
        docs = cargar_y_dividir_markdowns(directorio_md)
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=persist_directory,
        )
        print("Base de datos vectorial guardada exitosamente.")

    return vectorstore


def iniciar_chat_rag(vectorstore):
    """Inicia una sesión de preguntas y respuestas utilizando el RAG."""
    # Configurar el retriever para obtener los 4 fragmentos más relevantes
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # Instanciar el LLM local
    #llm = ChatOllama(model="llama3.2", temperature=0.1)
    llm = ChatOllama(model="qwen2.5:7b", temperature=0.1)

    # Prompt del RAG
    template = """
    Eres un asistente de investigación. Utiliza únicamente el siguiente contexto extraído de los artículos científicos para responder la pregunta.
    Si no sabes la respuesta o no está en el contexto, di honestamente que no la encuentras en los documentos.

    Contexto:
    {context}

    Pregunta: {question}

    Respuesta (en español y bien estructurada):
    """
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        # Formatea los fragmentos recuperados incluyendo su fuente
        resultado = []
        for d in docs:
            fuente = d.metadata.get("source", "Desconocido")
            resultado.append(f"[Fuente: {fuente}]\n{d.page_content}")
        return "\n\n---\n\n".join(resultado)

    # Pipeline LCEL (LangChain Expression Language)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("\n" + "=" * 50)
    print("  Sistema RAG sobre archivos Markdown Activo")
    print("  Escribe tu pregunta o 'salir' para finalizar.")
    print("=" * 50 + "\n")

    while True:
        pregunta = input("\nPregunta: ")
        if pregunta.lower() in ["salir", "exit", "quit"]:
            break

        if not pregunta.strip():
            continue

        print("\nConsultando documentos...")
        respuesta = rag_chain.invoke(pregunta)
        print(f"\nRespuesta:\n{respuesta}")


if __name__ == "__main__":
    CARPETA_MD = "./bibliografiamarkdown"
    DB_DIR = "./chroma_db_markdown"

    vectorstore = crear_o_cargar_vectorstore(
        directorio_md=CARPETA_MD, persist_directory=DB_DIR
    )
    iniciar_chat_rag(vectorstore)