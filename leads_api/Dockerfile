FROM python:3.11-slim

WORKDIR /

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /src/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /src/requirements.txt

COPY . /
WORKDIR /src

EXPOSE 8001

CMD ["python", "run_server.py"]