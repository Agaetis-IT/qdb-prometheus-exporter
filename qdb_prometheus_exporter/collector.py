import logging
import re
import socket

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily
from prometheus_client.metrics_core import InfoMetricFamily
from quasardb.quasardb import Node

from qdb_prometheus_exporter.metrics import MetricType, get_metrics_metadata

def sanitize(key: str) -> str:
  return re.sub(r'[^a-zA-Z_]', '_', key)

class QdbCollector(object):
  def __init__(self, qdb_direct_connection: Node, qdb_node: str,
      max_metrics: int = 100, prefix: str = 'qdb',
      prefix_statistics: str = '$qdb.statistics.'):
    self._direct_connection = qdb_direct_connection
    self._node = qdb_node
    self._max_metrics = max_metrics
    self._hostname = socket.getfqdn()
    self._prefix = prefix
    self._prefix_statistics = prefix_statistics
    self._available_statistics = dict()

    self.retrieve_available_statistics()

  def collect_metric(self, metric_type: MetricType, metric_key: str):

    fn = metric_type.lookup_function(self._direct_connection)

    metric_full_key = self._available_statistics[metric_key]

    value = fn(metric_full_key)

    return value

  def collect(self):
    for statistic in self._available_statistics:
      try:
        metadata = get_metrics_metadata(statistic)
        name = self.metric_name(statistic)

        logging.info("Collecting metric %s.", statistic)

        metric_value = self.collect_metric(metric_type=metadata['type'],
                                           metric_key=statistic)

        if metadata['type'] == MetricType.COUNTER:
          metric = CounterMetricFamily(name=name,
                                       documentation=metadata['description'],
                                       labels=["node", "host"],
                                       unit=metadata['unit'])
          metric.add_metric(labels=[self._node, self._hostname],
                            value=metric_value)
          yield metric

        elif metadata['type'] == MetricType.GAUGE:
          metric = GaugeMetricFamily(name=name,
                                     documentation=metadata['description'],
                                     labels=["node", "host"],
                                     unit=metadata['unit'])
          metric.add_metric(labels=[self._node, self._hostname],
                            value=metric_value)
          yield metric

        elif metadata['type'] == MetricType.INFO:
          metric = InfoMetricFamily(name=name,
                                    documentation=metadata['description'],
                                    labels=["node", "host"])
          metric.add_metric(labels=[self._node, self._hostname],
                            value={
                              sanitize(statistic): metric_value
                            })
          yield metric
      except KeyError as e:
        logging.warning("Key do not exists: %s.", e.args[0])

  def metric_name(self, metric_key: str):
    return "{}_{}".format(self._prefix, metric_key.replace('.', '_'))

  def retrieve_available_statistics(self):
    """
    Retrieve all metric names provided by QuasarDB and assign the simple name to the fully qualified named.

    :return:
    """
    statistics = self._direct_connection.prefix_get(self._prefix_statistics,
                                                    self._max_metrics)

    for statistic in statistics:
      statistic_key = statistic[
                      statistic.startswith(self._prefix_statistics) and len(
                        self._prefix_statistics):]
      self._available_statistics[statistic_key] = statistic
