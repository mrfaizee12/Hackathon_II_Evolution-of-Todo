"""
Metrics collection for Recurring Engine
"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server, generate_latest
from typing import Dict, Any
import time
import threading
from enum import Enum


class MetricLabels(Enum):
    """
    Common metric labels for the Recurring Engine
    """
    METHOD = "method"
    PATH = "path"
    STATUS_CODE = "status_code"
    EVENT_TYPE = "event_type"
    OPERATION = "operation"
    SCHEDULE_TYPE = "schedule_type"


# Define metrics
REQUEST_COUNT = Counter(
    'recurring_requests_total',
    'Total number of requests',
    [MetricLabels.METHOD.value, MetricLabels.PATH.value, MetricLabels.STATUS_CODE.value]
)

REQUEST_DURATION = Histogram(
    'recurring_request_duration_seconds',
    'Request duration in seconds',
    [MetricLabels.METHOD.value, MetricLabels.PATH.value]
)

EVENT_CONSUMED_COUNT = Counter(
    'recurring_events_consumed_total',
    'Total number of events consumed',
    [MetricLabels.EVENT_TYPE.value]
)

SCHEDULE_OPERATIONS = Counter(
    'recurring_schedule_operations_total',
    'Total number of schedule operations',
    [MetricLabels.OPERATION.value, MetricLabels.SCHEDULE_TYPE.value]
)

ACTIVE_SCHEDULES = Gauge(
    'recurring_active_schedules',
    'Number of active schedules'
)

SCHEDULE_EXECUTION_TIME = Histogram(
    'recurring_schedule_execution_time_seconds',
    'Time taken to execute a schedule',
    [MetricLabels.SCHEDULE_TYPE.value]
)


class MetricsCollector:
    """
    Metrics collector for the Recurring Engine
    """
    
    def __init__(self, port: int = 8002):
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
    
    def record_event_consumed(self, event_type: str):
        """
        Record an event consumption
        """
        EVENT_CONSUMED_COUNT.labels(
            event_type=event_type
        ).inc()
    
    def record_schedule_operation(self, operation: str, schedule_type: str):
        """
        Record a schedule operation
        """
        SCHEDULE_OPERATIONS.labels(
            operation=operation,
            schedule_type=schedule_type
        ).inc()
    
    def set_active_schedules(self, count: int):
        """
        Set the number of active schedules
        """
        ACTIVE_SCHEDULES.set(count)
    
    def record_schedule_execution_time(self, schedule_type: str, execution_time: float):
        """
        Record the time taken to execute a schedule
        """
        SCHEDULE_EXECUTION_TIME.labels(
            schedule_type=schedule_type
        ).observe(execution_time)
    
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


def record_event_consumed_metric(event_type: str):
    """
    Record an event consumed metric
    """
    metrics_collector.record_event_consumed(event_type)


def record_schedule_operation_metric(operation: str, schedule_type: str):
    """
    Record a schedule operation metric
    """
    metrics_collector.record_schedule_operation(operation, schedule_type)


def set_active_schedules_metric(count: int):
    """
    Set the active schedules gauge
    """
    metrics_collector.set_active_schedules(count)


def record_schedule_execution_time_metric(schedule_type: str, execution_time: float):
    """
    Record the schedule execution time
    """
    metrics_collector.record_schedule_execution_time(schedule_type, execution_time)