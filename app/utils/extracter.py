def get_previous_id(raw_records):
    if not raw_records:
        return 0
    return max(map(lambda x: x['previous_id'], raw_records))


def get_col_values(raw_records, col_name):
    return [x[col_name] for x in raw_records]
