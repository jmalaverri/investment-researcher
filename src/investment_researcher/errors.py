class FundDataError(Exception):
    """Base for fund-data retrieval failures."""


class TickerNotFound(FundDataError):
    """The ticker is unknown. Expected and recoverable — the orchestrator can degrade."""


class FundDataUnavailable(FundDataError):
    """Transient: network failure, rate limit, or provider error. Not the caller's fault."""
