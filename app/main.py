from fastapi import FastAPI

app = FastAPI(
    title="orbit-pilot-145 API",
    version="0.1.0",
    description="Open-source Grok Bot alternative with a virtual machine that bots can use",
)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "service is healthy"}


@app.get("/", tags=["root"])
async def root():
    """Root endpoint returning service info."""
    return {
        "message": "Welcome to orbit-pilot-145 API",
        "documentation": "/docs",
        "health": "/health",
    }
