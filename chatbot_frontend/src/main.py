import os
import requests
import streamlit as st
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

def get_session_id():
    return get_script_run_ctx().session_id

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8081/docs-rag-agent")

with st.sidebar:

    st.header("Một số câu hỏi thường gặp")
    st.markdown("- Đoàn Thanh niên Cộng sản Hồ Chí Minh được tổ chức theo mấy cấp? Đó là những cấp nào?")
    st.markdown("- Đoàn viên Đoàn Thanh niên Cộng sản Hồ Chí Minh có độ tuổi giới hạn là bao nhiêu?")
    st.markdown("- Quy trình kết nạp một đoàn viên mới bao gồm những bước nào?")
    st.markdown("- Đoàn Thanh niên Cộng sản Hồ Chí Minh giữ vai trò gì trong Hội Liên hiệp Thanh niên Việt Nam và Đội Thiếu niên Tiền phong Hồ Chí Minh?")
    st.markdown("- Nguồn tài chính của Đoàn đến từ đâu?")
    st.markdown("- Những hình thức khen thưởng nào được áp dụng cho đoàn viên và tổ chức Đoàn?")
    st.markdown("- Trong trường hợp đoàn viên vi phạm, có những hình thức kỷ luật nào được quy định?")
    st.markdown("- Thông tin người hỗ trợ là gì?")

st.title("Chatbot Hỗ trợ học tập (chưa có dữ liệu - sử dụng dữ liệu của đoàn))")
st.info(
    """Tôi là một chatbot sẽ hỗ trợ bạn tìm hiểu thông tin về Đại học Công nghiệp Hà Nội. Các thông tin có thể liên quan đến học phí, môn học,.."""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("Cách tạo nội dung này", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("Bạn muốn biết gì?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {
    "text": prompt,
    "session": get_session_id()
}

    with st.spinner("Đang tìm kiếm câu trả lời..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """Đã xảy ra lỗi khi xử lý tin nhắn của bạn.
            Điều này thường có nghĩa là chatbot không thể tạo truy vấn để
            trả lời câu hỏi của bạn. Vui lòng thử lại hoặc thay đổi cách diễn đạt câu hỏi."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("Cách tạo nội dung này?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
