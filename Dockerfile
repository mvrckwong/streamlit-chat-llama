# Use an official Python runtime as a base image
FROM python:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade the to the latest pip
RUN pip install --no-cache-dir --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install wget
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Create the models directory
RUN mkdir /models

# Download the file into the models directory
RUN wget -P /app/models/ https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q2_K.bin

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit.py when the container launches
CMD ["streamlit", "run", "src/app.py", "--server.port=8501"]