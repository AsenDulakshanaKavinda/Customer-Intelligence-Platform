#!/bin/bash

echo "Creating project structure inside current directory..."

# App structure
mkdir -p app/{api,agents,rag,nlp,analytics,database,services,utils}

# Other directories
mkdir -p scripts
mkdir -p tests
mkdir -p docker

# Main app file
touch app/main.py

# API
touch app/api/routes_chat.py
touch app/api/routes_feedback.py
touch app/api/routes_admin.py

# Agents
touch app/agents/router_agent.py
touch app/agents/retrieval_agent.py
touch app/agents/answer_agent.py
touch app/agents/escalation_agent.py

# RAG
touch app/rag/retriever.py
touch app/rag/knowledge_base.py
touch app/rag/ingestion.py

# NLP
touch app/nlp/sentiment.py
touch app/nlp/topic_detection.py
touch app/nlp/embeddings.py

# Analytics
touch app/analytics/trends.py
touch app/analytics/clustering.py
touch app/analytics/reports.py

# Database
touch app/database/models.py
touch app/database/session.py
touch app/database/pgvector_client.py

# Services
touch app/services/chat_service.py
touch app/services/feedback_service.py
touch app/services/ingestion_service.py

# Utils
touch app/utils/config.py
touch app/utils/logger.py

# Scripts
touch scripts/ingest_documents.py
touch scripts/initialize_db.py

# Tests
touch tests/test_api.py
touch tests/test_agents.py

# Docker
touch docker/Dockerfile
touch docker-compose.yml

# Requirements
touch requirements.txt

echo "Structure created successfully!"