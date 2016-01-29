#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, License LGPL 2.1

from setuptools import setup, find_packages

info = dict()
with open("INFO") as f: exec(f.read(),info)

setup(
  name=info["name"],
  version=info["version"],
  description=info["title"],
  author=info["author"],
  url=info["url"],
  packages = find_packages(),
  entry_points={
    "console_scripts": [
      "mknew=mknew.mknew:main"
    ]
  },
  license = info["license"]  
)