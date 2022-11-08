from datetime import timedelta


def str_to_timedelta(duration: str) -> timedelta:
    if duration.endswith("s"):
        return timedelta(seconds=int(duration[:-1]))

    if duration.endswith("m"):
        return timedelta(minutes=int(duration[:-1]))

    if duration.endswith("h"):
        return timedelta(hours=int(duration[:-1]))

    if duration.endswith("d"):
        return timedelta(days=int(duration[:-1]))

    raise Exception("not supported")
