from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class EquipmentHistoryEvent:
    """
    Internal representation of a machine history event.

    This is a domain model used by the history service to aggregate
    events from multiple sources before converting them into API
    responses.
    """

    type: str
    title: str
    occurred_at: datetime
    actor: str | None

    payload: dict[str, Any]