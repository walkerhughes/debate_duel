FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY debate_duel/ /app/debate_duel/

# Default environment variables
ENV PORT=8003
ENV HOST=0.0.0.0

# Run the service
CMD ["python", "-m", "debate_duel.agents.judge"]