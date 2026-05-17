# backend/app.py

import os
import sys
import io
import chromadb
import pandas as pd

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Document,
    Settings
)

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core.agent.workflow import FunctionAgent



sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from backend.tool import (
    calculate_speed_fine,
    mock_toll_wallet_deduction
)



app = FastAPI(title="Smart Toll AI Agent System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



API_KEY = "AIzaSyAx6CIKP1AsOz6_M9yLQyb3a-VqdAAqCnU"

google_llm = GoogleGenAI(
    model="gemini-2.5-flash",
    api_key=API_KEY
)

google_embed = GoogleGenAIEmbedding(
    model="models/text-embedding-004",
    api_key=API_KEY
)

Settings.llm = google_llm
Settings.embed_model = google_embed



os.makedirs("data", exist_ok=True)

law_file_path = os.path.join(
    "data",
    "traffic_laws.txt"
)

if os.path.exists(law_file_path):

    with open(
        law_file_path,
        "r",
        encoding="utf-8"
    ) as f:

        law_text_content = f.read()

else:

    law_text_content = """
    Overspeeding:
    Fine depends on exceeded speed.

    Parking Violation:
    Fine = 500

    Honking Violation:
    Fine = 300

    Triple Riding:
    Fine = 1000
    """


db_client = chromadb.PersistentClient(
    path="chroma_db_storage"
)

chroma_collection = db_client.get_or_create_collection(
    "isolated_traffic_laws_v2"
)

vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

print("[Backend] Indexing traffic laws into ChromaDB...")


clean_document = Document(
    text=law_text_content,
    doc_id="static_smart_city_law_book"
)

index = VectorStoreIndex.from_documents(
    [clean_document],
    storage_context=storage_context,
    embed_model=google_embed
)

query_engine = index.as_query_engine()

print("[Backend] ChromaDB initialization complete.")



def lookup_traffic_laws(
    violation_description: str
) -> str:

    """
    Search traffic law database
    """

    result = query_engine.query(
        violation_description
    )

    return str(result)



agent = FunctionAgent(

    name="toll_inspector_agent",

    description="""
    Intelligent traffic enforcement AI system
    """,

    tools=[
        lookup_traffic_laws,
        calculate_speed_fine,
        mock_toll_wallet_deduction
    ],

    llm=google_llm
)



@app.post("/process-toll/")
async def process_toll(

    vehicle_id: str,
    file: UploadFile = File(...)

):
    try:
        agent_response = await agent.run(
            execution_prompt
        )

        return {
            "status": "success",
            "vehicle_id": vehicle_id,
            "report": str(agent_response)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }