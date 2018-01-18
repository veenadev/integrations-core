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
from checks.prometheus_check import PrometheusCheck


class IstioMeshCheck(PrometheusCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        super(IstioMeshCheck, self).__init__(name, init_config, agentConfig, instances)

        self.NAMESPACE = 'istio.mesh'

        self.metrics_mapper = {
            'istio_request_count': 'istio_request_count',
            'istio_request_duration': 'istio_request_duration',
            'istio_request_size': 'istio_request_size',
            'istio_response_size': 'istio_response_size',
        }
        self.ignore_metrics = []
        self.label_joins = {}
        self._dry_run = False

    def check(self, instance):
        self.log.debug('running istio mesh check')

        istio_mesh_endpoint = instance.get('istio_mesh_endpoint')

        send_buckets = instance.get('send_histograms_buckets', True)
        # By default we send the buckets.
        if send_buckets is not None and str(send_buckets).lower() == 'false':
            send_buckets = False
        else:
            send_buckets = True

        self.process(istio_mesh_endpoint, send_histograms_buckets=send_buckets, instance=instance)
