FROM python:3.11.4-alpine

# Install dependencies
RUN apk update && \
    apk add --no-cache git linux-headers libffi-dev build-base && \ 
    rm -rf /var/cache/apk/*

WORKDIR /opt/membercounter

# Create a Python venv
RUN python3 -m venv .venv

# Enable venv
ENV PATH="/opt/membercounter/.venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt

WORKDIR /opt/membercounter

COPY . .
CMD [ "python",  "./src/main.py"]