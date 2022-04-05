from asyncpg import Record

def get_previous_id(raw_records: list[Record]) -> int:
    if not raw_records:
        return 0
    return max(map(lambda x: x['previous_id'], raw_records))


def get_col_values(raw_records: list[Record], col_name: str) -> list:
    return [x[col_name] for x in raw_records]

def prepare_search_query(search_query: str) -> str:
    return ' & '.join(search_query.split())
