# main.py

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from neo4j_client import Neo4jClient
import logging
from typing import Optional
from contextlib import asynccontextmanager
from handle_unstructure_pdf import chunk_text
from agents.rag_agent import chat_agent
from models.schemas import Message, ChatResponse
from utils.async_utils import async_retry1
from asyncio import TimeoutError, wait_for
import uvicorn
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


neo4j_client = Neo4jClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up and ensuring Neo4j connection is ready.")
    # Initialize any other resources here if needed
    yield
    # Shutdown actions
    logger.info("Shutting down and closing Neo4j connection.")
    await neo4j_client.close()

# Apply lifespan to the app
app = FastAPI(
    title="Lyli - Document Management & Chatbot API",
    description="Combined endpoints for document management and RAG chatbot",
    lifespan=lifespan
)

# Re-add middleware after reinitializing app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"], # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Document Management Endpoints
# ============================

@app.post("/files", summary="Upload a new file")
async def create_file(
    file: UploadFile = File(...),
    link: str = Form(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
):
    """
    Upload a file, extract text, chunk it, and store in Neo4j.
    """
    try:
        # Save file temporarily
        temp_dir = "/tmp"  # Use an appropriate directory for temporary files
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, file.filename)

        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Process chunks
        chunks = chunk_text(temp_file_path)

        # Prepare metadata
        metadata = {
            "link": link,
            "description": description,
            "tags": tags.split(",") if tags else [],
        }

        # Store in Neo4j
        file_id = await neo4j_client.create_file_with_chunks(file.filename, chunks, link)

        # Cleanup temporary file
        os.remove(temp_file_path)

        return {
            "file_id": file_id,
            "filename": file.filename,
            "chunk_count": len(chunks),
            "link": link,
            "description": description,
            "tags": metadata["tags"],
        }

    except Exception as e:
        logger.error(f"Error in create_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files", summary="List all uploaded files")
async def list_files():
    """
    Retrieve a list of all uploaded files.
    """
    try:
        files = await neo4j_client.list_files()
        return files
    except Exception as e:
        logger.error(f"Error in list_files: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/{file_id}/chunks", summary="Get chunks of a specific file")
async def get_file_chunks(file_id: str):
    """
    Retrieve chunks of a specific file by its ID.
    """
    try:
        chunks = await neo4j_client.get_chunks_by_file(file_id)
        if not chunks:
            raise HTTPException(status_code=404, detail="File not found")
        return chunks
    except Exception as e:
        logger.error(f"Error in get_file_chunks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/files/{file_id}", summary="Delete a specific file")
async def delete_file(file_id: str):
    """
    Delete a specific file by its ID.
    """
    try:
        await neo4j_client.delete_file(file_id)
        return {"message": f"File {file_id} deleted successfully."}
    except Exception as e:
        logger.error(f"Error in delete_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================
# Chatbot Endpoints
# ============================

@async_retry1(max_retries=3, delay=1)
async def invoke_agent_with_retry(message: Message, timeout: int = 400):
    """
    Retry the agent if a tool fails to run. Helps with intermittent connection issues.
    """
    logger.info("Invoking chat agent with retry mechanism.")
    try:
        # Adding a timeout to ensure the query does not hang indefinitely
        response = await wait_for(
            chat_agent.ainvoke(
                {"input": message.text},
                {"configurable": {"session_id": message.session}}
            ),
            timeout=timeout
        )
        return response
    except TimeoutError:
        logger.error(f"Query timed out after {timeout} seconds.")
        raise
    except Exception as e:
        logger.error(f"Error invoking agent: {e}")
        raise


@app.get("/", summary="API Status")
async def get_status():
    """
    Check the status of the API.
    """
    return {"status": "running"}


@app.post("/docs-rag-agent", response_model=ChatResponse, summary="Chat with the RAG Agent")
async def ask_docs_agent(message: Message) -> ChatResponse:
    """
    Interact with the RAG chatbot.
    """
    try:
        # Call the agent with retry mechanism
        query_response = await invoke_agent_with_retry(message)

        if query_response is None:
            logger.error("invoke_agent_with_retry returned None after all retry attempts.")
            return ChatResponse(
                success=False,
                intermediate_steps=["No response from the agent."],
                output="Failed to get a response."
            )

        # Ensure 'intermediate_steps' exists in the response
        if "intermediate_steps" not in query_response:
            logger.error("Invalid response structure: 'intermediate_steps' key is missing.")
            query_response["intermediate_steps"] = ["No intermediate steps available."]

        # Process intermediate steps into strings if necessary
        try:
            query_response["intermediate_steps"] = [
                str(step) for step in query_response.get("intermediate_steps", [])
            ]
        except Exception as e:
            logger.error(f"Error processing 'intermediate_steps': {e}")
            query_response["intermediate_steps"] = ["Error processing intermediate steps."]

        # Construct the final response object
        final_response = ChatResponse(
            success=True,
            intermediate_steps=query_response.get("intermediate_steps", []),
            output=query_response.get("output", "No output text provided.")
        )
        logger.info("Chat agent response successfully processed.")
        return final_response

    except Exception as e:
        logger.error(f"Unexpected error in ask_docs_agent: {e}")
        return ChatResponse(
            success=False,
            intermediate_steps=["An unexpected error occurred."],
            output=str(e)
        )
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)