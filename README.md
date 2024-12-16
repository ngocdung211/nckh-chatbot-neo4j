
# Thai Binh Chatbot
*Chatbot Hỗ trợ tìm hiểu Điều lệ Đoàn Thanh niên Cộng sản Hồ Chí Minh khóa XII*

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [System Requirements](#system-requirements)  
4. [Installation & Setup](#installation--setup)  
5. [Usage](#usage)  
6. [Environment Configuration](#environment-configuration)  
7. [Troubleshooting & FAQ](#troubleshooting--faq)  
8. [License & Acknowledgments](#license--acknowledgments)

---

## 1. Overview
**Thai Binh Chatbot** is designed to assist users in exploring and understanding the **Điều lệ Đoàn Thanh niên Cộng sản Hồ Chí Minh (Khóa XII)**. It leverages modern NLP techniques, including **LangChain** and **Neo4j** graph databases, to provide contextual and accurate information. The chatbot uses the **OpenAI ChatGPT API** for generating responses.

### Purpose
- Provide **quick access** to key sections of the Điều lệ Đoàn TNCS Hồ Chí Minh Khóa XII.
- Offer a **user-friendly interface** for searching regulations, articles, and guidelines.
- Demonstrate **Python**, **LangChain**, and **Neo4j** integration in a conversational AI project.

---

## 2. Features
- **Conversational Interface**: Interactive Q&A about the Điều lệ Đoàn TNCS Hồ Chí Minh.
- **Neo4j Integration**: Stores and retrieves structured data for better context.
- **OpenAI ChatGPT API**: Generates natural language answers and explanations.
- **Command-Line Execution**: Straightforward commands to run the chatbot on Linux systems.

---

## 3. System Requirements
- **Operating System**: Linux (tested on Ubuntu, Debian, etc.).
- **Python Environment**: Python 3.10 is recommended.
- **Memory**: Minimum 2 GB RAM (4 GB or more recommended).
- **Neo4j**: NEO4J AURA instance.
- **Network**: Stable internet connection (for OpenAI ChatGPT API calls).

---

## 4. Installation & Setup
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/thanthienhai/thaibinh-chatbot
   cd thaibinh-chatbot
   ```
2.	**Create & Activate a Virtual Environment and nstall Dependencies**
    ```
    conda env create -f environment.yml -n thaibinhbot
    conda activate thaibinhbot
    ```
    If it does not work you can try:
    ```
    conda env create -f environment2.yml -n thaibinhbot
    conda activate thaibinhbot
    ```
    Eles:
    ```
    conda create -n thaitbinhbot
    conda activate thaibinhbot
    pip install -r requirements.txt   
    ```
3.	**Neo4j Setup**

    •	Ensure you have a running Neo4j instance (e.g., via Docker or a local installation).
    •	Obtain the URI, username, and password for your database.

3.	**Install Vietnamese language extraction on the Tesserat**
    ```
    ./create.sh
    ```
    **Note:** Add permisison for the entrypoint.sh before run
    ```
    chmod +x entrypoint.sh     
    ```

4.	**Usage**
    Start the chatbot api via the command line in folder thaitbinh-chatbot/src:
    ```
    ./entrypoint.sh
    ```
    Start the chatbot frontend via the command line in folder thaitbinh-chatbot/chatbot_frontend/src:
    ```
    ./entrypoint.sh
    ```
    **Note:** Add permisison for the entrypoint.sh before run
    ```
    chmod +x entrypoint.sh     
    ```
    Once running, the chatbot will prompt you for questions regarding Điều lệ Đoàn TNCS Hồ Chí Minh (Khóa XII). Queries will be processed by LangChain with data from Neo4j and enhanced by the ChatGPT API.
5.	**Environment Configuration**
    Create a file named .env (or set environment variables) containing:
    ```
    NEO4J_URI=
    NEO4J_USERNAME=
    NEO4J_PASSWORD=

    AURA_INSTANCEID=
    AURA_INSTANCENAME=

    OPENAI_API_KEY=
    OPENAI_EMBEDDING="text-embedding-3-small"

    AGENT_MODEL=gpt-4o-mini
    CYPHER_MODEL=gpt-4o-mini
    QA_MODEL=gpt-4o-mini
    TEST_MODEL=gpt-4o-mini

    ```
    Note: Keep this file secure and untracked. Use .gitignore to ensure it’s not committed.
