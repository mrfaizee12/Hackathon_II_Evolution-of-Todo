"""
Metrics collection for Reminder Service
"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server, generate_latest
from typing import Dict, Any
import time
import threading
from enum import Enum


class MetricLabels(Enum):
    """
    Common metric labels for the Reminder Service
    """
    METHOD = "method"
    PATH = "path"
    STATUS_CODE = "status_code"
    EVENT_TYPE = "event_type"
    OPERATION = "operation"
    NOTIFICATION_METHOD = "method"
    REMINDER_STATUS = "status"


# Define metrics
REQUEST_COUNT = Counter(
    'reminder_requests_total',
    'Total number of requests',
    [MetricLabels.METHOD.value, MetricLabels.PATH.value, MetricLabels.STATUS_CODE.value]
)

REQUEST_DURATION = Histogram(
    'reminder_request_duration_seconds',
    'Request duration in seconds',
    [MetricLabels.METHOD.value, MetricLabels.PATH.value]
)

EVENT_CONSUMED_COUNT = Counter(
    'reminder_events_consumed_total',
    'Total number of events consumed',
    [MetricLabels.EVENT_TYPE.value]
)

NOTIFICATIONS_SENT = Counter(
    'reminder_notifications_sent_total',
    'Total number of notifications sent',
    [MetricLabels.NOTIFICATION_METHOD.value, MetricLabels.REMINDER_STATUS.value]
)

REMINDER_OPERATIONS = Counter(
    'reminder_operations_total',
    'Total number of reminder operations',
    [MetricLabels.OPERATION.value]
)

ACTIVE_REMINDERS = Gauge(
    'reminder_active_reminders',
    'Number of active reminders'
)

NOTIFICATION_LATENCY = Histogram(
    'reminder_notification_latency_seconds',
    'Latency of notification delivery',
    [MetricLabels.NOTIFICATION_METHOD.value]
)


class MetricsCollector:
    """
    Metrics collector for the Reminder Service
    """
    
    def __init__(self, port: int = 8003):
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
    
    def record_notification_sent(self, method: str, status: str):
        """
        Record a notification being sent
        """
        NOTIFICATIONS_SENT.labels(
            method=method,
            status=status
        ).inc()
    
    def record_reminder_operation(self, operation: str):
        """
        Record a reminder operation
        """
        REMINDER_OPERATIONS.labels(
            operation=operation
        ).inc()
    
    def set_active_reminders(self, count: int):
        """
        Set the number of active reminders
        """
        ACTIVE_REMINDERS.set(count)
    
    def record_notification_latency(self, method: str, latency: float):
        """
        Record the latency of a notification
        """
        NOTIFICATION_LATENCY.labels(
            method=method
        ).observe(latency)
    
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


def record_notification_sent_metric(method: str, status: str):
    """
    Record a notification sent metric
    """
    metrics_collector.record_notification_sent(method, status)


def record_reminder_operation_metric(operation: str):
    """
    Record a reminder operation metric
    """
    metrics_collector.record_reminder_operation(operation)


def set_active_reminders_metric(count: int):
    """
    Set the active reminders gauge
    """
    metrics_collector.set_active_reminders(count)


def record_notification_latency_metric(method: str, latency: float):
    """
    Record the notification latency
    """
    metrics_collector.record_notification_latency(method, latency)