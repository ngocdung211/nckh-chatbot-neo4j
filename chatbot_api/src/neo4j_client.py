# neo4j_client.py

from neo4j import AsyncGraphDatabase
import os
from dotenv import load_dotenv
import uuid
import logging
import asyncio

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self, uri=None, user=None, password=None):
        self._uri = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        self._user = user or os.environ.get("NEO4J_USER", "neo4j")
        self._password = password or os.environ.get("NEO4J_PASSWORD", "test")
        self._driver = AsyncGraphDatabase.driver(self._uri, auth=(self._user, self._password))
        logger.info("Connected to Neo4j (Async)")

    async def close(self):
        if self._driver:
            await self._driver.close()
            logger.info("Neo4j connection closed (Async)")

    async def run_query(self, query, parameters=None):
        async with self._driver.session() as session:
            result = await session.run(query, parameters)
            records = []
            async for record in result:
                records.append(record.data())
            # print(records)
        return records

    async def create_file_with_chunks(self, filename, chunks,link):
        # Generate a unique file_id using UUID4
        file_id = f"{filename}_{uuid.uuid4()}"
        
        async with self._driver.session() as session:
            await session.write_transaction(self._create_file_and_chunks_tx, file_id, filename, chunks,link)
        
        logger.info(f"Created File node with file_id: {file_id}")
        return file_id

    @staticmethod
    async def _create_file_and_chunks_tx(tx, file_id, filename, chunks, link="demo_link"):
        # Create the File node
        await tx.run("""
        CREATE (f:File {file_id: $file_id, filename: $filename, link: $link, upload_date: datetime() })
        """, file_id=file_id, filename=filename, link=link)
        
        prev_chunk_id = None
        for chunk in chunks:
            # Construct a unique chunk_id based on file_id and chunk["chunk_id"]
            page_number = chunk["metadata"]["page_number"] # could be None or an integer
            element_id = chunk["metadata"]["element_id"]
            c_id = f"{filename} +page_+{page_number}+_+ {element_id}"
            text = chunk["page_content"]  # Ensure consistency with chunking function

            await tx.run("""
            MATCH (f:File {file_id: $file_id})
            CREATE (c:Chunk {chunk_id: $chunk_id, text: $text, page_number: $page_number})
            CREATE (f)-[:HAS_CHUNK]->(c)
            """, file_id=file_id, chunk_id=c_id, text=text, page_number=page_number)
            
            # Link the previous chunk
            if prev_chunk_id is not None:
                await tx.run("""
                MATCH (c1:Chunk {chunk_id: $prev_chunk_id}), (c2:Chunk {chunk_id: $chunk_id})
                CREATE (c1)-[:HAS_NEXT]->(c2)
                CREATE (c2)-[:HAS_PREV]->(c1)
                """, prev_chunk_id=prev_chunk_id, chunk_id=c_id)
            
            prev_chunk_id = c_id
        
        logger.info(f"Inserted {len(chunks)} chunks for file_id: {file_id}")

    async def list_files(self):
        query = """
        MATCH (f:File) 
        RETURN f.file_id as file_id, f.filename as filename, f.upload_date as upload_date 
        ORDER BY f.upload_date DESC
        """
        files = await self.run_query(query)

        logger.info(f"Retrieved {len(files)} files")
        return files

    async def get_chunks_by_file(self, file_id):
        query = """
        MATCH (f:File {file_id: $file_id})-[:HAS_CHUNK]->(c:Chunk)
        RETURN c.chunk_id as chunk_id, c.text as text, c.order as order, c.page_number as page_number
        ORDER BY c.order ASC
        """
        chunks = await self.run_query(query, {"file_id": file_id})
        logger.info(f"Retrieved {len(chunks)} chunks for file_id: {file_id}")
        return chunks

    async def delete_file(self, file_id):
        query = """
        MATCH (f:File {file_id: $file_id})-[:HAS_CHUNK]->(c:Chunk)
        DETACH DELETE c, f
        """
        await self.run_query(query, {"file_id": file_id})
        logger.info(f"Deleted File node and associated Chunks for file_id: {file_id}")