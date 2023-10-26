import logging
import datetime
import os
import sys
import glob
import tqdm
from typing import List
import re

class LoggingManager:
    def __init__(self, init_root: str):
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

        self.logs_addr = re.sub(r"\s|:|-", "_", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.logs_addr = os.path.join(init_root, f"logs_{self.logs_addr}.log")
        self.file_handler = logging.FileHandler(self.logs_addr)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

        self.logger.info(f'Logs generated at "{self.logs_addr}". For detailed logs check the file.')
        self.logger.info(f'Docstrings generation started for "{init_root}/*.py" files')

    @property
    def LOGGER(self):
        return self.logger
    
    @LOGGER.setter
    def get_logger(self):
        raise NotImplementedError("Cannot set logger")
    
    @property
    def set_log_handlers(self):
        raise NotImplementedError("Cannot access applied log handlers")
    
    @set_log_handlers.setter
    def set_log_handlers(self, handlers: List[logging.Handler]):
        self.logger.handlers = []
        self.logger.handlers = handlers
    
    
    def log_curr_state(self, root: str):
        self.set_log_handlers = [self.file_handler]
        self.logger.info(f'Working on "{root}\\*.py"')

        start = datetime.datetime.now()
        files = glob.glob(os.path.join(root + "/*.py"))

        for file in tqdm.tqdm(files, desc=f"Working on {root}"):
            self.set_log_handlers = [self.file_handler]
            self.logger.info(f'Working on "{file}"')
            yield file
            logging.info(f'Docstrings generated for "{file}". Time Taken: {datetime.datetime.now() - start}')
            self.line_breaks(dir=False, file=True)
        
        self.set_log_handlers = [self.file_handler]
        self.logger.info(f'Docstrings generation completed for "{root}\\.*py". Time Taken: {datetime.datetime.now() - start}')
        self.line_breaks(dir=True, file=False)
    

    def line_breaks(self, dir: bool, file: bool):
        if not dir ^ file:
            raise ValueError("Both dir and file cannot be True or False")

        if dir:
            self.logger.info(">"*50)
        if file:
            self.logger.info("="*50)

        


    

    
