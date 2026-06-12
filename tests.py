"""Tests for pwgen."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from pwgen.core import generate_random, generate_pronounceable, estimate_entropy, DIGITS


class TestPwgen(unittest.TestCase):

    def test_random_length(self):
        pwd = generate_random(length=12)
        self.assertEqual(len(pwd), 12)

    def test_random_default_length(self):
        pwd = generate_random()
        self.assertEqual(len(pwd), 20)

    def test_random_no_symbols(self):
        pwd = generate_random(length=32, pools=["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789"])
        self.assertEqual(len(pwd), 32)
        for c in pwd:
            self.assertIn(c, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    def test_pin_only_digits(self):
        for _ in range(10):
            pwd = generate_random(length=6, pools=[DIGITS])
            self.assertEqual(len(pwd), 6)
            self.assertTrue(pwd.isdigit())

    def test_pronounceable_words(self):
        pwd = generate_pronounceable(words=3)
        parts = pwd.split("-")
        self.assertEqual(len(parts), 3)

    def test_pronounceable_capitalize(self):
        pwd = generate_pronounceable(words=2, capitalize=True)
        parts = pwd.split("-")
        for p in parts:
            self.assertTrue(p[0].isupper())

    def test_pronounceable_with_digit(self):
        pwd = generate_pronounceable(words=2, add_digit=True)
        self.assertTrue(pwd[-1].isdigit())

    def test_pronounceable_custom_separator(self):
        pwd = generate_pronounceable(words=2, separator=".")
        self.assertIn(".", pwd)
        self.assertNotIn("-", pwd)

    def test_estimate_entropy(self):
        e = estimate_entropy(20, 72)
        self.assertGreater(e, 100)
        self.assertLess(e, 200)

    def test_estimate_entropy_zero(self):
        self.assertEqual(estimate_entropy(0, 72), 0.0)
        self.assertEqual(estimate_entropy(20, 0), 0.0)

    def test_random_uniqueness(self):
        passwords = {generate_random(length=20) for _ in range(100)}
        self.assertEqual(len(passwords), 100)

    def test_pronounceable_uniqueness(self):
        passwords = {generate_pronounceable(words=4) for _ in range(50)}
        # Should be at least 48 unique out of 50
        self.assertGreaterEqual(len(passwords), 48)


if __name__ == "__main__":
    unittest.main()
