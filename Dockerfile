FROM python:latest

# Setting Working Directory
WORKDIR /app

# Installing dependencies
COPY ./requirements.txt /app
RUN pip install --upgrade -r requirements.txt

# Copying scripts to folder
COPY . /app

# Starting server
CMD ["streamlit", "run", "app.py"]