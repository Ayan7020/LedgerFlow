from opentelemetry.sdk.trace import SpanProcessor,ReadableSpan
from opentelemetry.trace import StatusCode
import re

_TX_SPAN_RE = re.compile(
    r"^\s*(BEGIN|COMMIT|ROLLBACK)(\s+TRANSACTION)?\s*;?\s*$",
    re.IGNORECASE,
)

class FilteringSpanProcessor(SpanProcessor):
    """Drop noisy TX spans unless slow or errored. Forwards everything else."""

    def __init__(
            self,
            next_processor: SpanProcessor,
            *,
            keep_tx_slower_than_ms: float = 50.2
        ):
        self.__next = next_processor
        self._keep_tx_ns = int(keep_tx_slower_than_ms * 1_000_000)


    def on_start(self, span, parent_context=None) -> None:
        self.__next.on_start(span,parent_context=parent_context)


    def on_end(self, span: ReadableSpan) -> None:
        if self._should_drop(span):
            return
        self.__next.on_end(span)

    def shutdown(self) -> None:
        self.__next.shutdown()

    def _should_drop(self,span: ReadableSpan) -> bool:

        if not _TX_SPAN_RE.match(span.name or ""):
            return False

        if span.status.status_code == StatusCode.ERROR:
            return False

        if span.start_time is None or span.end_time is None:
            return True

        duration_ns = span.end_time - span.start_time
        return duration_ns < self._keep_tx_ns
        