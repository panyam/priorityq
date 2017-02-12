#!/usr/bin/env python

import unittest
test_modules = []

alltests = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(test_module.Tests) for test_module in test_modules
    ])
unittest.TextTestRunner(verbosity=2).run(alltests)
