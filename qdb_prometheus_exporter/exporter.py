import argparse
import time

from prometheus_client.exposition import start_http_server
from prometheus_client.registry import CollectorRegistry, REGISTRY
from quasardb import quasardb

from qdb_prometheus_exporter.collector import QdbCollector


class QdbExporter(object):
    def __init__(self,
                 qdb_uri: str,
                 qdb_node: str,
                 registry: CollectorRegistry = REGISTRY,
                 http_host: str = '',
                 http_port: int = 8080,
                 **kwargs):
        qdb_kwargs = dict()
        collector_kwargs = dict()

        if kwargs.get('qdb_user_name'): qdb_kwargs['user_name'] = kwargs.get('qdb_user_name')
        if kwargs.get('qdb_user_private_key'):
            try:
                with open(file=kwargs.get('qdb_user_private_key'), mode='r') as f:
                    user_private_key = f.read()
                    qdb_kwargs['user_private_key'] = user_private_key
            except Exception:
                qdb_kwargs['user_private_key'] = str(kwargs.get('qdb_user_private_key'))
        if kwargs.get('qdb_cluster_public_key'):
            try:
                with open(file=kwargs.get('qdb_cluster_public_key'), mode='r') as f:
                    user_private_key = f.read()
                    qdb_kwargs['cluster_public_key'] = user_private_key
            except Exception:
                qdb_kwargs['cluster_public_key'] = str(kwargs.get('qdb_cluster_public_key'))


        if kwargs.get('qdb_max_metrics'): collector_kwargs['max_metrics'] = kwargs.get('qdb_max_metrics')
        if kwargs.get('qdb_prefix_statistics'): collector_kwargs['prefix_statistics'] = kwargs.get('qdb_prefix_statistics')
        if kwargs.get('prefix'): collector_kwargs['prefix'] = kwargs.get('prefix')

        self._cluster = quasardb.Cluster(uri=qdb_uri, **qdb_kwargs)
        self._direct_connection = self._cluster.node(qdb_node)

        self._collector = QdbCollector(qdb_direct_connection=self._direct_connection, qdb_node=qdb_node, **collector_kwargs)

        self._registry = registry

        self._http_host = http_host
        self._http_port = http_port

        if self._registry:
            self._registry.register(self._collector)

    def start(self):
        start_http_server(port=self._http_port, addr=self._http_host, registry=self._registry)

        while True:
            time.sleep(1)


def get_args():
    parser = argparse.ArgumentParser(description="QuasarDB metrics exporter used to Prometheus")
    parser.add_argument("--qdb_uri",
                        dest="qdb_uri",
                        type=str,
                        help='QuasarDB cluster uri to connect to. Defaults to qdb://127.0.0.1:2836',
                        default='qdb://127.0.0.1:2836')
    parser.add_argument("--qdb_node",
                        dest="qdb_node",
                        type=str,
                        help='QuasarDB cluster direct node used for statistics collection. Defaults to 127.0.0.1:2836',
                        required=True,
                        default='127.0.0.1:2836')
    parser.add_argument("--qdb_user_name",
                        dest="qdb_user_name",
                        type=str,
                        help='QuasarDB cluster username. Defaults to ""',
                        default='')
    parser.add_argument("--qdb_user_private_key",
                        dest="qdb_user_private_key",
                        type=str,
                        help='QuasarDB cluster user private file. Defaults to None',
                        default=None)
    parser.add_argument("--qdb_cluster_public_key",
                        dest="qdb_cluster_public_key",
                        help='QuasarDB cluster user public key file. Defaults to None',
                        type=str,
                        default=None)
    parser.add_argument("--qdb_max_metrics",
                        dest="qdb_max_metrics",
                        type=int,
                        help='Max metrics to retrieve from QuasarDB cluster. Defaults to 100',
                        default=200)

    parser.add_argument("--qdb_prefix_statistics",
                        dest="qdb_prefix_statistics",
                        help='QuasarDB cluster statistics prefix. Ued to get all statistics by prefix., Default to $qdb.statistics.',
                        type=str,
                        default='$qdb.statistics.')
    parser.add_argument("--exporter_http_port",
                        dest="exporter_http_port",
                        type=int,
                        help='HTTP exporter port. Defaults to 8080',
                        default=8080)
    parser.add_argument("--exporter_http_host",
                        dest="exporter_http_host",
                        type=str,
                        help='HTTP exporter host. Defaults to ""',
                        default='')
    parser.add_argument("--exporter_metric_prefix",
                        dest="exporter_metric_prefix",
                        type=str,
                        help='Metric prefix. Defaults to "qdb"',
                        default='qdb')
    return parser.parse_args()


def main():
  args = get_args()

  exporter = QdbExporter(
      qdb_uri=args.qdb_uri,
      qdb_node=args.qdb_node,
      qdb_user_name=args.qdb_user_name,
      qdb_user_private_key=args.qdb_user_private_key,
      qdb_cluster_public_key=args.qdb_cluster_public_key,
      qdb_max_metrics=args.qdb_max_metrics,
      qdb_prefix_statistics=args.qdb_prefix_statistics,
      http_host=args.exporter_http_host,
      http_port=args.exporter_http_port,
      prefix=args.exporter_metric_prefix
  )

  exporter.start()
