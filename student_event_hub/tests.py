from django.test import TestCase
from datetime import datetime
from .services import check_time_conflict

class RegistrationConflictTests(TestCase):

    def test_no_conflict(self):
        """Scenario 1: No overlap between time slots.
        The registration should be allowed (Expected: False)."""
        existing = [
            (datetime(2026, 3, 20, 10, 0), datetime(2026, 3, 20, 12, 0))
        ]
        new_start = datetime(2026, 3, 20, 13, 0)
        new_end = datetime(2026, 3, 20, 15, 0)

        has_conflict = check_time_conflict(new_start, new_end, existing)
        self.assertFalse(has_conflict)

    def test_with_conflict_overlap(self):
        """Scenario 2: Partial overlap between time slots.
        The registration should be blocked (Expected: True)."""
        existing = [
            (datetime(2026, 3, 20, 10, 0), datetime(2026, 3, 20, 12, 0))
        ]
        new_start = datetime(2026, 3, 20, 11, 0)
        new_end = datetime(2026, 3, 20, 13, 0)

        has_conflict = check_time_conflict(new_start, new_end, existing)
        self.assertTrue(has_conflict)

    def test_with_conflict_exact_match(self):
        """Scenario 3: Exact match of time slots.
        The registration should be blocked (Expected: True)."""
        existing = [
            (datetime(2026, 3, 20, 10, 0), datetime(2026, 3, 20, 12, 0))
        ]
        new_start = datetime(2026, 3, 20, 10, 0)
        new_end = datetime(2026, 3, 20, 12, 0)

        has_conflict = check_time_conflict(new_start, new_end, existing)
        self.assertTrue(has_conflict)