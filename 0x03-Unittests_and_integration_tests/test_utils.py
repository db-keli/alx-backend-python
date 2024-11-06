#!/usr/bin/env python3
"""Test utils Module"""


import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized

utils = __import__('utils')


class TestAccessNestedMap(unittest.TestCase):
    """Access Map Test Class"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test Access Nested Map"""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Test Access Nested Map Exception"""
        with self.assertRaises(expected):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Get Json Test Class"""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test Get Json"""
        test_cases = [
            ("http://example.com", {"test_payload": True}),
            ("http://holberton.io", {"test_payload": False}),
        ]

        for test_case in test_cases:
            mock_get.return_value = Mock(ok=True)
            mock_get.return_value.json.return_value = test_case[1]
            self.assertEqual(utils.get_json(test_case[0]), test_case[1])
            mock_get.assert_called_once_with(test_case[0])
            mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    """Memoize Test Class"""

    def test_memoize(self):
        """Test Memoize"""

        class TestClass:
            """Test Class"""

            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mm:
            test_class = TestClass()
            test_class.a_property
            test_class.a_property
            mm.assert_called_once()
