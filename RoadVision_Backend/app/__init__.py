from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload_process_routes import router as upload_router

def create_app():
    app = FastAPI(
        title="ROADvision_Lagos: Infrastructure Guardian API", 
        description="AI-powered infrastructure governance for Nigeria. Created by David Akpoviroro Oke (MrIridescent)",
        version="2.0.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api_prefix = "/api/v1"

    @app.get("/")
    async def root():
        return {
            "message": "ROADvision_Lagos Sentinel API",
            "creator": "David Akpoviroro Oke (MrIridescent)",
            "region": "Lagos, Nigeria",
            "version": "2.0.0",
            "endpoints": {
                "upload": "/api/upload",
                "status": "/api/status/{video_id}",
                "results": "/api/results/{video_id}",
                "websocket": "/ws/{video_id}",
                "list_videos": "/api/videos"
            }
        }
    # Include routers
    app.include_router(upload_router, prefix=f"{api_prefix}", tags=["Detection"])

    return app

    