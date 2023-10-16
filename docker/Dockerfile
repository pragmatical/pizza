# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Install dependencies
FROM python:3.10-slim AS base

<<<<<<< HEAD
# Install FFModel and other dependencies (and unpack secrets into environment first)
=======
# Install FFModel (and unpack secrets into environment first)
>>>>>>> e9fb3a83f86551fc10c85aa6b287542a1523d3b6
RUN --mount=type=secret,id=ffmodelreposecrets \
    export $(grep -v '^#' /run/secrets/ffmodelreposecrets | tr -d '\r' | xargs -d '\n') \ 
    && apt-get -y update && apt-get install -y git --no-install-recommends && rm -rf /var/lib/apt/lists/* && \
    pip install "git+https://$FFMODEL_REPO_PAT@$FFMODEL_REPO@$FFMODEL_REPO_REF#egg=ffmodel"

WORKDIR /setup

# Only copy and install requirements.txt if it exists in the context
COPY endpoint/*requirements.txt .
RUN if [ -f "requirements.txt" ]; then \
<<<<<<< HEAD
    pip install --no-cache-dir -r requirements.txt; \
=======
    pip install -r requirements.txt; \
>>>>>>> e9fb3a83f86551fc10c85aa6b287542a1523d3b6
fi

# Run the app
FROM base AS app

WORKDIR /app
COPY . .

<<<<<<< HEAD
WORKDIR /app/endpoint

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]
=======
ENTRYPOINT ["python", "endpoint/main.py"]
>>>>>>> e9fb3a83f86551fc10c85aa6b287542a1523d3b6
