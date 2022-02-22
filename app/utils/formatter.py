def format_records(raw_records):
    if not raw_records:
        return []
    return list(map(lambda x: dict(x), raw_records))


def format_record(raw_record):
    return dict(raw_record)

def get_col_values(raw_records, col_name):
    res = list()
    for i in raw_records:
        res.append(i[col_name])
    return res
