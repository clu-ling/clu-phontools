# -*- coding: utf-8 -*-

import unittest
from typing import Sequence
from clu.phontools.arabictools import *

"""
Test `clu.phontools.arabictools.BuckwalterConverter` behavior
"""

class TestBuckwalterConverter(unittest.TestCase):
    arabic = "يُولَدُ جَمِيعُ ٱلنَّاسِ أَحْرَارًا مُتَسَاوِينَ فِي ٱلْكَرَامَةِ وَٱلْحُقُوقِ. وَقَدْ وُهِبُوا عَقْلًا وَضَمِيرًا وَعَلَيْهِمْ أَنْ يُعَامِلَ بَعْضُهُمْ بَعْضًا بِرُوحِ ٱلْإِخَاءِ"
    buck = "yuwladu jamiyEu {lna~Asi >aHoraArFA mutasaAwiyna fiy {lokaraAmapi wa{loHuquwqi. waqado wuhibuwA EaqolFA waDamiyrFA waEalayohimo >ano yuEaAmila baEoDuhumo baEoDFA biruwHi {lo<ixaA'i"

    def test_arabic_to_buckwalter(self):
        res = BuckwalterConverter.convert_arabic_to_buckwalter(self.arabic)
        self.assertEqual(
            res, self.buck, f"`clu.phontools.arabictools.BuckwalterConverter.convert_arabic_to_buckwalter(arabic)` should return {self.buck}" 
        )

    def test_buckwalter_to_arabic(self):
        res = BuckwalterConverter.convert_buckwalter_to_arabic(self.buck)
        self.assertEqual(
            res, self.arabic, f"`clu.phontools.arabictools.BuckwalterConverter.convert_buckwalter_to_arabic(buck)` should return {self.arabic}" 
        )

"""
Test `clu.phontools.arabictools.IPAConverter` behavior
"""

class TestIPAConverter(unittest.TestCase):
    pass



if __name__ == '__main__':
    unittest.main()