import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 8945))
    host = os.getenv("APP_HOST", "0.0.0.0")

    print(f"Starting FINd API on {host}:{port}...")
    
    uvicorn.run(
        "api.main:app", 
        host=host, 
        port=port, 
        reload=True  # Helpful for development
    )
