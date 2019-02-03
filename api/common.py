#!/usr/bin/env python3

import json
import os

"""
returns a JSON object of the config file
"""
def config():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, '../config/config.json')

    with open(filename) as cfg:
        data = json.load(cfg)
    return data

if __name__ == "__main__":
    print(config())
