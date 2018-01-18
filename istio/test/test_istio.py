# (C) Datadog, Inc. 2010-2017
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
from os import environ

# 3rd-party
from nose.plugins.attrib import attr

# project
from checks import AgentCheck
from utils.platform import Platform
from tests.checks.common import AgentCheckTest

class TestIstio(AgentCheckTest):

    def test_istio(self):
        pass
        config = {'instances': [{
            
        }]}
        self.run_check(config)

        self.assertTrue(True)
