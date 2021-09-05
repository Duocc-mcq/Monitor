import json
import time

import psutil
import ray
from kafka import KafkaConsumer

from .config import BOOTSTRAP_SERVER, RECEIVE_BOX_TOPIC, RECEIVE_GROUP_ID
from .config import logger
from .task import Task

num_cpus = psutil.cpu_count(logical=False)
ray.init(num_cpus=num_cpus, include_dashboard=False)


class Service:
	__slots__ = [
		"consumer",
		"task_dict",
		"cam_worker_mapping",
	]

	def __init__(self):

		self.consumer = None
		self.init_consumer()

		self.task_dict = {}
		self.cam_worker_mapping = {}

	def init_consumer(self):
		while True:
			try:
				self.consumer = KafkaConsumer(bootstrap_servers=BOOTSTRAP_SERVER,
											  auto_offset_reset='latest',
											  value_deserializer=lambda value: json.loads(value.decode()),
											  group_id=RECEIVE_GROUP_ID)
				self.consumer.subscribe(RECEIVE_BOX_TOPIC)
				break
			except Exception as e:
				time.sleep(1)  # error when connect kafka
		logger.info(
			f"KafkaConsumer: BOOTSTRAP_SERVER={BOOTSTRAP_SERVER}, CONSUMER_TOPIC={RECEIVE_BOX_TOPIC},"
			f" CONSUME_GROUP_ID={RECEIVE_GROUP_ID}...")

	def run(self):
		logger.info("Service is running...")

		core_id = 0  # current core_id for new cam
		for message in self.consumer:
			# try:
			data = message.value
			# Filter valid data
			if not {"box_id", "cam_id", "data", "scale", "timestamp"} <= data.keys():
				logger.warning(f"Wrong format input data={data}...")
				continue
			# box_id = data["box_id"]
			cam_id = data["cam_id"]

			task_id = self.cam_worker_mapping.get(cam_id, None)
			if task_id is None:
				t = self.task_dict.get(core_id, None)
				if t is None:
					t = Task.remote(core_id)
					self.task_dict[core_id] = t
				task_id = core_id
				self.cam_worker_mapping[cam_id] = task_id
				core_id = (core_id+1) % num_cpus

			self.task_dict[task_id].process.remote(data)
			# except Exception as e:
			# 	logger.exception(e)

