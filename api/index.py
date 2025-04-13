from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import streamlit as st
import subprocess
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    # Get the directory where the main app.py is located
    main_dir = os.path.dirname(os.path.dirname(__file__))
    main_app = os.path.join(main_dir, "app.py")
    
    # Run streamlit as a subprocess
    process = subprocess.Popen(
        ["streamlit", "run", main_app, "--server.port=8501", "--server.address=0.0.0.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    return {"message": "WhatsApp Chat Analyzer is running"}