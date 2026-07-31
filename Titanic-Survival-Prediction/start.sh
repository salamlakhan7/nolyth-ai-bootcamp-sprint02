#!/bin/bash
# Runs FastAPI (backend) and Streamlit (frontend) together in one container.
# Used for Hugging Face Spaces Option 2 (combined deployment).

cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 &

cd ../frontend
streamlit run app.py --server.port 7860 --server.address 0.0.0.0