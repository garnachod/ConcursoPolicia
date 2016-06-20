import unittest
from APITextosTestCase import APITextosTestCase


class APITextosTestSuite(unittest.TestSuite):
	"""docstring for APITextosTestSuite"""
	def __init__(self):
		super(APITextosTestSuite, self).__init__()
		self.addTest(APITextosTestCase('test_getUsersSimilar_user_all_topic_1'))


if __name__ == '__main__':
	ts = APITextosTestSuite()
	unittest.TextTestRunner(verbosity=2).run(ts)
		

