from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os 
import json

# load api key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# load models
embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
llm = ChatGoogleGenerativeAI( model="gemini-3.6-flash", max_tokens=1000)

def loadData():
    # load pdf
    pdf_link = "../data/manual.pdf"
    loader = PyPDFLoader(pdf_link, extract_images=False)
    pages = loader.load_and_split()

    # separate chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(pages)

    # save vector DB - Chroma
    db = Chroma.from_documents(chunks, embedding=embedding_model)

    # load vector DB - Chroma
    vectordb = Chroma(persist_directory="text_index", embedding_function=embedding_model)

    # load retriever (top 3 relevant documents)
    retriever = vectordb.as_retriever(search_kwargs={"k":3})

    return retriever

def getRelevantDocs(question):
    retriever = loadData()
    context = retriever.invoke(question)

    return context


def ask(question, llm):

    TEMPLATE = """
        Você é um técnico que não sabe nada sobre como lidar com PDFs, mas olhando o manual consegue entender as ideias 
        e tirar dúvidas dos clientes, sem o contexto do manual você não sabe resolver.
        Além disso, responde tudo com muita preguiça.

        Contexto: {context}
        Query: {question}
    """

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=TEMPLATE
    )

    sequence = RunnableSequence(prompt | llm)
    context = getRelevantDocs(question)
    response = sequence.invoke({"context": context, "question": question})

    return response

def lambda_handler(event, context):
    body = json.loads(event.get("body", {}))
    query = body.get("question")
    response = ask(query, llm).content

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "messsage": "Tarefa concluída com sucesso",
            "details": response
        })
    }

