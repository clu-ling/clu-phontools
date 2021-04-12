import unittest
from scoring import Metrics

class ScoringTests(unittest.TestCase):
    
    def test_alignments(self):
        alignments = [('æ', '-'), ('-', 'd'), ('v', 'v'), ('æ', 'ɛ')]
        assert alignments[0] == ('æ', '-')
        assert len(alignments) == 4, "should be 4"
        assert Metrics(alignments)
        for item in alignments:
            assert len(item) == 2, "should be 2"
            assert item[0] != ['æ', '-', 'v', 'æ']

    def test_phoneme_errors(self):
        alignments = [('æ', '-'), ('-', 'd'), ('v', 'v'), ('æ', 'ɛ')]
        score = Metrics(alignments)
        self.assertEqual(score.calcPhonemeErrors(),
                         ('edit distance score:', 3, 'deletions:', 1, [
                          ('æ', '-')], 'insertions:', 1, [('-', 'd')], 'substitutions:', 1, [('æ', 'ɛ')]),
            "Tesing phoneme errors failed.")

    def test_phone_similarity(self):
        alignments = [('æ', '-'), ('-', 'd'), ('v', 'v'), ('æ', 'ɛ')]
        score = Metrics(alignments)
        self.assertEqual([score.similarity(i)
                          for i in alignments], [75.0, 89.0, 0.0, 0.0])
