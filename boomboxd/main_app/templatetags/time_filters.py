from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def ms_to_mins(milliseconds):
    """
    Converts a value in milliseconds to a formatted string "M:SS" or "MM:SS".
    """
    if milliseconds is None:
        return ""

    # Create a timedelta object
    duration = timedelta(milliseconds=milliseconds)
    total_seconds = int(duration.total_seconds())

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    # Format as "M:SS" or "MM:SS"
    return f"{minutes}:{seconds:02d}"
