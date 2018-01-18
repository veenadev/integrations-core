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

class MixerCheck(PrometheusCheck):
    def __init__(self, name, init_config, agentConfig, instances=None):
        super(MixerCheck, self).__init__(name, init_config, agentConfig, instances)

        self.NAMESPACE = 'istio.mixer'

        self.metrics_mapper = {
            'go_gc_duration_seconds': 'go_gc_duration_seconds',
            'go_goroutines': 'go_goroutines',
            'go_info': 'go_info',
            'go_memstats_alloc_bytes': 'go_memstats_alloc_bytes',
            'go_memstats_alloc_bytes_total': 'go_memstats_alloc_bytes_total',
            'go_memstats_buck_hash_sys_bytes': 'go_memstats_buck_hash_sys_bytes',
            'go_memstats_frees_total': 'go_memstats_frees_total',
            'go_memstats_gc_cpu_fraction': 'go_memstats_gc_cpu_fraction',
            'go_memstats_gc_sys_bytes': 'go_memstats_gc_sys_bytes',
            'go_memstats_heap_alloc_bytes': 'go_memstats_heap_alloc_bytes',
            'go_memstats_heap_idle_bytes': 'go_memstats_heap_idle_bytes',
            'go_memstats_heap_inuse_bytes': 'go_memstats_heap_inuse_bytes',
            'go_memstats_heap_objects': 'go_memstats_heap_objects',
            'go_memstats_heap_released_bytes': 'go_memstats_heap_released_bytes',
            'go_memstats_heap_sys_bytes': 'go_memstats_heap_sys_bytes',
            'go_memstats_last_gc_time_seconds': 'go_memstats_last_gc_time_seconds',
            'go_memstats_lookups_total': 'go_memstats_lookups_total',
            'go_memstats_mallocs_total': 'go_memstats_mallocs_total',
            'go_memstats_mcache_inuse_bytes': 'go_memstats_mcache_inuse_bytes',
            'go_memstats_mcache_sys_bytes': 'go_memstats_mcache_sys_bytes',
            'go_memstats_mspan_inuse_bytes': 'go_memstats_mspan_inuse_bytes',
            'go_memstats_mspan_sys_bytes': 'go_memstats_mspan_sys_bytes',
            'go_memstats_next_gc_bytes': 'go_memstats_next_gc_bytes',
            'go_memstats_other_sys_bytes': 'go_memstats_other_sys_bytes',
            'go_memstats_stack_inuse_bytes': 'go_memstats_stack_inuse_bytes',
            'go_memstats_stack_sys_bytes': 'go_memstats_stack_sys_bytes',
            'go_memstats_sys_bytes': 'go_memstats_sys_bytes',
            'go_threads': 'go_threads',
            'grpc_server_handled_total': 'grpc_server_handled_total',
            'grpc_server_handling_seconds': 'grpc_server_handling_seconds',
            'grpc_server_msg_received_total': 'grpc_server_msg_received_total',
            'grpc_server_msg_sent_total': 'grpc_server_msg_sent_total',
            'grpc_server_started_total': 'grpc_server_started_total',
            'mixer_adapter_dispatch_count': 'mixer_adapter_dispatch_count',
            'mixer_adapter_dispatch_duration': 'mixer_adapter_dispatch_duration',
            'mixer_adapter_old_dispatch_count': 'mixer_adapter_old_dispatch_count',
            'mixer_adapter_old_dispatch_duration': 'mixer_adapter_old_dispatch_duration',
            'mixer_config_resolve_actions': 'mixer_config_resolve_actions',
            'mixer_config_resolve_count': 'mixer_config_resolve_count',
            'mixer_config_resolve_duration': 'mixer_config_resolve_duration',
            'mixer_config_resolve_rules': 'mixer_config_resolve_rules',
            'process_cpu_seconds_total': 'process_cpu_seconds_total',
            'process_max_fds': 'process_max_fds',
            'process_open_fds': 'process_open_fds',
            'process_resident_memory_bytes': 'process_resident_memory_bytes',
            'process_start_time_seconds': 'process_start_time_seconds',
            'process_virtual_memory_bytes': 'process_virtual_memory_bytes',
        }
        self.ignore_metrics = []
        self.label_joins = {}
        self._dry_run = False

    def check(self, instance):
        self.log.debug('running istio mixer check')
        mixer_endpoint = instance.get('mixer_endpoint')

        send_buckets = instance.get('send_histograms_buckets', True)
        # By default we send the buckets.
        if send_buckets is not None and str(send_buckets).lower() == 'false':
            send_buckets = False
        else:
            send_buckets = True


        self.process(mixer_endpoint, send_histograms_buckets=send_buckets, instance=instance)
