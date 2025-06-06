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
from llm.get_llm import get_model_function
from langchain_core.runnables.history import RunnableWithMessageHistory



print("✅✅call agent step")

graph = get_graph_function()
model = get_model_function()
@tool 
def get_chunk_tool(question: str) -> str:
    "Search for information about the 'Đoàn thanh niên, hội sinh viên' . For any questions in the about 'Đoàn thành niên, hội sinh viên', you must use this tool!"
    result =  get_chunk_retriever(name='openai').invoke(question)
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
           1. Main Responsibilities:
            •	Answer questions related to the Information Technology Faculty at Hanoi University of Industry. 
                Provide responses about activities, training programs, and student life.
            •	Only answer based on information provided in the supplied documents.

        2. Mandatory Requirements:
            •	Information Limitations:
            •	If the information is not available in the documents, respond with: 
                “I do not have this information” and recommend that the user refer to other sources.

        3. Instructions for Tool Usage:

        NOTE: You must use the tool to query data and base your answers on the query results.
            •	Upon receiving a question:
            1.	Use the tool with a rewritten version of the question to find relevant context.
            •	Processing tool results:
            •	If the context is not empty (e.g., not []), provide an answer based on the retrieved context.
            •	If the context is empty ([]), retry with different tools or keywords and suggest that the user 
                clarify their question or provide more specific context.
            •	If no answer is found after multiple attempts, provide contact 
                information for customer service via the customer_service() tool.

        4. Answer Formatting:
            •	Language: Vietnamese
            •	Use formal, objective, and easy-to-understand language.
            •	Formatting:
            •	Use lists or step-by-step explanations when describing a process.
            •	Content should be returned in markdown format.
            •	Do not include consecutive line breaks, such as \n\n.
            •	Provide concise but complete explanations.
            •	Source Citations:
            •	Include references at the end of the answer in the following format:
        [Document Name] - [Page Number] - [**Reference Link**](Link from metadata).
        Example: [Giải thưởng khoa công nghệ thông tin] - [**Reference Link**](https://drive.google.com/file/d/1g5BnGtdS5vp7TKad4ua0tdRdRQo4hJZW/view).

        5. Interaction Suggestions:
            •	At the end of each response, encourage the user to ask further related 
                questions or provide necessary information. Inform them that if they encounter issues, they can contact support for assistance.

        Previous Conversation History:
            """
        ),
        

        ("user", " Với các thông tin về trường đại học công nghiệp và khoa công nghệ thông tin tôi cần tiềm hiểu về hoạt động khóa, các hoạt động đoàn hội. {input}"),
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

# chat_agent = RunnableWithMessageHistory(
#     rag_agent_executor,
#     input_messages_key="input"
# )
def get_agent():
    return rag_agent_executor
