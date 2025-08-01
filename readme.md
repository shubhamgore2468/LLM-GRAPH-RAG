# LLM Graph RAG - Product Review Comparison System

A sophisticated product comparison system that leverages Graph Retrieval-Augmented Generation (RAG) to analyze and compare products based on customer reviews from multiple e-commerce platforms.

## 🚀 Features

- **Web Scraping**: Automated product data and review extraction from e-commerce sites
- **Graph Database**: Neo4j-powered knowledge graph for structured data relationships
- **LLM Integration**: GPT-powered analysis with LangChain framework
- **Interactive Chat**: Streamlit-based conversational interface
- **Hybrid Search**: Combined vector and full-text search capabilities
- **Real-time Analysis**: Live product comparison with instant insights

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Scraper   │    │   Neo4j Graph   │    │   LLM Chain     │
│   (Crawl4AI)    │───▶│   Database      │───▶│   (LangChain)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Parser   │    │  Vector Index   │    │  Streamlit UI   │
│   (BeautifulSoup)│    │  (OpenAI)       │    │  (Chat Interface)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Technology Stack

- **Backend**: Python, LangChain, Neo4j
- **LLM**: OpenAI GPT-3.5-turbo
- **Web Scraping**: Crawl4AI, BeautifulSoup4
- **Search Enhancement**: Tavily Search API
- **Frontend**: Streamlit
- **Database**: Neo4j Graph Database
- **Embeddings**: OpenAI Embeddings

## 📦 Installation

### Prerequisites

- Python 3.8+
- Neo4j Database (local or cloud instance)
- OpenAI API Key
- Tavily API Key (optional, for enhanced search)

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd GraphRag_Langchain
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file based on `.env.example`:

   ```bash
   cp .env.example .env
   ```

   Fill in your credentials:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_neo4j_password
   NEO4J_URI=neo4j+s://your_neo4j_instance
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Start Neo4j Database**
   ```bash
   docker-compose up -d
   ```
   Or use your cloud Neo4j instance.

## 🚀 Usage

### Running the Application

1. **Start the Streamlit application**

   ```bash
   cd src
   streamlit run flow.py
   ```

2. **Access the web interface**
   Open your browser and navigate to `http://localhost:8501`

### Using the System

#### Step 1: Input Product URLs

- Navigate to the input page
- Enter two product URLs from supported e-commerce platforms
- Click "Analyze" to start data collection

#### Step 2: Chat with the System

- Switch to the chatbot page
- Ask questions about the products:
  - "Which product is better for daily usage?"
  - "What do reviews say about the camera quality?"
  - "Which is more cost-effective?"
  - "Compare the battery life of both products"

### Example Queries

```
User: "Which phone has better camera quality?"
System: "Based on the reviews, the iPhone 15 Pro Max has superior camera quality with its 48MP main camera and advanced computational photography features..."

User: "What are the main complaints about the Samsung Galaxy?"
System: "The main complaints include occasional heating issues and some users reporting slower performance with heavy multitasking..."
```

## 📊 Data Flow

1. **Data Collection**

   - URLs are scraped using Crawl4AI
   - Product information and reviews are extracted
   - Data is enhanced with Tavily search results

2. **Data Processing**

   - Text is split into manageable chunks
   - Metadata is preserved for product association
   - Documents are prepared for graph transformation

3. **Graph Creation**

   - LLM transforms documents into graph structures
   - Entities and relationships are identified
   - Data is stored in Neo4j with vector embeddings

4. **Query Processing**
   - User queries are processed through entity extraction
   - Hybrid search combines vector similarity and graph traversal
   - LLM generates contextual responses

## 🔧 Configuration

### Neo4j Setup

The system automatically creates necessary indices:

- Full-text index for entity search
- Vector index for semantic similarity
- Relationship indices for graph traversal

### LLM Configuration

Default settings:

- Model: GPT-3.5-turbo
- Temperature: 0 (for consistent responses)
- Chunk size: 512 tokens
- Overlap: 24 tokens

## 📂 Project Structure

```
GraphRag_Langchain/
├── src/
│   ├── data_collection/       # Web scraping modules
│   ├── data_processing/       # Data preprocessing
│   ├── database/             # Neo4j connection
│   ├── inference/            # LLM integration
│   ├── models/               # Graph creation
│   ├── streamlit/            # UI components
│   └── utils/                # Utility functions
├── data/                     # Data storage
├── notebooks/                # Development notebooks
├── scripts/                  # Standalone scripts
├── docker-compose.yml        # Neo4j setup
└── requirements.txt          # Dependencies
```
