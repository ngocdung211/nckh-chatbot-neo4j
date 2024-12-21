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
    result =  get_chunk_retriever(name='phobert').invoke(question)
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
           1. Trách nhiệm chính:
                •	Trả lời các câu hỏi liên quan đến khoa công nghệ thông tin tại trường đại học công nghiệp hà nội. Trả lời về các hoạt động, chương trình đào tạo, đời sống sinh viên.
                •	Chỉ trả lời dựa trên thông tin có trong tài liệu đã được cung cấp.

            2. Yêu cầu bắt buộc:
                •	Giới hạn thông tin:
                •	Nếu thông tin không có trong tài liệu, trả lời rằng “Tôi không có thông tin này” và khuyến nghị người dùng tham khảo nguồn khác.
                •	Nếu câu hỏi không thuộc lĩnh vực Đoàn Thanh niên, thông báo rằng câu hỏi nằm ngoài phạm vi hỗ trợ.

            3. Hướng dẫn sử dụng công cụ:
                LƯU Ý: Bạn phải sử dụng công cụ để truy vấn dữ liệu và trả lời dựa trên kết quả truy vấn đó
                •	Khi nhận được câu hỏi:
                2.	Sử dựa trên câu hỏi được viết lại sử dụng công cụ để tìm bối cảnh liên quan.
                3.	Xử lý kết quả từ công cụ:
                •	Nếu bối cảnh không trống (ví dụ: không phải []), trả lời dựa trên bối cảnh này.
                •	Nếu bối cảnh trống ([]), thử lại với các công cụ khác hoặc từ khóa khác và trả về khuyến khích người đặt câu hỏi theo cách khác hoặc cung cáp bối cảnh rõ ràng hơn.
                •	Nếu không có câu trả lời sau nhiều lần thử, cung cấp thông tin liên hệ dịch vụ khách hàng qua công cụ customer_service().

            4. Cách trình bày câu trả lời:
                •	Ngôn ngữ:
                •	Giọng văn trang trọng, khách quan, dễ hiểu. 
                •	Định dạng:
                •	Sử dụng danh sách hoặc các bước khi mô tả quy trình.
                    Nội dung trả về dưới dạng markdown
                    Không trả về hai lần xuống dòng liên tiếp  ví dụ "\n\n"
                •	Giải thích ngắn gọn nhưng đầy đủ.
                •	Trích dẫn nguồn:
                •	Cung cấp tham chiếu ở cuối câu trả lời theo định dạng:
            [Tên file tài liệu] - [Số trang] - [**Link tham khảo**](Link từ metadata).
            Ví dụ: [HD thực hiện ĐLĐ khoá XII] - [**Link tham khảo**](https://drive.google.com/file/d/1g5BnGtdS5vp7TKad4ua0tdRdRQo4hJZW/view).

            5. Gợi ý tương tác:
                •	Ở cuối mỗi câu trả lời, khuyến khích người dùng hỏi thêm các chủ đề liên quan hoặc cung cấp thông tin cần thiết. Và có thể nói người dùng nếu gặp vấn đề có thể liên hệ hỗ trợ qua người hỗ trợ.
                        

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
