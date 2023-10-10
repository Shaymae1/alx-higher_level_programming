#!/usr/bin/python3
"""import json for encoding and decoding the json file
import sys to help parse through the arguments
import os.path to help check if the file exists"""
import json
import os.path
import sys

"""importing the necessary modules to help in craeting object from
JSON file and write an object text file using json representation"""
enc = __import__('5-save_to_json_file').save_to_json_file
dec = __import__('6-load_from_json_file').load_from_json_file

my_list = []
filename = "add_item.json"

if os.path.isfile(filename):
    """decode the json file if the file exists"""
    my_list = dec(filename)

"""loop through the list of arguments"""
for arg in sys.argv[1:]:
    my_list.append(arg)

enc(my_list, "add_item.json")
