from typing import List, Tuple, Text
from . import features
import numpy as np


class ReAline(object):
    """
    Feature-based algorithm for aligning two sequences of phones.

    Based on Kondrak 2002
    """

    inf = float("inf")

    def __init__(
        self,
        similarity_matrix=features.similarity_matrix,
        feature_matrix=features.feature_matrix,
        salience=features.salience,
        consonants=features.consonants,
        C_skip=features.C_skip,
        C_vwl=features.C_vwl,
        C_sub=features.C_sub,
        C_exp=features.C_exp,
        R_c=features.R_c,
        R_v=features.R_v,
    ):
        self.similarity_matrix = similarity_matrix
        self.feature_matrix = feature_matrix
        self.consonants = consonants
        self.salience = salience
        self.C_skip = C_skip
        # weight assigned to vowel, consonant pairs
        self.C_vwl = C_vwl
        self.C_sub = C_sub
        self.C_exp = C_exp
        # List of relevant features for consonants
        self.R_c = R_c
        # List of relevant features for vowels
        self.R_v = R_v
        # sanity check
        self.sanity_check()

    def sanity_check(self):
        """
        Sanity check that ensures necessary features are present
        """

        similarity_matrix = self.similarity_matrix
        feature_matrix = self.feature_matrix
        salience = self.salience
        consonants = self.consonants

        # ensure all salience values are found in feature matrix
        feats = set()
        feat_values = set()
        for phone_fm in feature_matrix.values():
            for (k, v) in phone_fm.items():
                feats.add(k)
                feat_values.add(v)

        # check that all features has an assigned salience
        assert (
            len(salience.keys() - feats) == 0
        ), f"salience and features for each sound in feature_matrix do not match: {salience.keys() - feats}"

        # FIXME: re-enable this check
        assert (
            len(similarity_matrix.keys() - feat_values) == 0
        ), f"similarity_matrix and feature values for each sound in feature_matrix do not match: {similarity_matrix.keys() - feat_values}"

        # FIXME: re-enable this check
        missing = [c for c in consonants if c not in feature_matrix.keys()]
        assert (
            len(missing) == 0
        ), f"Some consonants missing from feature_matrix: {missing}"

    def sigma_skip(self, p: Text) -> int:
        """
        Returns score of an indel of P.
        (Kondrak 2002: 54)
        """
        return self.C_skip

    def V(self, p: Text) -> int:
        """
        Return vowel weight if P is vowel.
        (Kondrak 2002: 54)
        """
        return 0 if p in self.consonants else self.C_vwl

    def R(self, p: Text, q: Text) -> List[Text]:
        """
        Return relevant features for segment comparsion.
        (Kondrak 2002: 54)
        """
        consonants = self.consonants

        return self.R_c if p in consonants or q else self.R_v

    def diff(self, p: Text, q: Text, f: Text) -> int:
        """
        Returns difference between phonetic segments P and Q for feature F.
        (Kondrak 2002: 52, 54)
        """
        p_features, q_features = self.feature_matrix[p], self.feature_matrix[q]
        return abs(
            self.similarity_matrix[p_features[f]]
            - self.similarity_matrix[q_features[f]]
        )

    def delta(self, p: Text, q: Text) -> int:
        """
        Return weighted sum of difference between P and Q.
        (Kondrak 2002: 54)
        """
        features = self.R(p, q)
        total = 0
        for f in features:
            total += self.diff(p, q, f) * self.salience[f]
        return total

    def sigma_sub(self, p: Text, q: Text) -> int:
        """
        Returns score of a substitution of P with Q.
        (Kondrak 2002: 54)
        """
        return self.C_sub - self.delta(p, q) - self.V(p) - self.V(q)

    def sigma_exp(self, p: Text, q: List[Text]) -> int:
        """
        Returns score of an expansion/compression.
        (Kondrak 2002: 54)
        """
        q1 = q[0]
        q2 = q[1]
        return (
            self.C_exp
            - self.delta(p, q1)
            - self.delta(p, q2)
            - self.V(p)
            - max(self.V(q1), self.V(q2))
        )

    def _retrieve(self, i, j, s, S, T, seq1, seq2, out) -> List[Tuple[Text, Text]]:
        """
        Retrieve the path through the similarity matrix S starting at (i, j).

        :return: Alignment of seq1 and seq2
        """
        if S[i, j] == 0:
            return out
        else:
            if (
                j > 1
                and S[i - 1, j - 2] + self.sigma_exp(seq1[i - 1], seq2[j - 2 : j]) + s
                >= T
            ):
                out.insert(0, (seq1[i - 1], seq2[j - 2 : j]))
                self._retrieve(
                    i - 1,
                    j - 2,
                    s + self.sigma_exp(seq1[i - 1], seq2[j - 2 : j]),
                    S,
                    T,
                    seq1,
                    seq2,
                    out,
                )
            elif (
                i > 1
                and S[i - 2, j - 1] + self.sigma_exp(seq2[j - 1], seq1[i - 2 : i]) + s
                >= T
            ):
                out.insert(0, (seq1[i - 2 : i], seq2[j - 1]))
                self._retrieve(
                    i - 2,
                    j - 1,
                    s + self.sigma_exp(seq2[j - 1], seq1[i - 2 : i]),
                    S,
                    T,
                    seq1,
                    seq2,
                    out,
                )
            elif S[i, j - 1] + self.sigma_skip(seq2[j - 1]) + s >= T:
                out.insert(0, ("-", seq2[j - 1]))
                self._retrieve(
                    i, j - 1, s + self.sigma_skip(seq2[j - 1]), S, T, seq1, seq2, out
                )
            elif S[i - 1, j] + self.sigma_skip(seq1[i - 1]) + s >= T:
                out.insert(0, (seq1[i - 1], "-"))
                self._retrieve(
                    i - 1, j, s + self.sigma_skip(seq1[i - 1]), S, T, seq1, seq2, out
                )
            elif S[i - 1, j - 1] + self.sigma_sub(seq1[i - 1], seq2[j - 1]) + s >= T:
                out.insert(0, (seq1[i - 1], seq2[j - 1]))
                self._retrieve(
                    i - 1,
                    j - 1,
                    s + self.sigma_sub(seq1[i - 1], seq2[j - 1]),
                    S,
                    T,
                    seq1,
                    seq2,
                    out,
                )
        return out

    def align(
        self, seq1: List[Text], seq2: List[Text], epsilon: float = 0
    ) -> List[List[Tuple[Text, Text]]]:
        """
        Computes the alignment of two symbol sequences.

        :param seq1: a sequence of symbols
        :param seq2: a sequence of symbols

        :type epsilon: float (0.0 to 1.0)
        :param epsilon: Adjusts threshold similarity score for near-optimal alignments
        :return: Alignment(s) of seq1 and seq2
        (Kondrak 2002: 51)
        """

        assert 0.0 <= epsilon <= 1.0, "Epsilon must be between 0.0 and 1.0."

        m = len(seq1)
        n = len(seq2)
        # This includes Kondrak's initialization of row 0 and column 0 to all 0s.
        S = np.zeros((m + 1, n + 1), dtype=float)
        # If i <= 1 or j <= 1, don't allow expansions as it doesn't make sense,
        # and breaks array and string indices. Make sure they never get chosen
        # by setting them to -inf.
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                edit1 = S[i - 1, j] + self.sigma_skip(seq1[i - 1])
                edit2 = S[i, j - 1] + self.sigma_skip(seq2[j - 1])
                edit3 = S[i - 1, j - 1] + self.sigma_sub(seq1[i - 1], seq2[j - 1])
                if i > 1:
                    edit4 = S[i - 2, j - 1] + self.sigma_exp(
                        seq2[j - 1], seq1[i - 2 : i]
                    )
                else:
                    edit4 = -ReAline.inf
                if j > 1:
                    edit5 = S[i - 1, j - 2] + self.sigma_exp(
                        seq1[i - 1], seq2[j - 2 : j]
                    )
                else:
                    edit5 = -ReAline.inf
                S[i, j] = max(edit1, edit2, edit3, edit4, edit5, 0)
        T = (1 - epsilon) * np.amax(S)  # Threshold score for near-optimal alignments

        alignments = []
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if S[i, j] >= T:
                    alignments.append(self._retrieve(i, j, 0, S, T, seq1, seq2, []))
        return alignments
