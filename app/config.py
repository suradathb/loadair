import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://bondnuy007:xWt0w8D0NjvbvlvM@isansoftdb.coskaoq.mongodb.net/?retryWrites=true&w=majority&appName=IsanSoftDB")
DB_NAME = os.getenv("loadair_db", "quotation_db")
