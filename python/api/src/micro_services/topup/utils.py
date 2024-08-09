import datetime


def get_current_month_start_end():
    now = datetime.datetime.utcnow()

    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    next_month = now.replace(day=1) + datetime.timedelta(days=31)
    end_of_month = next_month.replace(day=1) - datetime.timedelta(days=1)
    end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=999999)

    return start_of_month.timestamp() * 1000, end_of_month.timestamp() * 1000