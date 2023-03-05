
def covert_to_seconds(time_str: str) -> int:
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds


