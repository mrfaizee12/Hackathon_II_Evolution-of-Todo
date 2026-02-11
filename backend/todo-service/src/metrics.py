"""
Metrics collection for Todo Service
"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server, generate_latest
from typing import Dict, Any
import time
import threading
from enum import Enum


class MetricLabels(Enum):
    """
    Common metric labels for the Todo Service
    """
    METHOD = "method"
    PATH = "path"
    STATUS_CODE = "status_code"
    EVENT_TYPE = "event_type"
    OPERATION = "operation"


# Define metrics
REQUEST_COUNT = Counter(
    'todo_requests_total',
    'Total number of requests',
    [MetricLabels.METHOD.value, MetricLabels.PATH.value, MetricLabels.STATUS_CODE.value]
)

REQUEST_DURATION = Histogram(
    'todo_request_duration_seconds',
    'Request duration in seconds',
    [MetricLabels.METHOD.value, MetricLabels.PATH.value]
)

EVENT_PUBLISHED_COUNT = Counter(
    'todo_events_published_total',
    'Total number of events published',
    [MetricLabels.EVENT_TYPE.value]
)

TASK_OPERATIONS = Counter(
    'todo_task_operations_total',
    'Total number of task operations',
    [MetricLabels.OPERATION.value]
)

ACTIVE_TASKS = Gauge(
    'todo_active_tasks',
    'Number of active tasks'
)


class MetricsCollector:
    """
    Metrics collector for the Todo Service
    """
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.start_server()
    
    def start_server(self):
        """
        Start the metrics server in a separate thread
        """
        def run_metrics_server():
            start_http_server(self.port + 100)  # Use a different port for metrics
        
        thread = threading.Thread(target=run_metrics_server, daemon=True)
        thread.start()
    
    def record_request(self, method: str, path: str, status_code: int, duration: float):
        """
        Record an HTTP request
        """
        REQUEST_COUNT.labels(
            method=method,
            path=path,
            status_code=status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=method,
            path=path
        ).observe(duration)
    
    def record_event_published(self, event_type: str):
        """
        Record an event publication
        """
        EVENT_PUBLISHED_COUNT.labels(
            event_type=event_type
        ).inc()
    
    def record_task_operation(self, operation: str):
        """
        Record a task operation
        """
        TASK_OPERATIONS.labels(
            operation=operation
        ).inc()
    
    def set_active_tasks(self, count: int):
        """
        Set the number of active tasks
        """
        ACTIVE_TASKS.set(count)
    
    def get_metrics(self) -> str:
        """
        Get the current metrics in Prometheus format
        """
        return generate_latest().decode('utf-8')


# Global metrics collector instance
metrics_collector = MetricsCollector()


def record_request_metric(method: str, path: str, status_code: int, duration: float):
    """
    Record an HTTP request metric
    """
    metrics_collector.record_request(method, path, status_code, duration)


def record_event_published_metric(event_type: str):
    """
    Record an event published metric
    """
    metrics_collector.record_event_published(event_type)


def record_task_operation_metric(operation: str):
    """
    Record a task operation metric
    """
    metrics_collector.record_task_operation(operation)


def set_active_tasks_metric(count: int):
    """
    Set the active tasks gauge
    """
    metrics_collector.set_active_tasks(count)