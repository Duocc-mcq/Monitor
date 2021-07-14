import collections
import json
import time
import timeit
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import ray

from .bot import Bot
from .config import logger, benchmark
from .config import TELE_TOKEN
from .tracker import Tracker
from .utils import to_timestamp, init_producer


@ray.remote
class Task(object):
	__slots__ = [
		"bot",
		"cam_trackings",
		"producer",
	]

	def __init__(self, core_id):
		super().__init__()
		logger.info(f"core_id={core_id} Initializing...")
		self.bot = Bot(TELE_TOKEN)

		self.producer = init_producer()
		self.cam_trackings = {}

	def process(self, data):
		try:
			t00 = timeit.default_timer()

			timestamp = to_timestamp(data["timestamp"])
			cam_id = data["cam_id"]
			box_id = data["box_id"]
			scale = json.loads(data["scale"])  # convert '[1,2]' to [1,2]
			shape = json.loads(data["shape"])
			is_heatmap = True if scale and shape else False

			tracker = self.cam_trackings.get(cam_id, None)
			if tracker is None:
				tracker = Tracker(self.producer, is_heatmap, box_id, cam_id)
				if is_heatmap:
					tracker.make_grids(shape=shape, scale=scale)

			t0 = timeit.default_timer()
			# [tracker.update(timestamp, obj) for obj in data["data"]]
			tracker.update(timestamp, data["data"])
			t1 = timeit.default_timer()
			# benchmark.info(f"Tracker update {len(data['data'])} objects {t1 - t0}")

			# remove dead obj
			now = int(time.time())
			if now % 30 == 0:
				self.cam_trackings[cam_id].refresh(now=now, timeout=15)

			self.cam_trackings[cam_id] = tracker

			t11 = timeit.default_timer()
			# benchmark.info(f"Task process {t11 - t00}")

		except Exception as e:
			logger.exception(e)
