import streamlit as st
import requests
import math
import os
import uuid
# Adjust API URLs as needed
API_URL = "http://localhost:8081"  # Base URL without /documentsCHATBOT_URL = "http://localhost:8000/chatbot/docs-rag-agent"
CHATBOT_URL = "http://localhost:8081/docs-rag-agent"  # Direct endpoint
# Initialize session state variables
if 'chunk_page' not in st.session_state:
    st.session_state.chunk_page = 1
if 'current_file_id' not in st.session_state:
    st.session_state.current_file_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

def get_session_id():
    return st.session_state.get("session_id", "default_session")

# Main Title
st.title("Multi-Screen Application")

# Sidebar Navigation
main_action = st.sidebar.selectbox("Navigate to", ["Document Management", "Chatbot"])

# ============================
# Document Management Screen
# ============================
if main_action == "Document Management":
    st.header("Document Management for RAG Preparation")
    
    # Sub-navigation for Document Management actions
    action = st.selectbox("Select Action", ["List Files", "Upload File", "View Chunks", "Delete File"])
    
    if action == "Upload File":
        st.subheader("Upload a File")
        
        # Optional: Collect metadata (e.g., description)
        with st.expander("Add File Metadata (Optional)"):
            file_description = st.text_input("File Description")
            tags = st.text_input("Tags (comma-separated)")
        
        # File uploader
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx", "md"])
        
        if uploaded_file is not None:
            # Display file details
            st.write("**File Details:**")
            st.write(f"- **Original Name:** {uploaded_file.name}")
            st.write(f"- **Type:** {uploaded_file.type}")
            st.write(f"- **Size:** {uploaded_file.size / (1024 * 1024):.2f} MB")
            
            # Editable fields for File Name and Link of File
            st.markdown("### Edit File Details")
            edited_file_name = st.text_input("File Name", value=uploaded_file.name)
            file_link = st.text_input("Link of File", value=f"http://localhost:8000/files/{edited_file_name}")
            
            # Optional: Validate file size (e.g., max 10MB)
            max_size_mb = 10
            if uploaded_file.size > max_size_mb * 1024 * 1024:
                st.error(f"File size exceeds the maximum limit of {max_size_mb} MB.")
            else:
                # Confirm upload
                if st.button("Upload"):
                    with st.spinner("Uploading file..."):
                        try:
                            # Prepare files and optional metadata
                            files = {
                                "file": (edited_file_name, uploaded_file.getvalue(), uploaded_file.type)
                            }
                            
                            # Prepare additional data if metadata is provided
                            data = {
                                "link": file_link,  # Ensure this is provided
                                "description": file_description,  # Optional field
                                "tags": ",".join(tags) if tags else ""  # Optional field, joined as comma-separated string
                            }
                            response = requests.post(f"{API_URL}/files", files=files, data=data)
                            
                            if response.status_code == 200:
                                resp_json = response.json()
                                st.success(f"File uploaded successfully: **{resp_json['filename']}**")
                                st.info(f"**File ID:** {resp_json['file_id']} | **Chunks:** {resp_json['chunk_count']}")
                                st.write(f"**Access Link:** [View File]({file_link})")
                            else:
                                # Attempt to extract error message from response
                                try:
                                    error_detail = response.json().get("detail", response.text)
                                except ValueError:
                                    error_detail = response.text
                                st.error(f"Error uploading file: {error_detail}")
                        
                        except requests.exceptions.RequestException as e:
                            st.error(f"An error occurred while uploading the file: {e}")
    
    elif action == "List Files":
        st.subheader("List of Uploaded Files")
        resp = requests.get(f"{API_URL}/files")
        if resp.status_code == 200:
            files = resp.json()
            if files:
                # Pagination
                page_size = 5
                total = len(files)
                total_pages = math.ceil(total / page_size)
                
                # Ensure the current page is within valid range
                if st.session_state.chunk_page > total_pages:
                    st.session_state.chunk_page = total_pages if total_pages > 0 else 1
                
                page = st.number_input("Page", min_value=1, max_value=total_pages, value=st.session_state.chunk_page, step=1)
                st.session_state.chunk_page = page  # Update session state
                
                start = (page - 1) * page_size
                end = start + page_size
                for f in files[start:end]:
                    st.write(f"**File ID**: {f['file_id']} | **Filename**: {f['filename']}")
                st.write(f"Page {page} of {total_pages}")
            else:
                st.write("No files found.")
        else:
            st.error("Failed to retrieve files.")
    
    elif action == "View Chunks":
        st.subheader("View Chunks of a File")
        
        # Input for File ID
        file_id = st.text_input("Enter File ID", value=st.session_state.get("current_file_id", ""))
        
        if st.button("View Chunks") and file_id:
            st.session_state.current_file_id = file_id  # Save the current file ID in session state
            st.session_state.chunk_page = 1  # Reset pagination to page 1
            try:
                # Fetch chunks from the API
                resp = requests.get(f"{API_URL}/files/{file_id}/chunks")
                if resp.status_code == 200:
                    chunks = resp.json()
                    st.session_state.chunks = chunks  # Save chunks in session state
                    if not chunks:
                        st.warning("No chunks found for this file.")
                else:
                    st.error(f"Error fetching chunks: {resp.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
        
        # Check if chunks are loaded in session state
        if "chunks" in st.session_state and st.session_state.chunks:
            chunks = st.session_state.chunks
            chunk_page_size = 3  # Number of chunks per page
            chunk_total = len(chunks)
            total_chunk_pages = math.ceil(chunk_total / chunk_page_size)
            
            # Ensure current page is valid
            st.session_state.chunk_page = max(1, min(st.session_state.chunk_page, total_chunk_pages))
            
            # Calculate start and end indices
            chunk_start = (st.session_state.chunk_page - 1) * chunk_page_size
            chunk_end = chunk_start + chunk_page_size
            current_chunks = chunks[chunk_start:chunk_end]
            
            # Display current page info
            st.write(f"Page {st.session_state.chunk_page} of {total_chunk_pages}")
            
            # Display chunks for the current page
            for c in current_chunks:
                st.subheader(f"Chunk Order: {chunks.index(c)}")
                st.text_area("Chunk Text", c['text'], height=200)
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("Previous", key="prev_button"):
                    if st.session_state.chunk_page > 1:
                        st.session_state.chunk_page -= 1
                        st.rerun()
            with col3:
                if st.button("Next", key="next_button"):
                    if st.session_state.chunk_page < total_chunk_pages:
                        st.session_state.chunk_page += 1
                        st.rerun()
    
    elif action == "Delete File":
        st.subheader("Delete a File")
        file_id = st.text_input("Enter File ID to delete")
        if st.button("Delete"):
            resp = requests.delete(f"{API_URL}/files/{file_id}")
            if resp.status_code == 200:
                st.success("File deleted successfully.")
            else:
                st.error(resp.text)

# ============================
# Chatbot Screen
# ============================
elif main_action == "Chatbot":
    st.header("Chatbot Hỗ trợ tìm hiểu Điều lệ Đoàn Thanh niên Cộng sản Hồ Chí Minh khóa XII")
    st.info(
        """Tôi là một chatbot sẽ hỗ trợ bạn tìm hiểu thông tin về Điều lệ Đoàn Thanh niên Cộng sản Hồ Chí Minh khóa XII, bao gồm các quy định cơ bản về tổ chức, hoạt động, nhiệm vụ và quyền hạn của các cấp bộ Đoàn"""
    )
    
    # FAQ Section in Sidebar (optional, can be moved to main area if preferred)
    st.sidebar.header("Một số câu hỏi thường gặp")
    faqs = [
        "Đoàn Thanh niên Cộng sản Hồ Chí Minh được tổ chức theo mấy cấp? Đó là những cấp nào?",
        "Đoàn viên Đoàn Thanh niên Cộng sản Hồ Chí Minh có độ tuổi giới hạn là bao nhiêu?",
        "Quy trình kết nạp một đoàn viên mới bao gồm những bước nào?",
        "Đoàn Thanh niên Cộng sản Hồ Chí Minh giữ vai trò gì trong Hội Liên hiệp Thanh niên Việt Nam và Đội Thiếu niên Tiền phong Hồ Chí Minh?",
        "Nguồn tài chính của Đoàn đến từ đâu?",
        "Những hình thức khen thưởng nào được áp dụng cho đoàn viên và tổ chức Đoàn?",
        "Trong trường hợp đoàn viên vi phạm, có những hình thức kỷ luật nào được quy định?",
        "Thông tin người hỗ trợ là gì?"
    ]
    for faq in faqs:
        st.sidebar.markdown(f"- {faq}")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "output" in message:
                st.markdown(message["output"])
            if "explanation" in message:
                with st.status("Cách tạo nội dung này", state="complete"):
                    st.info(message["explanation"])
    
    # Chat input
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
                output_text = response.json().get("output", "Không có phản hồi từ chatbot.")
                explanation = response.json().get("intermediate_steps", "Không có giải thích thêm.")
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