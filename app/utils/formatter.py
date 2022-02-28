def format_records(raw_records):
    if not raw_records:
        return []
    return list(map(lambda x: dict(x), raw_records))
