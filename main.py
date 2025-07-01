#!/usr/bin/env python3
"""
Vercel entry point for Streamlit app
"""
import os
import sys
from streamlit.web import cli as stcli

def main():
    """Main function to run Streamlit app on Vercel"""
    # Set the port from Vercel environment
    port = int(os.environ.get("PORT", 8501))
    
    # Streamlit app arguments
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    # Run the Streamlit app
    stcli.main()

if __name__ == "__main__":
    main()