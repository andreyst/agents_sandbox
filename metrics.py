from prometheus_client import start_http_server, Summary, Gauge, Histogram
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR
import random
import time
import sys

worker_id = int(sys.argv[2])

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
gauge = Gauge('test_gauge', 'Test gauge', ["worker_id"])
h = Histogram('test_hist', 'Description of histogram', ["worker_id"], buckets=[1,3,5,10])

REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
# Unlike process and platform_collector gc_collector registers itself as three different collectors that have no corresponding public named variable.
REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    gauge.labels(worker_id=str(worker_id)).set(random.randint(worker_id, worker_id))
    h.labels(worker_id=str(worker_id)).observe(random.randint(worker_id, worker_id))
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(int(sys.argv[1]))
    # Generate some requests.
    while True:
        process_request(random.random())