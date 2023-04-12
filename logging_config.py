import logging
import sys
from datetime import datetime

time = datetime.now()
log_name = f'logs/{time.strftime("%d%m%YT%H:%M:%S")}.log'

logging.basicConfig(
    filename=log_name,
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger("Scraper")
logger.addHandler(logging.StreamHandler(sys.stdout))
