def format_records(raw_records):
    if not raw_records:
        return []
    return list(map(dict, raw_records))
