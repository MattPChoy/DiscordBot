def format_seconds_to_hms(seconds: float) -> str:
    h, remainder = divmod(int(seconds), 3600)
    m, s = divmod(remainder, 60)
    return f"{h:02d}h{m:02d}m{s:02d}s"