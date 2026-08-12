import uuid
import logging
from flask import request, g, has_request_context

def register_correlation_id(app):
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        if has_request_context():
            record.correlation_id = getattr(g, "correlation_id", "no-correlation-id")
        else:
            record.correlation_id = "no-request-context"
        return record

    logging.setLogRecordFactory(record_factory)

    @app.before_request
    def set_correlation_id():
        incoming_id = request.headers.get("X-Correlation-ID")
        g.correlation_id = incoming_id or str(uuid.uuid4())

    @app.after_request
    def add_correlation_id_header(response):
        response.headers["X-Correlation-ID"] = getattr(g, "correlation_id", "unknown")
        return response