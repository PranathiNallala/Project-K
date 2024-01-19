import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import scripts.api.endpoint_router as endpoint_router

# Contains End_Points that exposes End-Points.

app = FastAPI(debug=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[],
)


app.include_router(
    endpoint_router.router,
    prefix="/projectk",
    tags=["project-k"],
    responses={404: {"description": "Not found"}},
)

# Mount the 'static' folder to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    PORT = "8000"
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', PORT)))
