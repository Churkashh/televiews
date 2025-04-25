import yaml
import time
import os

from pydantic import BaseModel
from loguru import logger


class Config(BaseModel):
    main: dict
    
    class Config:
        extra = "forbid"

class MainConfig(BaseModel):
    threads: int
    log_proxy_err: bool
    detailed_exception_log: bool

def validate_config():
    """Config validation"""
    try:
        with open("./inp/config.yaml", "r") as file:
            config = yaml.safe_load(file)
            
        config_data = Config.model_validate(config)

        main_config = MainConfig(**config_data.main)
        return main_config
    except Exception as e:
        logger.exception(f"Config validation error -> {e}")
        time.sleep(5)
        os._exit(1)
        

main_config = validate_config()

THREADS = main_config.threads
PROXY_ERR_LOG = main_config.log_proxy_err
DETAILED_EXCEPTION = main_config.detailed_exception_log
