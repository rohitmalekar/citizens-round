import os
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from IPython.display import Markdown, display

documents = SimpleDirectoryReader('data').load_data()
index = GPTVectorStoreIndex(documents)

# save to disk
index.save_to_disk('index.json')

# load from disk
index = GPTVectorStoreIndex.load_from_disk('index.json')

response = index.query("What is Citizens Round?")
print(response)
