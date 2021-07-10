import collections
import time
import timeit
from itertools import product
import numpy as np
from scipy import spatial
# import cv2
from datetime import datetime

from .utils import centroids_std
from .config import logger, benchmark, SEND_COUNT_TOPIC, SEND_HEATMAP_TOPIC, SEND_ROUTEMAP_TOPIC


class TrackObject:
	__slots__ = [
		"obj_id",
		"time",
		"time_in_roi",
		"time_in_grid",
		"route_id",
		"centroids",
		"is_stall",
		"line_id"
	]

	def __init__(self, obj_id=-1):
		start = time.time()
		self.time = [start, start]
		self.obj_id = obj_id
		self.time_in_roi = {}  # roi_id: time
		self.time_in_grid = {}  # grid_point: time
		self.route_id = None  # final decision
		self.line_id = None
		self.centroids = []
		self.is_stall = False

	def accumulate(self, timestamp, route_id, roi_id, grid_point, ct):
		self.centroids.append(ct)

		if route_id:
			self.route_id = route_id

		if roi_id and self.is_stall:
			dwell_time = self.time_in_roi.get(roi_id, None)
			if dwell_time is None:
				dwell_time = [timestamp, 0]
			else:
				dwell_time[1] += timestamp - dwell_time[0]
				dwell_time[0] = timestamp
			self.time_in_roi[roi_id] = dwell_time

		if grid_point:
			dwell_time = self.time_in_grid.get(grid_point, None)
			if dwell_time is None:
				dwell_time = [timestamp, 0]
			else:
				dwell_time[1] += timestamp - dwell_time[0]
				dwell_time[0] = timestamp
			self.time_in_grid[grid_point] = dwell_time

# class Grid:
# 	__slots__ = [
# 		"index",
# 		"offset",
# 		"centroid"
# 	]

# 	def __init__(self, index):
# 		self.index = index
# 		self.centroid = tuple()

# 	def __repr__(self):
# 		return f"Index {self.index}"


class Tracker:
	__slots__ = [
		"timestamp",
		"producer",
		"is_heatmap",
		"box_id",
		"cam_id",
		"objs",
		"default_shape",
		"grid_size",
		"grid_shape",
		"next_minute",
		"push_priod",
		"heatmap_data"
	]

	def __init__(self, producer, is_heatmap, box_id, cam_id):
		self.producer = producer
		self.is_heatmap = is_heatmap
		self.box_id = box_id
		self.cam_id = cam_id
		self.timestamp = None
		self.objs = {}
		self.default_shape = (1920, 1080)
		self.grid_size = tuple()
		self.grid_shape = tuple()
		minute = datetime.now().minute
		self.push_priod = 5  # minute
		self.next_minute = minute + self.push_priod - minute % self.push_priod
		self.heatmap_data = {}


	def update(self, timestamp, data):
		image = None  # debug
		for obj in data:
			self.timestamp = timestamp  # update timestamp
			obj_id, line_id, route_id, roi_id, x, y = obj["obj_id"], \
													obj["line_id"], \
													obj["route_id"], \
													obj["roi_id"], \
													obj["x"], \
													obj["y"]

			trk = self.objs.get(obj_id, None)
			if trk is None:
				trk = TrackObject(obj_id)
				# Neu bat dau khoi tao da trong roi thi khong dem
				trk.is_stall = False if roi_id else True
			else:
				end = time.time()
				trk.time[-1] = end

			if line_id and trk.line_id is None:
				trk.line_id = line_id
				self.realtime_process(line_id)

			grid_point = None
			if self.is_heatmap:
				t0 = timeit.default_timer()
				grid_point = self.get_grid_point((x, y))
				t1 = timeit.default_timer()
				# benchmark.info(f"get_grid_point {t1 - t0}")

			trk.accumulate(self.timestamp, route_id, roi_id, grid_point, (x, y))
			self.objs[obj_id] = trk

		# 	# for debug
		# 	if image is None:
		# 		image = np.zeros((410, 730, 3), dtype=np.uint8)
		# 	std_x = np.std([p[0] for p in trk.centroids])
		# 	std_y = np.std([p[1] for p in trk.centroids])
		# 	text = "{:.1f}".format(std_x)
		# 	pts = (grid_point[0]*10,grid_point[1]*10)
		# 	cv2.putText(image, text, pts, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
		# 	cv2.circle(image, pts, radius=5, color=(0, 0, 255), thickness=-1)

		# cv2.imshow("image", image)
		# cv2.waitKey(1) & 0xff

	def refresh(self, now, timeout):
		for obj_id in self.objs.copy():
			trk = self.objs[obj_id]
			minute = datetime.now().minute
			obj_timeout = now - trk.time[-1] > timeout
			
			if self.is_heatmap:
				if obj_timeout or minute == self.next_minute:
					while len(trk.time_in_grid):
						grid_point, dwell_time = trk.time_in_grid.popitem()
						dwell_time = dwell_time[1]
						if dwell_time == 0:
							continue
						data = self.heatmap_data.get(grid_point, None)
						c_std = round(centroids_std(trk.centroids), 2)
						if data is None:
							data = {
								"dwell_time": dwell_time,
								"centroid_std": [c_std]
							}
						else:
							data["dwell_time"] += dwell_time
							data["centroid_std"].append(c_std)
						self.heatmap_data[grid_point] = data

			if obj_timeout:
				self.accumulation_process(trk)
				del self.objs[obj_id]
		
		if minute == self.next_minute:
			self.heatmap_process()
			self.next_minute = (minute + self.push_priod) % 60


	def realtime_process(self, line_id):
		"""
		Push data counting
		"""
		entry_value = {'type': "entry", 'box_id': self.box_id, 'cam_id': self.cam_id, 'zone_id': line_id,
		               'timestamp': self.timestamp}
		self.producer.send(
			SEND_COUNT_TOPIC, key=f"{self.box_id}", value=entry_value
		)
		logger.info(f"[Entry] zone id {line_id}")

	def accumulation_process(self, trk):
		"""
		Push route and dwell time data
		"""
		if trk.route_id:
			route_value = {'type': "route", 'box_id': self.box_id, 'cam_id': self.cam_id, 'route_id': trk.route_id,
						   'timestamp': self.timestamp}
			# print(f"Route: {route_value}")
			self.producer.send(
				SEND_ROUTEMAP_TOPIC, key=f"{self.box_id}", value=route_value
			)
			logger.info(f"[Route] route id {trk.route_id}")
		if trk.time_in_roi:
			while len(trk.time_in_roi):
				roi_id, dwell_time = trk.time_in_roi.popitem()
				if dwell_time[1] > 0:
					stall_value = {'type': "stall", 'box_id': self.box_id, 'cam_id': self.cam_id, 'zone_id': roi_id,
								   'dwell_time': dwell_time[1], 'timestamp': self.timestamp}
					self.producer.send(
						SEND_COUNT_TOPIC, key=f"{self.box_id}", value=stall_value
					)
					logger.info(f"[Stall] zone id {roi_id}")

	def heatmap_process(self):
		"""
		Push heatmap data and free data
		"""
		heatmap_data = []
		# image = np.zeros((410, 730, 3), dtype=np.uint8)
		while len(self.heatmap_data):
			grid_point, data = self.heatmap_data.popitem()
			if self.check_mutation_point(data):
				continue
			heatmap_data.append({'index': list(grid_point), 'dwell_time': data['dwell_time']})
		# 	pts = (grid_point[0]*10,grid_point[1]*10)
		# 	cv2.circle(image, pts, radius=data['dwell_time'], color=(0, 0, 255), thickness=-1)
		# cv2.imwrite("image.jpg", image)

		if heatmap_data:
			heatmap_value = {'type': "heatmap", 'box_id': self.box_id, 'cam_id': self.cam_id, 'data': heatmap_data,
							 'timestamp': self.timestamp}
			self.producer.send(
				SEND_HEATMAP_TOPIC, key=f"{self.box_id}", value=heatmap_value
			)
			logger.info(f"[Heatmap] cam id {self.cam_id}")


	def make_grids(self, shape=(1280, 720), scale=(73, 41)):
		self.grid_size = (
			(self.default_shape[0]-1)/(scale[0]-1),
			(self.default_shape[1]-1)/(scale[1]-1)  # w, h
		)
		self.grid_shape = scale

	def get_grid_point(self, ct):
		grid_x = (ct[0] / self.grid_size[0]) // 1
		grid_y = (ct[1] / self.grid_size[1]) // 1
		grid_x = int(grid_x)
		grid_y = int(grid_y)
		# index = grid_y*self.grid_size[0] + grid_x
		return (grid_x, grid_y)
	
	def check_mutation_point(self, data):
		# data = {"dwell_time": 1, "centroid_std": [143.06, 12.3]}
		dwell_time = data["dwell_time"]
		centroid_std = data["centroid_std"]
		if dwell_time > self.push_priod * 0.5 * 60 or \
				sum(centroid_std) / len(centroid_std) < 2.5:
			return True
		return False
		
