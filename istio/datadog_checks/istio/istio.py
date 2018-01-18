# (C) Datadog, Inc. 2010-2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

# stdlib
import re
import traceback
from contextlib import closing, contextmanager
from collections import defaultdict

# 3p

# project
from config import _is_affirmative
from checks import AgentCheck

from . import mesh, mixer


class Istio(AgentCheck):

    def __init__(self, name, init_config, agentConfig, instances=None):
        super(Istio, self).__init__(name, init_config, agentConfig, instances)

        # Instead of one check, use three
        self.mesh_check = mesh.IstioMeshCheck(name, init_config, agentConfig, instances)
        self.mixer_check = mixer.MixerCheck(name, init_config, agentConfig, instances)

        # Put them in an array, so that duplicate actions are easier
        self.checks = [self.mesh_check, self.mixer_check]

        # Make sure they all have the same aggregator so that the status page works
        for check in self.checks:
            check.aggregator = self.aggregator


    def check(self, instance):
        self.log.debug('running all istio checks')

        # run the checks
        for check in self.checks:
            check.check(instance)
