"""Configuration file for the PyBuilder build tool."""
#   -*- coding: utf-8 -*-
# pylint: skip-file
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.flake8")
use_plugin("python.distutils")

name = "G85.2025.T07.GE2.bis"
default_task = "publish"


@init
def set_properties(project):
    pass
