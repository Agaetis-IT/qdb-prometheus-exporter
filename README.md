# QuasarDB Prometheus Exporter

## Third party libraries

- Prometheus Python Client [https://github.com/prometheus/client_python] 
- QuasarDB API [https://doc.quasardb.net/master/api/python.html]

## Script arguments

- __exporter_http_host__: Exporter HTTP hostname, defaults to `''`, 
- __exporter_http_port__: Exporter HTTP port, defaults to `8080`, 
- __exporter_metric_prefix__: Exporter metrics prefix, defaults to `qdb`, 
- __qdb_cluster_public_key__: QuasarDB cluster public key absolute file path, defaults to `None`, 
- __qdb_max_metrics__: Max number of metrics retrieved from QuasarDB, defaults to `200`, 
- __qdb_uri__: QuasarDB cluster URI, defaults to `qdb://127.0.0.1:2836`, 
- __qdb_user_name__: QuasarDB username, defaults to `''`, 
- __qdb_user_private_key__: QuasarDB user private key absolute file path, defaults to `None`
- __qdb_node_id__: QuasarDB node id to invoke, this value is mandatory and if the node id do not match any of the cluster no statistics while be available., defaults to `'0-0-0-1'`

## Installation

### Pre requisites

- qdb-api=3.5.0

## Run 

```bash
qdb-prometheus-exporter --qdb_node_id=0-0-0-1 --qdb_uri=qdb://qdb-server:2836 --exporter_http_port=9090
```