import unittest
from APITextos import APITextos

class APITextosTestCase(unittest.TestCase):

	def test_getUsersSimilar_user_all_topic_1(self):
		"""
			Comprueba que las expresiones regulares de entrada estan bien creadas
		"""
		with self.assertRaises(Exception) as context:
			APITextos.getUsersSimilar_user_relations_semantic("@asd asd", "es", 10, 1)

		self.assertTrue("Parametros incorrectos" in context.exception)