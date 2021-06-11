import unittest
from clu.phontools.scoring import Metrics, PhonemeErrors


class ScoringTests(unittest.TestCase):
    def test_docstrings(self):
        assert Metrics.__doc__ is not None

    def test_alignments(self):
        alignments = [("æ", "-"), ("-", "d"), ("v", "v"), ("æ", "ɛ")]
        assert alignments[0] == ("æ", "-")
        self.assertEqual(len(alignments), 4, "should be 4")
        for item in alignments:
            assert len(item) == 2, "should be 2"
            # assert item[0] != ['æ', '-', 'v', 'æ']

    def test_phone_similarity(self):
        pair = ("æ", "a")
        predicted = Metrics.similarity(pair)
        print(predicted)
        assert predicted > 0
        # , ('-', 'd'), ('v', 'v'), ('æ', 'ɛ')]
        # predicted = [Metrics.similarity(pair) for pair in alignments]
        # expected  = [75.0, 89.0, 0.0, 0.0]
        # self.assertEqual(predicted, [75.0, 89.0, 0.0, 0.0])

    # def test_phoneme_errors(self):
    #     alignments = [('æ', '-'), ('-', 'd'), ('v', 'v'), ('æ', 'ɛ')]
    #     predicted_errors = Metrics.phoneme_errors(alignments)
    #     expected_errors = PhonemeErrors(
    #       insertions = [('æ', '-')],
    #       deletions = [('-', 'd')],
    #       substitutions = [('æ', 'ɛ')]
    #     )
    #     self.assertEqual(predicted_errors, expected_errors, "Testing phoneme errors failed.")
