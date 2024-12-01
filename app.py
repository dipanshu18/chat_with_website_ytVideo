import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_groq.chat_models import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

from youtube_transcript_api import YouTubeTranscriptApi, CouldNotRetrieveTranscript
from youtube_transcript_api.formatters import TextFormatter
import streamlit as st
import re


load_dotenv()

# Set environment variables
os.environ["LANGCHAIN_TRACING_V2"] = st.secrets.creds["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets.creds["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets.creds["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets.creds["LANGCHAIN_PROJECT"]
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = st.secrets.creds["HUGGINGFACE_ACCESS_TOKEN"]

groq_api_key = st.secrets.creds["GROQ_API_KEY"]

# Initialize the model
model = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-8b-8192")
parser = StrOutputParser()

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio(
    "Choose an action:", ["QnA with Website", "Chat with YouTube Video"]
)

if option == "QnA with Website":
    st.title("🔍 Website Q&A")

    website_url = st.text_input("🌐 Paste the website URL:")

    if website_url:
        try:
            st.toast("Indexing the webpage...", icon="🔄")
            loader = WebBaseLoader(web_path=website_url)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=300
            )

            final_docs = text_splitter.split_documents(documents)

            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            db = Chroma.from_documents(
                final_docs, embeddings, persist_directory="./chroma_db"
            )

            st.success("✅ Website content indexed successfully!")
        except Exception as e:
            st.error(f"❌ Failed to index the website. Error: {e}")

        user_question = st.text_input("🤔 Enter your question about the website:")

        if user_question:
            try:
                st.toast("Generating answer...", icon="📝")
                relevant_docs = db.similarity_search(user_question, k=3)
                context = "\n".join([doc.page_content for doc in relevant_docs])

                prompt = ChatPromptTemplate(
                    [
                        (
                            "system",
                            "You are a knowledgeable and precise assistant tasked with answering questions based on website content. "
                            "Provide clear, concise, and accurate responses using only the given context. ",
                        ),
                        ("system", f"Context: {context}"),
                        (
                            "user",
                            "Based on the above context, answer the following question: {question}",
                        ),
                    ]
                )

                chain = prompt | model | parser
                st.write("💡 Answer:")
                st.write_stream(chain.stream({"question": user_question}))

            except Exception as e:
                st.error(f"❌ Failed to fetch the answer. Error: {e}")


elif option == "Chat with YouTube Video":
    st.title("🎥 YouTube Video Chat")

    video_url = st.text_input("📹 Paste the YouTube video URL:")

    if video_url:
        try:
            toast2 = st.toast("Processing the video...", icon="🔄")

            match = re.search(r"v=([^&]+)", video_url)
            video_id = match.group(1) if match else None

            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id)
            except CouldNotRetrieveTranscript:
                st.error(
                    "Transcript for this video is not available. It may be disabled by the video owner."
                )
                transcript = None

            if transcript:
                formatter = TextFormatter()
                formatted_text = formatter.format_transcript(transcript)

                st.success("✅ Video content processed successfully!")

                user_query = st.text_input("🤔 Ask a question about the video:")

                if user_query:
                    try:
                        toast2.toast("Generating answer...", icon="📝")

                        prompt = ChatPromptTemplate(
                            [
                                (
                                    "system",
                                    "You are a knowledgeable and precise assistant tasked with answering questions based on website content. "
                                    "Provide clear, concise, and accurate responses using only the given context. ",
                                ),
                                ("system", f"Context: {formatted_text}"),
                                (
                                    "user",
                                    "Based on the above context, answer the following question: {question}",
                                ),
                            ]
                        )

                        chain = prompt | model | parser
                        st.write("💡 Answer:")
                        st.write_stream(chain.stream({"question": user_query}))
                    except Exception as e:
                        st.error(f"❌ Failed to generate a response. Error: {e}")
        except Exception as e:
            st.error(
                "❌ Something went wrong while processing the video. Please try again."
            )
