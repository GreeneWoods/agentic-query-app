import chromadb
from chromadb.config import Settings
from config import settings


client = chromadb.PersistentClient(path='./chromadb_data', settings=Settings(allow_reset=True))
# client.reset()

leads_collection = client.get_or_create_collection(settings.base_collection)