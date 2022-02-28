def get_previous_id(raw_records):
    if not raw_records:
        return 0
    return max(map(lambda x: x['previous_id'], raw_records))
