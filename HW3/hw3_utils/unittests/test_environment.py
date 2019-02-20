import unittest
from nose.tools import eq_, ok_
from distutils.version import LooseVersion

import nose
import sys
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib
import torch

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        pass

    def test_library_versions(self):
        min_python = '3.6'
        min_numpy = '1.16'
        min_pandas = '0.23'
        min_scipy = '1.2'
        min_matplotlib = '3.0'
        min_torch = '1.0'


        ok_(LooseVersion(sys.version) > LooseVersion(min_python))
        ok_(LooseVersion(np.__version__) > LooseVersion(min_numpy))
        ok_(LooseVersion(pd.__version__) > LooseVersion(min_pandas))
        ok_(LooseVersion(sp.__version__) > LooseVersion(min_scipy))
        ok_(LooseVersion(matplotlib.__version__) > LooseVersion(min_matplotlib))
        ok_(LooseVersion(torch.__version__) > LooseVersion(min_torch))