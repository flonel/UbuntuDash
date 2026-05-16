FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    grep 

RUN pip install -r requirements.txt

RUN mkdir -p static/images

EXPOSE 8000

CMD ["python", "main.py"]