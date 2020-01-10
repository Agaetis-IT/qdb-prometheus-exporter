from enum import Enum

from quasardb.quasardb import Node


class MetricType(Enum):
    COUNTER = 1
    GAUGE = 2
    INFO = 3

    def lookup_function(self, qdb_direct_connection: Node):

        def string(key: str):
            return str(qdb_direct_connection.blob(key).get(), "utf-8").rstrip('\0')

        def integer(key: str):
            return qdb_direct_connection.integer(key).get()

        if self.value is self.COUNTER.value or self.value is self.GAUGE.value:
            return integer
        elif self.value is self.INFO.value:
            return string
        else:
            raise RuntimeError("Invalid value: ", str(self))


METRICS_METADATA = {
    'cpu.idle'                                                  : {
        'type'       : MetricType.COUNTER,
        'description': 'The cumulated CPU idle time',
        'unit'       : 'microseconds'
    },
    'cpu.system'                                                : {
        'type'       : MetricType.COUNTER,
        'description': 'The cumulated CPU system time',
        'unit'       : 'microseconds'
    },
    'cpu.user'                                                  : {
        'type'       : MetricType.COUNTER,
        'description': 'The cumulated CPU user time',
        'unit'       : 'microseconds'
    },
    'disk.bytes_free'                                           : {
        'type'       : MetricType.GAUGE,
        'description': 'The bytes free on the persistence path',
        'unit'       : 'bytes'
    },
    'disk.bytes_total'                                          : {
        'type'       : MetricType.GAUGE,
        'description': 'The bytes total on the persistence path',
        'unit'       : 'bytes'
    },
    'disk.path'                                                 : {
        'type'       : MetricType.INFO,
        'description': 'The persistence path',
        'unit'       : None
    },
    'engine_build_date'                                         : {
        'type'       : MetricType.INFO,
        'description': 'The QuasarDB engine build date',
        'unit'       : None
    },
    'engine_version'                                            : {
        'type'       : MetricType.INFO,
        'description': 'The QuasarDB engine version',
        'unit'       : None
    },
    'hardware_concurrency'                                      : {
        'type'       : MetricType.GAUGE,
        'description': 'The detected concurrent number of hardware threads supported on the system',
        'unit'       : 'count'
    },
    'memory.bytes_resident_size'                                : {
        'type'       : MetricType.GAUGE,
        'description': 'The computed amount of RAM used for data by QuasarDB',
        'unit'       : 'bytes'
    },
    'memory.physmem.bytes_total'                                : {
        'type'       : MetricType.GAUGE,
        'description': 'Physical RAM free bytes count',
        'unit'       : 'bytes'
    },
    'memory.physmem.bytes_used'                                 : {
        'type'       : MetricType.GAUGE,
        'description': 'Physical RAM used bytes count',
        'unit'       : 'bytes'
    },
    'memory.resident_count'                                     : {
        'type'       : MetricType.GAUGE,
        'description': 'The number of entries in RAM',
        'unit'       : 'count'
    },
    'memory.vm.bytes_total'                                     : {
        'type'       : MetricType.GAUGE,
        'description': 'Virtual memory free bytes count',
        'unit'       : 'bytes'
    },
    'memory.vm.bytes_used'                                      : {
        'type'       : MetricType.GAUGE,
        'description': 'Virtual memory used bytes count',
        'unit'       : 'bytes'
    },
    'network.current_users_count'                               : {
        'type'       : MetricType.GAUGE,
        'description': 'The current users count',
        'unit'       : 'count'
    },
    'network.sessions.available_count'                          : {
        'type'       : MetricType.GAUGE,
        'description': 'The current number of available sessions',
        'unit'       : 'count'
    },
    'network.sessions.max_count'                                : {
        'type'       : MetricType.GAUGE,
        'description': 'The configured maximum number of sessions',
        'unit'       : 'count'
    },
    'network.sessions.unavailable_count'                        : {
        'type'       : MetricType.GAUGE,
        'description': 'The current number of used sessions',
        'unit'       : 'count'
    },
    'node_id'                                                   : {
        'type'       : MetricType.INFO,
        'description': 'A string representing the node id',
        'unit'       : None
    },
    'operating_system'                                          : {
        'type'       : MetricType.INFO,
        'description': 'A string representing the operating system',
        'unit'       : None
    },
    'partitions_count'                                          : {
        'type'       : MetricType.GAUGE,
        'description': 'The number of partitions',
        'unit'       : 'count'
    },
    'perf.blob.update.content_writing.total_ns'                 : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.blob.update.deserialization.total_ns'                 : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.blob.update.entry_trimming.total_ns'                  : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.blob.update.entry_writing.total_ns'                   : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.blob.update.processing.total_ns'                      : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get.content_reading.total_ns'                  : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get.deserialization.total_ns'                  : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get.processing.total_ns'                       : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_by_affix.affix_search.total_ns'            : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_by_affix.deserialization.total_ns'         : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_by_affix.processing.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_metadata.deserialization.total_ns'         : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_metadata.processing.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_range.deserialization.total_ns'            : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_range.processing.total_ns'                 : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_versions.content_reading.total_ns': {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_versions.deserialization.total_ns': {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.get_versions.processing.total_ns': {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.set_transaction_state.content_reading.total_ns': {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.set_transaction_state.deserialization.total_ns': {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.set_transaction_state.entry_trimming.total_ns' : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.set_transaction_state.entry_writing.total_ns'  : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.common.set_transaction_state.processing.total_ns'     : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.control.system.deserialization.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.control.system.processing.total_ns'                   : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.integer.update.content_writing.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.integer.update.deserialization.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.integer.update.entry_trimming.total_ns'               : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.integer.update.entry_writing.total_ns'                : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.integer.update.processing.total_ns'                   : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.placeholder.put.deserialization.total_ns'             : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.placeholder.put.entry_writing.total_ns'               : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.placeholder.put.processing.total_ns'                  : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.tag.leaf_insert.deserialization.total_ns'             : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.tag.leaf_insert.entry_writing.total_ns'               : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.tag.leaf_insert.processing.total_ns'                  : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.aggregate_table.affix_search.total_ns'             : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.aggregate_table.content_reading.total_ns'          : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.aggregate_table.deserialization.total_ns'          : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.aggregate_table.directory_reading.total_ns'        : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.aggregate_table.processing.total_ns'               : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.aggregate_table.serialization.total_ns'            : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.blob_insert.content_reading.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.blob_insert.content_writing.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.blob_insert.deserialization.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.blob_insert.directory_writing.total_ns'            : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.blob_insert.entry_trimming.total_ns'               : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.blob_insert.entry_writing.total_ns'                : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.blob_insert.processing.total_ns'                   : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.blob_insert.ts_bucket_updating.total_ns'           : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.create_root.content_writing.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.create_root.deserialization.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.create_root.entry_writing.total_ns'                : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.create_root.processing.total_ns'                   : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.double_aggregate.affix_search.total_ns'            : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.double_aggregate.content_reading.total_ns'         : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.double_aggregate.deserialization.total_ns'         : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.double_aggregate.directory_reading.total_ns'       : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.double_aggregate.processing.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.double_aggregate.serialization.total_ns'           : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_column_info.content_reading.total_ns'          : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_column_info.deserialization.total_ns'          : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_column_info.processing.total_ns'               : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_columns.content_reading.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_columns.deserialization.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_columns.processing.total_ns'                   : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_range.affix_search.total_ns'                   : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_range.content_reading.total_ns'                : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_range.deserialization.total_ns'                : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_range.directory_reading.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_range.processing.total_ns'                     : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.get_range.serialization.total_ns'                  : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.int64_aggregate.affix_search.total_ns'             : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.int64_aggregate.content_reading.total_ns'          : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.int64_aggregate.deserialization.total_ns'          : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.int64_aggregate.directory_reading.total_ns'        : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.int64_aggregate.processing.total_ns'               : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.int64_aggregate.serialization.total_ns'            : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.table_insert.content_reading.total_ns'             : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.table_insert.content_writing.total_ns'             : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.table_insert.deserialization.total_ns'             : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.table_insert.directory_writing.total_ns'           : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.table_insert.entry_trimming.total_ns'              : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.table_insert.entry_writing.total_ns'               : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'perf.ts.table_insert.processing.total_ns'                  : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'microseconds'
    },
    'persistence.bytes_capacity'                                : {
        'type'       : MetricType.GAUGE,
        'description': 'The persistence layer storage capacity, in bytes. May be 0 if the value is unknown',
        'unit'       : 'bytes'
    },
    'persistence.bytes_read'                                    : {
        'type'       : MetricType.COUNTER,
        'description': 'The cumulated number of bytes read',
        'unit'       : 'bytes'
    },
    'persistence.bytes_utilized'                                : {
        'type'       : MetricType.GAUGE,
        'description': 'How many bytes are currently used in the persistence layer',
        'unit'       : 'bytes'
    },
    'persistence.bytes_written'                                 : {
        'type'       : MetricType.COUNTER,
        'description': 'The cumulated number of bytes written',
        'unit'       : 'bytes'
    },
    'persistence.entries_count'                                 : {
        'type'       : MetricType.GAUGE,
        'description': 'The current number of entries in the persistence layer',
        'unit'       : 'count'
    },
    'requests.bytes_out'                                        : {
        'type'       : MetricType.COUNTER,
        'description': 'The cumulated number of bytes sent by the server',
        'unit'       : 'bytes'
    },
    'requests.errors_count'                                     : {
        'type'       : MetricType.COUNTER,
        'description': '',
        'unit'       : 'count'
    },
    'requests.successes_count'                                  : {
        'type'       : MetricType.COUNTER,
        'description': 'The cumulated number of successful operations',
        'unit'       : 'count'
    },
    'requests.total_count'                                      : {
        'type'       : MetricType.COUNTER,
        'description': 'he cumulated number of requests',
        'unit'       : 'count'
    },
    'startup'                                                   : {
        'type'       : MetricType.COUNTER,
        'description': 'The startup timestamp',
        'unit'       : None
    }
}


def get_metrics_metadata(metric_key: str) -> dict:
    return METRICS_METADATA[metric_key]
