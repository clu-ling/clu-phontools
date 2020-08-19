# -*- coding: utf-8 -*-

import unittest
from realine import *
import os


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

'''
Test alignment of pairs
'''

class ReAlineTests(unittest.TestCase):
    
    def test_same_input(self):
        sounds = []
        phrase = []
        self.assertEqual(sounds, phrase, "sounds and phrases did not align")
