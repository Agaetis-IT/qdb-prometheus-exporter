import logging
import socket

import quasardb
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client.metrics_core import InfoMetricFamily

from .metrics import MetricType, get_metrics_metadata


class QdbCollector(object):
    def __init__(self, qdb_cluster: quasardb.Cluster, max_metrics: int = 100, prefix: str = 'qdb'):
        self._cluster = qdb_cluster
        self._max_metrics = max_metrics
        self._hostname = socket.getfqdn()
        self._prefix = prefix
        self._available_statistics = dict()

        self.retrieve_available_statistics()

    def collect_metric(self, metric_type: MetricType, metric_key: str):

        fn = metric_type.lookup_function(self._cluster)

        metric_full_key = self._available_statistics[metric_key]

        value = fn(metric_full_key)

        return value

    def collect(self):

        node_id = self.collect_metric(metric_type=MetricType.INFO, metric_key="node_id")

        for statistic in self._available_statistics:
            metadata = get_metrics_metadata(statistic)
            name = self.metric_name(statistic)

            logging.info("Collecting metric {}.", statistic)

            if metadata['type'] == MetricType.COUNTER:
                metric = CounterMetricFamily(name=name,
                                             documentation=metadata['description'],
                                             labels=["node", "host"],
                                             unit=metadata['unit'])
                metric.add_metric(labels=[node_id, self._hostname],
                                  value=self.collect_metric(metric_type=metadata['type'], metric_key=statistic))
                yield metric

            if metadata['type'] == MetricType.GAUGE:
                metric = GaugeMetricFamily(name=name,
                                           documentation=metadata['description'],
                                           labels=["node", "host"],
                                           unit=metadata['unit'])
                metric.add_metric(labels=[node_id, self._hostname],
                                  value=self.collect_metric(metric_type=metadata['type'], metric_key=statistic))
                yield metric

            if metadata['type'] == MetricType.INFO:
                metric = InfoMetricFamily(name=name,
                                          documentation=metadata['description'],
                                          labels=["node", "host"])
                metric.add_metric(labels=[node_id, self._hostname],
                                  value={
                                      statistic: self.collect_metric(metric_type=metadata['type'], metric_key=statistic)
                                  })
                yield metric

    def metric_name(self, metric_key: str):
        return "{}_{}".format(self._prefix, metric_key.replace('.', '_'))

    def retrieve_available_statistics(self):
        """
        Retrieve all metric names provided by QuasarDB and assign the simple name to the fully qualified named (which includes the node id).

        :return:
        """
        statistics = self._cluster.prefix_get("$qdb.statistics", self._max_metrics)

        for statistic in statistics:
            self._available_statistics[statistic.split(sep='.', maxsplit=3)[-1]] = statistic
