Chat to website and youtube video is a web application that analyzes transcripts of YouTube videos or indexes the website and provides a question-answer interface to interact with the video's content or website content.

🚀 Features

Website Content Indexing: Automatically fetches and processes website content.

Customizable Embeddings: Uses HuggingFace embeddings for semantic understanding.

Video Transcript Extraction: Retrieves and processes video transcripts.

Interactive Q&A: Allows users to ask questions about the video content or website content and get precise answers.

🖥️ Tech Stack

Frontend: Streamlit

Backend: Python, Langchain, HuggingFace, GroqAI, ChromaDB(vectorStoreDB), youtube-transcript-api

AI: Groq AI LLM for summarization and Q&A
Deployment: Deployed on a cloud platform(AWS)

🛠️ Installation & Setup

0. Environment Variables:

`LANGCHAIN_TRACING_V2=<your_langchain_tracing_v2>`

`LANGCHAIN_ENDPOINT=<your_langchain_endpoint>`

`LANGCHAIN_API_KEY=<your_langchain_api_key>`

`LANGCHAIN_PROJECT=<your_langchain_project>`

`HUGGINGFACE_ACCESS_TOKEN=<your_huggingface_access_token>`

`GROQ_API_KEY=<your_groq_api_key>`

1. Clone the Repository:

`git clone https://github.com/your-username/youtube-video-summarizer.git`

`cd youtube-video-summarizer`

2. Set Up a Virtual Environment:

`python3 -m venv venv`

`source venv/bin/activate`

3. Install Dependencies:

`pip install -r requirements.txt`

4. Run the Application:

`streamlit run app.py`

5. Open in Browser:

Navigate to the local server link provided in the terminal, typically http://localhost:8501.

🎯 How It Works

For Chat to Website:

1. Website Indexing:

- Paste a URL and watch the app fetch and process the content.

- Progress indicators show the indexing stage.

2. Ask Questions

- Input questions and get accurate, context-based answers.

For Chat to Youtube:

1. Input YouTube Video:

- Enter the YouTube video URL in the provided field.

2. Transcript Processing:

- The application extracts the transcript of the video (if available). Generates a structured summary using advanced NLP.

3. Interactive Q&A:

- Users can input specific questions related to the video, and the app responds intelligently.
