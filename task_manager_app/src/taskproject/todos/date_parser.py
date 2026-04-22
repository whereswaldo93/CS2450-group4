"""
Singleton date-parsing helper for the todos application.

The ``datetime.strptime(raw, "%Y-%m-%d").date()`` expression (along with its
try/except boilerplate) was duplicated in both ``add_task`` and ``edit_task``.
``DateParser`` centralises that logic so it lives in exactly one place.
"""

from __future__ import annotations

import re
from datetime import date, datetime


_DATE_FMT = "%Y-%m-%d"
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class DateParser:
    """Singleton for parsing and validating task due-date strings.

    Usage::

        parser = DateParser()
        due_date, error = parser.parse("2025-12-31")
    """

    _instance: "DateParser | None" = None

    def __new__(cls) -> "DateParser":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def parse(self, raw: str | None) -> tuple[date | None, str | None]:
        """Parse a date string into a :class:`datetime.date`.

        Args:
            raw: A string in ``YYYY-MM-DD`` format, or ``None`` / empty string.

        Returns:
            A ``(date, error_message)`` tuple.  Exactly one of the two values
            will be ``None``:

            * ``(date_obj, None)``  — parsing succeeded.
            * ``(None, error_str)`` — the string was malformed.
            * ``(None, None)``      — ``raw`` was empty/None; no date provided.
        """
        if not raw:
            return None, None

        if not _DATE_RE.match(raw):
            return None, "Invalid date format. Use YYYY-MM-DD."

        try:
            return datetime.strptime(raw, _DATE_FMT).date(), None
        except ValueError:
            return None, "Invalid date format. Use YYYY-MM-DD."
