import json
import time
from datetime import datetime
import numpy as np
import kafka
from kafka import KafkaProducer

from src.config import BOOTSTRAP_SERVER
from src.config import logger


def to_timestamp(str_time: str):
	return int(datetime.strptime(str_time.split(".")[0], "%Y-%m-%dT%H:%M:%S").timestamp())


def init_producer():
	producer = None
	while True:
		try:
			producer = KafkaProducer(
				bootstrap_servers=BOOTSTRAP_SERVER,
				key_serializer=lambda key: str(key).encode(),
				value_serializer=lambda value: json.dumps(value).encode(),
			)
			logger.info(
				f"[Producer] BOOTSTRAP_SERVER={BOOTSTRAP_SERVER}")
			break
		except kafka.errors.NoBrokersAvailable:
			logger.exception(
				f"[Producer] lost connection")
			time.sleep(1)

	return producer


def centroids_std(centroids):
	cx = [p[0] for p in centroids]
	cy = [p[1] for p in centroids]

	return (np.std(cx) + np.std(cy)) / 2
