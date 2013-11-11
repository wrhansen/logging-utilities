"""
This module contains the FilenamePatternFileHandler that is an advanced
logging.FileHandler that determines the filename based on a string
pattern. 
"""

import time
import logging
import os


class FilenamePatternFileHandler(logging.FileHandler):
	"""
	A timed, rotating log file handler that bases if it should be rotated
	on whether or not a file exists based on the pattern that you give it.
	Essentially, this subclass of `logging.FileHandler` does not know if
	and when you rotate into another log file, it just automatically does
	it based on the current time, the interval you specify and the
	filename pattern.

	This is determined when the filehandler is initalized, meaning this
	handler is designed for short running scripts as it does not determine
	rotate during or after initalization.
	"""

	available_intervals = ("H", "D", "M", "MIN", "S")

	def __init__(self, pattern, interval="d", utc=False, *args, **kwargs):
		'''
		Interval can be hourly, daily, monthly
		'''
		self.pattern = pattern
		if "{date}" not in self.pattern:
			self.pattern += "-{date}"
		self.utc = utc
		self.interval = interval.upper()
		if self.interval not in self.available_intervals:
			raise ValueError("{!r} is not a supported interval, the following are supported: {}".format(self.interval, ", ".join(self.available_intervals)))
		filename = self.determine_filename(time.time())

		logging.FileHandler.__init__(self, filename, mode="a", *args, **kwargs)

	def determine_filename(self, current_time):
		'''
		Determine what the current filename will be, depending on the
		pattern and interval set.
		'''
		curr_time = time.gmtime(current_time) if self.utc else time.localtime(current_time)

		# Determine the date format
		if self.interval == "H":
			# Hourly
			self.datefmt = "%Y-%m-%d_%H00"
		elif self.interval == "D":
			# Daily
			self.datefmt = "%Y-%m-%d"
		elif self.interval == "M":
			# Monthly
			self.datefmt = "%Y-%m"
		elif self.interval == "MIN":
			# By the minute
			self.datefmt = "%Y-%m-%d_%H_%M"
		elif self.interval == "S":
			# By the second
			self.datefmt = "%Y-%m-%d_%H_%M_%S"

		# Now put the date, with the given format into the pattern
		return self.pattern.format(date=time.strftime(self.datefmt, curr_time))