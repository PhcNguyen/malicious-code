FROM python:3.11.2
WORKDIR /app
COPY . /app
EXPOSE 4000
CMD ["python", "tests/server.py"]
