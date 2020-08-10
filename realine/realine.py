from __future__ import unicode_literals
from features import *

try:
    import numpy as np
except ImportError:
    np = None


def diff(p, q, f):
    """
    Returns difference between phonetic segments P and Q for feature F.

    (Kondrak 2002: 52, 54)
    """
    p_features, q_features = feature_matrix[p], feature_matrix[q]
    return abs(similarity_matrix[p_features[f]] - similarity_matrix[q_features[f]])

s = diff('p', 'b', 'voice')
print (s)