import chromadb
from config import settings


client = chromadb.Client()

leads_collection = client.get_or_create_collection(settings.base_collection)