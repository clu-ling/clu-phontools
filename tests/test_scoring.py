import unittest
from clu.phontools.scoring import Metrics


class ScoringTests(unittest.TestCase):
    def test_docstrings(self):
        assert Metrics.__doc__ is not None

    def test_phone_similarity(self):
        pair = ("æ", "a")
        predicted = Metrics.similarity(pair)
        print(predicted)
        assert predicted > 0
        # , ('-', 'd'), ('v', 'v'), ('æ', 'ɛ')]
        # predicted = [Metrics.similarity(pair) for pair in alignments]
        # expected  = [75.0, 89.0, 0.0, 0.0]
        # self.assertEqual(predicted, [75.0, 89.0, 0.0, 0.0])
