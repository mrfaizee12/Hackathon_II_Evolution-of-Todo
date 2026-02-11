"""
Metrics collection for Chatbot Service
"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server, generate_latest
from typing import Dict, Any
import time
import threading
from enum import Enum


class MetricLabels(Enum):
    """
    Common metric labels for the Chatbot Service
    """
    METHOD = "method"
    PATH = "path"
    STATUS_CODE = "status_code"
    EVENT_TYPE = "event_type"
    OPERATION = "operation"
    INTENT_TYPE = "intent"
    ACTION_TYPE = "action"
    USER_ID = "user_id"


# Define metrics
REQUEST_COUNT = Counter(
    'chatbot_requests_total',
    'Total number of requests',
    [MetricLabels.METHOD.value, MetricLabels.PATH.value, MetricLabels.STATUS_CODE.value]
)

REQUEST_DURATION = Histogram(
    'chatbot_request_duration_seconds',
    'Request duration in seconds',
    [MetricLabels.METHOD.value, MetricLabels.PATH.value]
)

MESSAGE_PROCESSED = Counter(
    'chatbot_messages_processed_total',
    'Total number of messages processed',
    [MetricLabels.INTENT_TYPE.value]
)

EVENT_CONSUMED_COUNT = Counter(
    'chatbot_events_consumed_total',
    'Total number of events consumed',
    [MetricLabels.EVENT_TYPE.value]
)

ACTIONS_PERFORMED = Counter(
    'chatbot_actions_performed_total',
    'Total number of actions performed',
    [MetricLabels.ACTION_TYPE.value]
)

ACTIVE_SESSIONS = Gauge(
    'chatbot_active_sessions',
    'Number of active chat sessions'
)

INTENT_RECOGNITION_LATENCY = Histogram(
    'chatbot_intent_recognition_latency_seconds',
    'Latency of intent recognition',
    [MetricLabels.INTENT_TYPE.value]
)

MESSAGE_PROCESSING_TIME = Histogram(
    'chatbot_message_processing_time_seconds',
    'Time taken to process a message',
    [MetricLabels.INTENT_TYPE.value]
)


class MetricsCollector:
    """
    Metrics collector for the Chatbot Service
    """
    
    def __init__(self, port: int = 8004):
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
    
    def record_message_processed(self, intent_type: str, processing_time: float):
        """
        Record a message being processed
        """
        MESSAGE_PROCESSED.labels(
            intent_type=intent_type
        ).inc()
        
        MESSAGE_PROCESSING_TIME.labels(
            intent_type=intent_type
        ).observe(processing_time)
    
    def record_event_consumed(self, event_type: str):
        """
        Record an event consumption
        """
        EVENT_CONSUMED_COUNT.labels(
            event_type=event_type
        ).inc()
    
    def record_action_performed(self, action_type: str):
        """
        Record an action being performed
        """
        ACTIONS_PERFORMED.labels(
            action_type=action_type
        ).inc()
    
    def set_active_sessions(self, count: int):
        """
        Set the number of active sessions
        """
        ACTIVE_SESSIONS.set(count)
    
    def record_intent_recognition_latency(self, intent_type: str, latency: float):
        """
        Record the latency of intent recognition
        """
        INTENT_RECOGNITION_LATENCY.labels(
            intent_type=intent_type
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


def record_message_processed_metric(intent_type: str, processing_time: float):
    """
    Record a message processed metric
    """
    metrics_collector.record_message_processed(intent_type, processing_time)


def record_event_consumed_metric(event_type: str):
    """
    Record an event consumed metric
    """
    metrics_collector.record_event_consumed(event_type)


def record_action_performed_metric(action_type: str):
    """
    Record an action performed metric
    """
    metrics_collector.record_action_performed(action_type)


def set_active_sessions_metric(count: int):
    """
    Set the active sessions gauge
    """
    metrics_collector.set_active_sessions(count)


def record_intent_recognition_latency_metric(intent_type: str, latency: float):
    """
    Record the intent recognition latency
    """
    metrics_collector.record_intent_recognition_latency(intent_type, latency)