# Use the official Python base image
FROM python:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

COPY config/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade Flask Werkzeug Flask-SQLAlchemy
RUN pip install Flask pyodbc openai

RUN rm -f requirements.txt
# Clone the repository (replace with your repository URL)
RUN git clone https://github.com/lakshmeeshks/ecommerceApp.git .

# Install the Python packages specified in requirements.txt
RUN ls -lrt
#RUN pip install --no-cache-dir -r config/requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP=src/app.py

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

#run below to start container
#docker run -dt -p 80:5000 flask-app