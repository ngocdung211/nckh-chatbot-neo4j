import os
from typing import Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from typing import List, Dict, Any
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_community.chat_message_histories import Neo4jChatMessageHistory

from chains.semantic_search_chunk_chain import get_chunk_retriever

from tools.tools import get_customer_service_infor
from llm.get_graph import get_graph_function
from langchain_core.runnables.history import RunnableWithMessageHistory
from llm.get_ollma_model import get_ollama_llama3_model



print("✅✅call agent step")

graph = get_graph_function()
model = get_ollama_llama3_model()

@tool 
def get_chunk_tool(question: str) -> str:
    "Search for information about the 'Đoàn thanh niên, hội sinh viên' . For any questions in the about 'Đoàn thành niên, hội sinh viên', you must use this tool!"
    result =  get_chunk_retriever().invoke(question)
    print(result)
    return result

@tool
def get_customer_service() -> str:
    """
    Retrieve contact information for customer service.
    
    Example:
    "How can I contact customer service?"
    """
    return get_customer_service_infor()


agent_tools = [

    get_chunk_tool,
    get_customer_service,
    # get_from_database,
 
]
def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Frist you awnser normal direct anwser the question of user if it seem does not satisfied you can you the function tools.
            You are a chatbot assisting users with questions about the Ho Chi Minh Communist Youth Union and the Communist Party of Vietnam. Based on provided documents:
                1.	Answer questions: Focus on organization, duties, operations, and the Charter.
                2.	Accurate language: Use a formal tone, keep answers precise and relevant.
                3.	Stay within materials: If information is missing, recommend other sources.
                4.	Polite responses: Use clear formats for processes or lists, and encourage follow-up questions.
                5.	Reference sources: Include metadata in this format: Document name - Page number - [Link to metadata].
             IMPORTANT: Your anwser must be in Vietnamese
            Previous conversation history:
            """
        ),
        

        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent_llm_with_tools = model.bind_tools(agent_tools)

rag_agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
        
    }
    | agent_prompt
    | agent_llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

rag_agent_executor = AgentExecutor(
    agent=rag_agent,
    tools=agent_tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
)

chat_agent = RunnableWithMessageHistory(
    rag_agent_executor,
    get_memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)
def get_agent():
    return chat_agent
