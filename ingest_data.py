from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle

# Load data
ps = list(Path("Notion_DB").glob("**/*.md"))

data = []
sources = []

for p in ps:
    with open(p, "r") as f:
        data.append(f.read())
    sources.append(p)

# Split data
# Here we split the documents, as needed, into smaller chunks.
# We do this due to the context limits of the LLMs.
text_splitter = CharacterTextSplitter(
    chunk_size=1500, chunk_overlap=300, separator="\n"
)

docs = []
metadatas = []

for i, d in enumerate(data):
    splits = text_splitter.split_text(d)
    docs.extend(splits)

    metadatas.extend([{"source": sources[i]}] * len(splits))


# Create vector store from data and save it to disk
vectorstore = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
faiss.write_index(vectorstore.index, "docs.index")
vectorstore.index = None

with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)
