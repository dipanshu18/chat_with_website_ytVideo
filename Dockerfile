FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
COPY .streamlit/secrets.toml /app/.streamlit/
COPY app.py /app/
EXPOSE 8501
CMD [ "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
