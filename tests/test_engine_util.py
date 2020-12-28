import unittest
from engine import engine_util
from engine.engine_constants import N_RANKS, N_FILES
import numpy as np


class TestEngineUtil(unittest.TestCase):

    def test_bitboard_to_locations_0_0(self):
        bitboard_0_0 = int('1' + '0' * (N_FILES * N_FILES - 1), 2)

        self.assertEqual([(0,0)], engine_util.bitboard_to_locations(bitboard_0_0))

    def test_bitboard_to_locations_8_9(self):
        bitboard_0_0 = int('1', 2)
        print(np.binary_repr(bitboard_0_0, width=90))

        self.assertEqual([(8, 9)], engine_util.bitboard_to_locations(bitboard_0_0))

    def test_bitboard_to_locations_3_4(self):
        bitboard_0_0 = int('0'*N_FILES*4 + '000010000' + (N_RANKS-5)*'0', 2)

        print(np.binary_repr(bitboard_0_0, width=90))

        self.assertEqual([(3, 4)], engine_util.bitboard_to_locations(bitboard_0_0))
