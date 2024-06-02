FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
# Install gunicorn
RUN pip install gunicorn
CMD ["gunicorn", "-b", ":8080", "main:app"]