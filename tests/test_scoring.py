import unittest
from clu.phontools.scoring import Metrics


class ScoringTests(unittest.TestCase):
    def test_docstrings(self):
        self.assertNotEqual(Metrics.__doc__, None, f"Metrics should have a docstring")

    def test_phone_similarity(self):
        pair = ("æ", "a")
        predicted = Metrics.similarity(pair)
        # print(predicted)
        self.assertTrue(predicted > 0, f"predicted should be > 0, but was {predicted}")
        # , ('-', 'd'), ('v', 'v'), ('æ', 'ɛ')]
        # predicted = [Metrics.similarity(pair) for pair in alignments]
        # expected  = [75.0, 89.0, 0.0, 0.0]
        # self.assertEqual(predicted, [75.0, 89.0, 0.0, 0.0])
