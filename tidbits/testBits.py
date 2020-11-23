import unittest

class TestString(unittest.TestCase):

    def test_compress(self, func):
        self.assertEqual(func(None), None)
        self.assertEqual(func(''), '')
        self.assertEqual(func('AABBCC'), 'AABBCC')
        self.assertEqual(func('AAABCCDDDD'), 'A3BCCD4')
        self.assertEqual(func('aaBCCEFFFFKKMMMMMMP taaammanlaarrrr seeeeeeeeek tooo'),
                        'aaBCCEF4KKM6P ta3mmanlaar4 se9k to3',)
        print('Success: test_compress')


    def test_commify(self, func):
        self.assertEqual(func(None), None)
        self.assertEqual(func(''), '')
        self.assertEqual(func('123456'), '123,456')
        self.assertEqual(func('ABCDEF'),'ABCDEF')
        self.assertEqual(func([123456]),[123456])
        self.assertEqual(func(123),'123')
        self.assertEqual(func(123456), '123,456')
        self.assertEqual(func(1234567), '1,234,567')
        self.assertEqual(func(12345.67), '12,345.67')
        print('Success: test_commify')


    def test_fizz_buzz(self, func):
        self.assertRaises(TypeError, func, None)
        self.assertRaises(ValueError, func, 0)
        expected = [
            '1',
            '2',
            'Fizz',
            '4',
            'Buzz',
            'Fizz',
            '7',
            '8',
            'Fizz',
            'Buzz',
            '11',
            'Fizz',
            '13',
            '14',
            'FizzBuzz'
        ]
        self.assertEqual(func(15), expected)
        print('Success: test_fizz_buzz')

    def test_reverse(self, func):
        self.assertEqual(func(None), None)
        self.assertEqual(func(['']), [''])
        self.assertEqual(func(
            ['f', 'o', 'o', ' ', 'b', 'a', 'r']),
            ['r', 'a', 'b', ' ', 'o', 'o', 'f'])
        print('Success: test_reverse')

    def test_reverse_inplace(self, func):
        target_list = ['f', 'o', 'o', ' ', 'b', 'a', 'r']
        func(target_list)
        self.assertEqual(target_list, ['r', 'a', 'b', ' ', 'o', 'o', 'f'])
        print('Success: test_reverse_inplace')

    def test_unique_chars(self, func):
        self.assertEqual(func(None), False)
        self.assertEqual(func(''), True)
        self.assertEqual(func('foo'), False)
        self.assertEqual(func('bar'), True)
        print('Success: test_unique_chars')

    def test_long_pressed(self, func):
        self.assertEqual(func(None, None), False)
        self.assertEqual(func(None, 'aleex'), False)
        self.assertEqual(func('alex', None), False)
        self.assertEqual(func('', ''), True)
        self.assertEqual(func('alex', ''), False)
        self.assertEqual(func('', 'aaaleex'), False)
        self.assertEqual(func('alex', 'aaleex'), True)
        self.assertEqual(func('saeed', 'ssaaedd'), False)
        self.assertEqual(func('leelee', 'lleeelee'), True)
        self.assertEqual(func('laiden', 'laiden'), True)
        print('Success: test_long_pressed')

    def test_find_diff(self, func):
        self.assertRaises(TypeError, func, None)
        self.assertEqual(func('ab', 'aab'), 'a')
        self.assertEqual(func('aab', 'ab'), 'a')
        self.assertEqual(func('abcd', 'abcde'), 'e')
        self.assertEqual(func('aaabbcdd', 'abdbacade'), 'e')
        print('Success: test_find_diff')
    
    def test_permutation(self, func):
        self.assertEqual(func(None, 'foo'), False)
        self.assertEqual(func('', 'foo'), False)
        self.assertEqual(func('Nib', 'bin'), False)
        self.assertEqual(func('act', 'cat'), True)
        self.assertEqual(func('a ct', 'ca t'), True)
        self.assertEqual(func('dog', 'doggo'), False)
        print('Success: test_permutation')