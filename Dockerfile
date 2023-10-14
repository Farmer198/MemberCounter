FROM python:3.11.6-alpine AS builder

# Install dependencies
RUN apk update && \
    apk add --no-cache git linux-headers libffi-dev build-base && \ 
    rm -rf /var/cache/apk/*

WORKDIR /app/membercounter

# Create a Python venv
RUN python3 -m venv .venv

# Enable venv
ENV PATH="/app/membercounter/.venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \ 
    pip install --no-cache-dir -r requirements.txt

FROM python:3.11.6-alpine AS final

# Install runtime dependencies
RUN apk update && \
    apk add --no-cache libffi git 

WORKDIR /app/membercounter

# Copy the Python venv and all dependencies from the build stage
COPY --from=builder /app/membercounter/.venv /app/membercounter/.venv

COPY . .

# Enable venv
ENV PATH="/app/membercounter/.venv/bin:$PATH"

CMD [ "python",  "./src/main.py"]
