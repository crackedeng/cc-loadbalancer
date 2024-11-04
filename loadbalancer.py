from typing import Union
from fastapi import FastAPI, Request
from logger import Logger
import requests
import uvicorn

app = FastAPI()
logger = Logger("loadbalancer").get_logger()

@app.get("/", status_code=200)
def loadbalancer_entry(request: Request):
    logger.info(
        {
            "host": request.headers.get("host"),
            "method": request.method,
            "agent": request.headers.get("user-agent"),
            "accept": request.headers.get("accept"),
        }
    )
    return "hello from loadbalancer"