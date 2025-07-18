# builder ahh
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --upgrade pip && pip install uv

# create venv and install deps from toml
COPY pyproject.toml uv.lock* ./
RUN uv venv && uv sync --no-dev

FROM python:3.12-slim
WORKDIR /app

# copy venv from builder
COPY --from=builder /app/.venv ./.venv 

# necessary code
COPY ./app ./app
COPY ./data ./data
COPY ./tests ./tests
COPY import_data.py .

# set path to venv dir
ENV PATH="/app/.venv/bin:$PATH"

# run 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
