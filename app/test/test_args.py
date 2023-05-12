import unittest
from .. import args


class TestArgs(unittest.TestCase):
    def test_comma_cleanup_successes(self):
        cases = (
            (['1',], [1,]),
            (['1,',], [1,]),
            (['11',], [11,]),
            (['11,',], [11,]),
            (['-1', '2'], [-1, 2])
        )
        for input_, expectation in cases:
            with self.subTest(input=input_):
                args.cleanup_comma_seperated_args(input_)
                self.assertEqual(input_, expectation)

    def test_comma_cleanup_failures(self):
        cases = (
            ['1,,'],
            [',1'],
            [''],
            ['1', 'foo'],
        )
        for input_ in cases:
            with self.subTest(input=input_):
                self.assertRaises(
                    ValueError, args.cleanup_comma_seperated_args, input_
                )
