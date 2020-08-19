from features import *

try:
    import numpy as np
except ImportError:
    np = None

class ReAline(object):
    def __init__(self):
        #self.str1 = str1
        #self.str2 = str2
        pass
    def sigma_skip(self,p):
        """
        Returns score of an indel of P.
        (Kondrak 2002: 54)
        """
        return C_skip
    def V(self, p):
        """
        Return vowel weight if P is vowel.
        (Kondrak 2002: 54)
        """
        if p in consonants:
            return 0
        return C_vwl
    def R(self, p, q):
        """
        Return relevant features for segment comparsion.
        (Kondrak 2002: 54)
        """
        if p in consonants or q in consonants:
            return R_c
        return R_v
    def diff(self,p, q, f):
        """
        Returns difference between phonetic segments P and Q for feature F.
        (Kondrak 2002: 52, 54)
        """
        p_features, q_features = feature_matrix[p], feature_matrix[q]
        return abs(similarity_matrix[p_features[f]] - similarity_matrix[q_features[f]])
    def delta(self, p, q):
        """
        Return weighted sum of difference between P and Q.
        (Kondrak 2002: 54)
        """
        features = self.R(p, q)
        total = 0
        for f in features:
            total += self.diff(p, q, f) * salience[f]
        return total
    def sigma_sub(self, p, q):
        """
        Returns score of a substitution of P with Q.
        (Kondrak 2002: 54)
        """
        return C_sub - self.delta(p, q) - self.V(p) - self.V(q)
    def sigma_exp(self, p, q):
        """
        Returns score of an expansion/compression.
        (Kondrak 2002: 54)
        """
        q1 = q[0]
        q2 = q[1]
        return C_exp - self.delta(p, q1) - self.delta(p, q2) - self.V(p) - max(self.V(q1), self.V(q2))

    def _retrieve(self,i, j, s, S, T, str1, str2, out):
        """
        Retrieve the path through the similarity matrix S starting at (i, j).

        :rtype: list(tuple(str, str))
        :return: Alignment of str1 and str2
        """
        if S[i, j] == 0:
            return out
        else:
            if j > 1 and S[i-1, j-2] + self.sigma_exp(str1[i-1], str2[j-2:j]) + s >= T:
                out.insert(0, (str1[i-1], str2[j-2:j]))
                self._retrieve(
                    i-1, j-2, s+self.sigma_exp(str1[i-1], str2[j-2:j]), S, T, str1, str2, out)
            elif i > 1 and S[i-2, j-1] + self.sigma_exp(str2[j-1], str1[i-2:i]) + s >= T:
                out.insert(0, (str1[i-2:i], str2[j-1]))
                self._retrieve(
                    i-2, j-1, s+self.sigma_exp(str2[j-1], str1[i-2:i]), S, T, str1, str2, out)
            elif S[i, j-1] + self.sigma_skip(str2[j-1]) + s >= T:
                out.insert(0, ('-', str2[j-1]))
                self._retrieve(i, j-1, s+self.sigma_skip(str2[j-1]), S, T, str1, str2, out)
            elif S[i-1, j] + self.sigma_skip(str1[i-1]) + s >= T:
                out.insert(0, (str1[i-1], '-'))
                self._retrieve(i-1, j, s+self.sigma_skip(str1[i-1]), S, T, str1, str2, out)
            elif S[i-1, j-1] + self.sigma_sub(str1[i-1], str2[j-1]) + s >= T:
                out.insert(0, (str1[i-1], str2[j-1]))
                self._retrieve(
                    i-1, j-1, s+self.sigma_sub(str1[i-1], str2[j-1]), S, T, str1, str2, out)
        return out


    def align(self, str1, str2, epsilon=0):
        """
        Compute the alignment of two phonetic strings.
        :type str1, str2: str
        :param str1, str2: Two strings to be aligned
        :type epsilon: float (0.0 to 1.0)
        :param epsilon: Adjusts threshold similarity score for near-optimal alignments
        :rtpye: list(list(tuple(str, str)))
        :return: Alignment(s) of str1 and str2
        (Kondrak 2002: 51)
        """
        if np == None:
            raise ImportError('You need numpy in order to use the align function')

        assert 0.0 <= epsilon <= 1.0, "Epsilon must be between 0.0 and 1.0."

        m = len(str1)
        n = len(str2)
        # This includes Kondrak's initialization of row 0 and column 0 to all 0s.
        S = np.zeros((m+1, n+1), dtype=float)
        # If i <= 1 or j <= 1, don't allow expansions as it doesn't make sense,
        # and breaks array and string indices. Make sure they never get chosen
        # by setting them to -inf.
        for i in range(1, m+1):
            for j in range(1, n+1):
                edit1 = S[i-1, j] + self.sigma_skip(str1[i-1])
                edit2 = S[i, j-1] + self.sigma_skip(str2[j-1])
                edit3 = S[i-1, j-1] + self.sigma_sub(str1[i-1], str2[j-1])
                if i > 1:
                    edit4 = S[i-2, j-1] + self.sigma_exp(str2[j-1], str1[i-2:i])
                else:
                    edit4 = -inf
                if j > 1:
                    edit5 = S[i-1, j-2] + self.sigma_exp(str1[i-1], str2[j-2:j])
                else:
                    edit5 = -inf
                S[i, j] = max(edit1, edit2, edit3, edit4, edit5, 0)
        T = (1-epsilon)*np.amax(S)  # Threshold score for near-optimal alignments
        
        alignments = []
        for i in range(1, m+1):
            for j in range(1, n+1):
                if S[i, j] >= T:
                    alignments.append(self._retrieve(i, j, 0, S, T, str1, str2, []))
        return alignments

