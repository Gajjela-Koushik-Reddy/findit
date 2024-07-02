# FindIt: Document Search Bot

**FindIt** is a smart bot that helps you search for relevant files and information from a collection of documents. It leverages the capabilities of OpenAI's GPT-3.5-turbo model for intelligent querying and ChromaDB for efficient document storage and retrieval.

## Features

- **Document Loading:** Load PDF documents from a specified directory.
- **Text Splitting:** Split documents into manageable chunks for efficient processing.
- **Embedding and Storage:** Utilize ChromaDB to store and retrieve document embeddings.
- **Intelligent Querying:** Use OpenAI's GPT-3.5-turbo to answer questions based on document content.
- **User Interaction:** Interactive console-based querying with colorful output for an enhanced user experience.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/findit.git
   cd findit
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Set Up Environment Variables:**  
   Create a .env file in the root directory and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
