#!/usr/bin/python3
"""
Contains tests for Base class
"""

import unittest
import inspect
import pep8
import json
from models.square import Square
from models.rectangle import Rectangle
from models import base
Base = base.Base


class TestBaseDocs(unittest.TestCase):
    """Tests to check the documentation and style of Base class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.base_funcs = inspect.getmembers(Base, inspect.isfunction)

    def test_pep8_conformance_base(self):
        """Test that models/base.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/base.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_base(self):
        """Test that tests/test_models/test_base.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['tests/test_models/test_base.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Tests for the module docstring"""
        self.assertTrue(len(base.__doc__) >= 1)

    def test_class_docstring(self):
        """Tests for the Base class docstring"""
        self.assertTrue(len(Base.__doc__) >= 1)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        for func in self.base_funcs:
            self.assertTrue(len(func[1].__doc__) >= 1)


class TestBase(unittest.TestCase):
    """Tests to check functionality of Base class"""
    def test_too_many_args(self):
        """test too many args to init"""
        with self.assertRaises(TypeError):
            b = Base(1, 1)

    def test_no_id(self):
        """Tests id as None"""
        b = Base()
        self.assertEqual(b.id, 1)

    def test_id_set(self):
        """Tests id as not None"""
        b98 = Base(98)
        self.assertEqual(b98.id, 98)

    def test_no_id_after_set(self):
        """Tests id as None after not None"""
        b2 = Base()
        self.assertEqual(b2.id, 2)

    def test_nb_private(self):
        """Tests nb_objects as a private instance attribute"""
        b = Base(3)
        with self.assertRaises(AttributeError):
            print(b.nb_objects)
        with self.assertRaises(AttributeError):
            print(b.__nb_objects)

    def test_to_json_string(self):
        """Tests regular to json string"""
        Base._Base__nb_objects = 0
        d1 = {"id": 9, "width": 5, "height": 6, "x": 7, "y": 8}
        d2 = {"id": 2, "width": 2, "height": 3, "x": 4, "y": 0}
        json_s = Base.to_json_string([d1, d2])
        self.assertTrue(type(json_s) is str)
        d = json.loads(json_s)
        self.assertEqual(d, [d1, d2])

    def test_empty_to_json_string(self):
        """Test for passing empty list/ None"""
        json_s = Base.to_json_string([])
        self.assertTrue(type(json_s) is str)
        self.assertEqual(json_s, "[]")

    def test_None_to_json_String(self):
        json_s = Base.to_json_string(None)
        self.assertTrue(type(json_s) is str)
        self.assertEqual(json_s, "[]")

    def test_from_json_string(self):
        """Tests regular from_json_string"""
        json_str = '[{"id": 9, "width": 5, "height": 6, "x": 7, "y": 8}, \
{"id": 2, "width": 2, "height": 3, "x": 4, "y": 0}]'
        json_l = Base.from_json_string(json_str)
        self.assertTrue(type(json_l) is list)
        self.assertEqual(len(json_l), 2)
        self.assertTrue(type(json_l[0]) is dict)
        self.assertTrue(type(json_l[1]) is dict)
        self.assertEqual(json_l[0],
                         {"id": 9, "width": 5, "height": 6, "x": 7, "y": 8})
        self.assertEqual(json_l[1],
                         {"id": 2, "width": 2, "height": 3, "x": 4, "y": 0})

    def test_fjs_empty(self):
        """Tests from_json_string with an empty string"""
        self.assertEqual([], Base.from_json_string(""))

    def test_fjs_None(self):
        """Tests from_json_string with an empty string"""
        self.assertEqual([], Base.from_json_string(None))

    def test_read_from_file_basic(self):
        """tests the base class method to read from json files when
            -> input is basic
        """
        r1 = Rectangle(10, 7, 8, 3, 44)
        r2 = Rectangle(24, 23, 5, 1, 99)
        Rectangle.save_to_file([r1, r2])
        with open('Rectangle.json', 'r', encoding='utf-8') as myFile:
            text = myFile.read()
        rects = Rectangle.load_from_file()
        self.assertEqual(rects[0].width, 10)
        self.assertEqual(rects[1].id, 99)
        self.assertEqual(rects[1].x, 5)

    def test_write_csv_basic(self):
        """tests the base class method to write instances as csv
        """
        r1 = Rectangle(10, 7, 2, 8, 33)
        r2 = Rectangle(10, 8, 4, 9, 44)
        Rectangle.save_to_file_csv([r1, r2])
        with open('Rectangle.csv', 'r', encoding='utf-8') as myFile:
            text = myFile.readlines()
        self.assertEqual(text[0][0] + text[0][1], "33")
        self.assertEqual(text[1][0] + text[1][1], "44")

    def test_read_csv_basic(self):
        """tests the base class method to read from csv
            -> basic input
        """
        r1 = Rectangle(10, 7, 2, 8)
        r2 = Rectangle(2, 4)
        list_rectangles_input = [r1, r2]
        Rectangle.save_to_file_csv(list_rectangles_input)
        list_output = Rectangle.load_from_file_csv()
        self.assertEqual(8, list_output[0].y)
        self.assertEqual(4, list_output[1].height)
        self.assertEqual(4, list_output[1].height)

    def test_read_csv_empty(self):
        """
        Testing read csv
        """
        try:
            os.remove('Square.csv')
        except Exception:
            pass
        list_output = Square.load_from_file_csv()
        self.assertEqual(0, len(list_output))
        self.assertEqual(list, type(list_output))


if __name__ == '__main__':
    unittest.main()
