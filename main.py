from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from chromadb.utils import embedding_functions
import chromadb.utils.embedding_functions as embedding_functions
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from termcolor import colored
from pyfiglet import Figlet
import chromadb
import os


DATA_PATH = "data"
def loadDocuments():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    return documents

docs = loadDocuments()

textSplitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 500,
    length_function = len,
    add_start_index = True
)

chunks = textSplitter.split_documents(docs)
chroma_client = chromadb.Client()

load_dotenv()

API_KEY = os.environ.get('OPENAI_API_KEY')

# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key=API_KEY,
#                 model_name="text-embedding-ada-002"
#             )

# collection = chroma_client.get_or_create_collection(name="my_collection", embedding_function=openai_ef)
collection = chroma_client.get_or_create_collection(name="my_collection", metadata={"hnsw:space": "cosine"})

# Prepare the data for insertion
documents = []
metadatas = []
ids = []

for chunk in chunks:
    documents.append(chunk.page_content)
    metadatas.append(chunk.metadata)
    if len(ids) == 0:
        ids.append(0)
    else:
        ids.append(ids[-1] + 1)

ids_str = []
for id in ids:
    ids_str.append(str(id))

# Insert the data into the collection
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids_str
)

model = ChatOpenAI(model="gpt-3.5-turbo")
f = Figlet()
print(f.renderText('findit'))

print("Hello I'm " + colored("netwon", "red", attrs=["blink"]) + " your smart bot to find the files you want.\n")

while(1):
    query_txt = input(colored("Enter Prompt:", "blue", "on_white") + " ")
    results = collection.query(query_texts=[query_txt], n_results=5)

    PROMPT_TEMPLATE = """
    Answer the question based only only on the following context:
    {context} 
    ---
    Answer the question based in the above context: {query}
    """

    context_text = "\n\n--\n\n".join([doc for doc in results['documents'][0]])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, query=query_txt)

    response_text = model.invoke(prompt)
    print(colored('newton :', 'red', "on_white"), colored(response_text.content + "\n\n", 'green'))

    results_ = collection.query(query_texts=["Just name the sources of the files"+ response_text.content], n_results=5)
    sources = [src['source'] for i, src in enumerate(results_["metadatas"][0]) if results_["distances"][0][i] <= 0.5]

    print(results_)
    print(results_["distances"][0])

    if len(set(sources)) == 0:
        print(colored("sources: ", 'green'), "No relevant sources found")
    else:
        print(colored("sources: ", 'green'), str(set(sources)))
    print("\n")