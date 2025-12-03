"""
Main FastAPI application - Hello World
"""
from fastapi import FastAPI

# Create FastAPI app
app = FastAPI(
    title="WhatsApp API Middleware",
    description="API middleware para notificaciones WhatsApp",
    version="0.1.1"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Hello World from WhatsApp API Middleware!",
        "status": "running",
        "version": "0.1.1"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "whatsapp-api-middleware"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
