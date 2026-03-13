from datetime import datetime

def check_time_conflict(new_start, new_end, existing_times):
    """
    Checks if a newly registered event conflicts with previously registered events (M5 Must Requirement).

    Parameters:
    new_start (datetime): The start time of the new event.
    new_end (datetime): The end time of the new event.
    existing_times (list of tuples): A list of time pairs for already registered events,

    Returns:
    bool: True if a conflict exists, False otherwise.
    """
    for exist_start, exist_end in existing_times:
        # An overlap occurs if the "latest start" is earlier than the "earliest end."
        latest_start = max(new_start, exist_start)
        earliest_end = min(new_end, exist_end)

        if latest_start < earliest_end:
            return True

    return False