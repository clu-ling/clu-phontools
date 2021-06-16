# -*- coding: utf-8 -*-

import unittest
from clu.phontools.alignment.lbe import (
    calculate_lbes_from_stress,
    LexicalBoundaryError,
    LexicalBoundaryErrorType,
)

"""
Test `clu.phontools.alignment.lbe` behaviors
"""


class LexicalBoundaryErrorTests(unittest.TestCase):
    def test_calculate_lbes_from_stress(self):
        """`clu.phontools.alignment.lbe` identify lexical boundary errors (LBEs) using the procedure described in [Jiao et al. (2019)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6808349/pdf/JSLHR-62-3359.pdf#page=4)."""

        target = ["SW", "S", "W", "SW"]
        transcript = ["X", "X", "X", "X", "XX"]
        res = calculate_lbes_from_stress(target=target, transcript=transcript)
        expected = [
            LexicalBoundaryError(
                error_type=LexicalBoundaryErrorType.INSERTION_WEAK,
                target_index=0,
                transcript_index=0,
            )
        ]
        self.assertEqual(
            res,
            expected,
            f"clu.phontools.alignment.lbe.calculate_lbes_from_stress(target={target},transcript={transcript}) produced {res}, but {expected} was expected",
        )

        target = ["WS", "S", "W", "SW"]
        transcript = ["X", "X", "X", "X", "XX"]
        res = calculate_lbes_from_stress(target=target, transcript=transcript)
        expected = [
            LexicalBoundaryError(
                error_type=LexicalBoundaryErrorType.INSERTION_STRONG,
                target_index=0,
                transcript_index=0,
            )
        ]
        self.assertEqual(
            res,
            expected,
            f"clu.phontools.alignment.lbe.calculate_lbes_from_stress(target={target},transcript={transcript}) produced {res}, but {expected} was expected",
        )

        target = ["SW", "S", "W", "SW"]
        transcript = ["XX", "X", "X", "XX"]
        res = calculate_lbes_from_stress(target=target, transcript=transcript)
        expected = []
        self.assertEqual(
            res,
            expected,
            f"clu.phontools.alignment.lbe.calculate_lbes_from_stress(target={target},transcript={transcript}) produced {res}, but {expected} was expected",
        )

        target = ["SW", "S", "W", "SW"]
        transcript = ["X", "X", "X", "XX"]
        res = calculate_lbes_from_stress(target=target, transcript=transcript)
        expected = [
            LexicalBoundaryError(
                error_type=LexicalBoundaryErrorType.INSERTION_WEAK,
                target_index=0,
                transcript_index=0,
            ),
            LexicalBoundaryError(
                error_type=LexicalBoundaryErrorType.DELETION_STRONG,
                target_index=3,
                transcript_index=3,
            ),
            LexicalBoundaryError(
                error_type=LexicalBoundaryErrorType.INSERTION_WEAK,
                target_index=3,
                transcript_index=3,
            ),
        ]
        self.assertEqual(
            res,
            expected,
            f"clu.phontools.alignment.lbe.calculate_lbes_from_stress(target={target},transcript={transcript}) produced {res}, but {expected} was expected",
        )

        # FIXME: is this correct?
        # target = ["WS", "S", "W", "SW"]
        # transcript = ["X", "X", "X", "X", "X", "XX"]
        # res = calculate_lbes_from_stress(
        #   target=target,
        #   transcript=transcript
        # )
        # expected = [
        #   LexicalBoundaryError(
        #     error_type=LexicalBoundaryErrorType.INSERTION_STRONG,
        #     target_index=0,
        #     transcript_index=0
        #   )
        #   LexicalBoundaryError(
        #     error_type=LexicalBoundaryErrorType.INSERTION_WEAK,
        #     target_index=3,
        #     transcript_index=4
        #   ),
        #   LexicalBoundaryError(
        #     error_type=LexicalBoundaryErrorType.DELETION_WEAK,
        #     target_index=3,
        #     transcript_index=5
        #   ),
        #   LexicalBoundaryError(
        #     error_type=LexicalBoundaryErrorType.UNKNOWN,
        #     target_index=-1,
        #     transcript_index=5
        #   )
        # ]
        # self.assertEqual(res, expected, f"clu.phontools.alignment.lbe.calculate_lbes_from_stress(target={target},transcript={transcript}) produced {res}, but {expected} was expected")


# How should this be handled?

# target:     ['WS', 'S', 'W', 'SW']
# transcript: ['X', 'X', 'X', 'X', 'X', 'XX']
