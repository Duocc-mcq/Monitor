from environs import Env
import uuid

from .logs import setup_logger

# logs
PC_NAME = "PeopleCounting"

logger = setup_logger(f"{PC_NAME}.log", debug=False)
benchmark = setup_logger("Benchmark.log", debug=False)

env = Env()
env.read_env()

# kafka
BOOTSTRAP_SERVER = env.list("BOOTSTRAP_SERVER", "192.168.30.201:9092")
RECEIVE_BOX_TOPIC = env.list("RECEIVE_BOX_TOPIC", "nvdsanalytics")
RECEIVE_GROUP_ID = env.str("RECEIVE_GROUP_ID", str(uuid.uuid1()))
SEND_COUNT_TOPIC = env.str("SEND_COUNT_TOPIC", "test")
SEND_HEATMAP_TOPIC = env.str("SEND_HEATMAP_TOPIC", "test")
SEND_ROUTEMAP_TOPIC = env.str("SEND_ROUTEMAP_TOPIC", "test")

# TELEBOT
TELE_TOKEN = "1179475771:AAE4nQnNqHe0xhWCT58stNN8UYlPjcJviZk"
TELE_GROUP_ID = -398927192
