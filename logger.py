import logging
from pydantic import PrivateAttr, BaseModel


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
