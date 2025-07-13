
# A Retrieval-Augmented Generation Approach Utilizing Graph Databases and Large Language Models for Student Assistance Chatbot Systems

## Abstract
This research implements a **Retrieval-Augmented Generation (RAG)** system using Neo4j graph databases and Vietnamese-specific embedding models for student assistance at Hanoi University of Industry. The system combines **PhoBERT**, **Vietnamese-bi-encoder**, **Vietnamese-SBERT**, and **OpenAI's text-embedding-3-small** with LangChain frameworks, evaluated using **RAGAS** metrics.

## Quick Start

### Installation
```bash
git clone https://github.com/ngocdung211/nckh-chatbot-neo4j
cd nckh-chatbot-neo4j

# Setup environment
conda env create -f environment.yml -n nckh-chatbot
conda activate nckh-chatbot
# OR: pip install -r requirements.txt

# Configure OCR
./setting.sh
chmod +x chatbot_api/src/entrypoint.sh chatbot_frontend/src/entrypoint.sh
```

### Environment Configuration
Create `.env` file:
```bash
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
OPENAI_API_KEY=your-openai-api-key
AGENT_MODEL=gpt-4o-mini
```

### Run System
```bash
# Start API
cd chatbot_api/src && ./entrypoint.sh

# Start Frontend  
cd chatbot_frontend/src && ./entrypoint.sh
```

## Key Results

### RAGAS Evaluation Results
| Model | Precision | Recall | Faithfulness | Relevance | Time (ms) |
|-------|-----------|--------|--------------|-----------|-----------|
| **text-embedding-3-small** | **73.4%** | **71.2%** | 40.7% | **74.4%** | 1,551 |
| Vietnamese-bi-encoder | 50.5% | 51.0% | 33.9% | 76.0% | 824 |
| Vietnamese-SBERT | 50.0% | 54.0% | **43.2%** | 73.7% | 1,662 |
| PhoBERT-base-v2 | 47.6% | 50.7% | 35.9% | 72.6% | 790 |
| all-mpnet-base-v2 | 38.0% | 35.2% | 34.5% | 49.0% | **249** |

**Key Findings**: OpenAI's text-embedding-3-small achieves the best overall performance with 73.4% precision and 71.2% recall, while Vietnamese-SBERT provides the highest faithfulness (43.2%).

## Technical Architecture
- **Graph Database**: Neo4j for structured knowledge representation
- **Embedding Models**: Multiple Vietnamese-specific and multilingual models
- **Framework**: LangChain for LLM orchestration
- **Evaluation**: RAGAS metrics for comprehensive assessment
- **Data**: HAUI academic content and student services

## Current Limitations & Future Work
**Limitations**:
- Limited to Faculty of Information Technology
- 8-second average response time
- Single model architecture

**Future Plans**:
- Expand to all university faculties
- Reduce response time to <3 seconds
- Multi-model ensemble support
- Real-time learning capabilities

## Citation & Contact
**Citation**:
```
Nguyen, X.H., Do, N.D., Pham, Q.T., Nguyen, C.T. (2025). 
A Retrieval-Augmented Generation Approach Utilizing Graph Databases 
and Large Language Models for Student Assistance Chatbot Systems. 
Hanoi University of Industry, Vietnam.
```

**Contact**: hoangnx@haui.edu.vn | ngocdung021103@gmail.com | Hanoi University of Industry

---

*Research project for Vietnamese educational AI systems and RAG evaluation*
- **Multilingual Support**: Optimized for Vietnamese with English fallback

---

## Installation & Setup
### System Requirements
- **Operating System**: Linux/macOS (tested on Ubuntu 20.04+, macOS 12+)
- **Python Environment**: Python 3.10+ (3.11 recommended)
- **Memory**: Minimum 8 GB RAM (16 GB recommended for large datasets)
- **Storage**: 10 GB available space for models and data
- **Neo4j**: Neo4j Aura instance or local Neo4j 5.0+
- **Network**: Stable internet connection for API calls and model downloads

### Installation Steps

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/ngocdung211/nckh-chatbot-neo4j
   cd nckh-chatbot-neo4j
   ```

2. **Environment Setup**
   ```bash
   # Option 1: Using conda (recommended)
   conda env create -f environment.yml -n nckh-chatbot
   conda activate nckh-chatbot
   
   # Option 2: If environment.yml fails
   conda env create -f environment2.yml -n nckh-chatbot
   conda activate nckh-chatbot
   
   # Option 3: Using pip
   conda create -n nckh-chatbot python=3.11
   conda activate nckh-chatbot
   pip install -r requirements.txt   
   ```

3. **Neo4j Database Setup**
   - Create a Neo4j Aura instance or set up local Neo4j
   - Note the URI, username, and password for configuration
   - Ensure the database is accessible from your environment


---

## Experimental Setup
### Running the System

1. **Start the Backend API**
   ```bash
   cd chatbot_api/src
   ./entrypoint.sh
   ```

2. **Start the Frontend Interface**
   ```bash
   cd chatbot_frontend/src
   ./entrypoint.sh
   ```

3. **API Testing**
   The system provides RESTful endpoints for:
   - Document ingestion and processing
   - Query processing and response generation
   - Performance metrics and evaluation

### Dataset Configuration
The system includes comprehensive test datasets for evaluation:
- **HAUI Dataset**: Hanoi University of Industry academic programs, campus facilities, and student services
- **FIT Dataset**: Faculty of Information Technology specific evaluation set
- **CSV files**: `test_fit*.csv`, `test_haui*.csv` for systematic evaluation
- **JSONL files**: Structured data for graph construction and testing
- **Results**: Multiple evaluation runs stored in `results/` directory organized by model type

### Research Datasets
- **Vietnamese Educational Content**: University-specific documents and resources
- **Academic Programs**: Course descriptions, curricula, and academic policies  
- **Student Services**: Campus facilities, administrative procedures, and support services
- **Multi-domain Testing**: Cross-faculty evaluation to assess generalization capabilities

---

## Results & Evaluation
### RAGAS Evaluation Framework
The system's performance is evaluated using the **RAGAS (Retrieval-Augmented Generation Assessment)** framework, which provides comprehensive metrics for RAG system evaluation:

#### Evaluation Metrics
1. **Contextual Precision**: Measures the proportion of relevant segments in the retrieved content
2. **Context Recall**: Measures the number of relevant documents successfully retrieved  
3. **Faithfulness**: Measures factual consistency of generated answers with respect to the given context
4. **Answer Relevance**: Assesses the degree of focus and relevance of generated answers to the given query

### Quantitative Evaluation Results

#### Embedding Model Comparison
We evaluated five different embedding models in our RAG system, comparing their performance across multiple dimensions:

| Model | Precision | Recall | Faithfulness | Relevance | Retrieval Time |
|-------|-----------|--------|--------------|-----------|----------------|
| **text-embedding-3-small** | **73.4%** | **71.2%** | 40.7% | **74.4%** | 1,551 ms |
| Vietnamese-bi-encoder | 50.5% | 51.0% | 33.9% | 76.0% | 824 ms |
| Vietnamese-SBERT | 50.0% | 54.0% | **43.2%** | 73.7% | 1,662 ms |
| PhoBERT-base-v2 | 47.6% | 50.7% | 35.9% | 72.6% | 790 ms |
| all-mpnet-base-v2 | 38.0% | 35.2% | 34.5% | 49.0% | **249 ms** |

#### Key Findings
- **OpenAI text-embedding-3-small** achieves outstanding performance with the highest precision (73.4%) and recall (71.2%), demonstrating superior accuracy due to its advanced Transformer architecture and large-scale training data
- **PhoBERT-base-v2** shows impressive balanced performance with competitive precision (47.6%) and recall (50.7%), offering cost-efficient solutions with faster response times (790 ms)
- **Vietnamese-SBERT** achieves the highest faithfulness score (43.2%), indicating better factual consistency in generated responses
- **all-mpnet-base-v2** provides the fastest retrieval time (249 ms) but significantly lower accuracy, making it unsuitable for high-precision tasks

### Performance Analysis
#### Retrieval Phase Performance
- **Best Overall**: text-embedding-3-small with superior precision and recall rates
- **Best Speed-Accuracy Balance**: PhoBERT-base-v2 with reasonable accuracy and fast retrieval
- **Best Faithfulness**: Vietnamese-SBERT for applications requiring high factual consistency

#### Generation Phase Performance  
- **Answer Relevance**: Vietnamese-bi-encoder slightly outperforms with 76.0% relevance
- **Contextual Consistency**: text-embedding-3-small maintains strong performance across all metrics
- **Response Time**: Critical for real-time applications, with all-mpnet-base-v2 leading in speed
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
