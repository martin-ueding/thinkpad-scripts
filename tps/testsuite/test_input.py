#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Martin Ueding <martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

import unittest

import tps.input

class InputTestCase(unittest.TestCase):
    def test_matrix_mult_unity(self):
        unity = [
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
        ]

        prod = tps.input._matrix_mul(unity, unity)

        self.assertEqual(prod, unity)

    def test_matrix_mult_unity(self):
        unity = [
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
        ]
        orthogonal = [
            0, -1, 0,
            1, 0, 0,
            0, 0, 1,
        ]

        prod = tps.input._matrix_mul(orthogonal, orthogonal)
        prod = tps.input._matrix_mul(prod, prod)

        self.assertEqual(prod, unity)

    def test_matrix_mult_arbitrary(self):
        m1 = [3, 9, -3, 5, 9, 40, 69, -12, -45]
        m2 = [653, 23, 12, 54, 76, 12, 45, 65, 91]
        m1m2 = [2310, 558, -129, 5551, 3399, 3808, 42384, -2250, -3411]

        prod = tps.input._matrix_mul(m1, m2)

        self.assertEqual(prod, m1m2)
