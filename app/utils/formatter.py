from asyncpg import Record

def format_records(raw_records: Record) -> list[dict]:
    if not raw_records:
        return []
    return list(map(dict, raw_records))
