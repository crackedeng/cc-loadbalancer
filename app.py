from typing import Union
from fastapi import FastAPI, Request
import logging
from pydantic import PrivateAttr, BaseModel
import requests
import uvicorn
import threading

HOST = '0.0.0.0'

class Logger(BaseModel):
    _logger: logging.Logger = PrivateAttr()

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        super().__init__()
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y%m%d"
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        return self._logger


app = FastAPI()
app1 = FastAPI()
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

def run_server(app, port):
    uvicorn.run(app, host=HOST, port=port)

if __name__ == "__main__":
    thread1 = threading.Thread(target=run_server, args=(app, 80))
    thread2 = threading.Thread(target=run_server, args=(app1, 81))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()