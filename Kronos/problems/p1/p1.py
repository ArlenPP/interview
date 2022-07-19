from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta, FR


def find_quarterly_month(month):
    m = [3, 6, 9, 12]
    if month % 3 == 0:
        return month
    else:
        return m[int(month/3)]


def find_last_fri(year, month):
    c = calendar.Calendar(firstweekday=calendar.MONDAY)
    monthcal = c.monthdatescalendar(year,month)
    last_friday = [day for week in monthcal for day in week if \
                    day.weekday() == calendar.FRIDAY and \
                    day.month == month][-1]
    return last_friday


def quarterly(cur_time):
    """ Return the expiry date in string format
    Args:
        cur_time(datetime): input datetime
    """
    t = cur_time
    # weekly contract
    this_fri = t + relativedelta(weekday=FR(+1))
    if t == this_fri: 
        weekly_contract = this_fri + relativedelta(weekday=FR(+2))
    else:
        weekly_contract = this_fri

    # biweekly contract
    biweekly_contract = weekly_contract + relativedelta(weekday=FR(+2))

    # quartely contract
    t = biweekly_contract
    q_month = find_quarterly_month(t.month)
    year = t.year
    if find_last_fri(year, q_month) == t.date():
        next_q = t + relativedelta(months=3)
        quartely_contract = find_last_fri(next_q.year, next_q.month)
    else:
        quartely_contract = find_last_fri(year, q_month)


    expiry = quartely_contract.strftime('%y%m%d')
    return expiry


if __name__ == '__main__':
    assert quarterly(datetime(2020, 1, 27)) == '200327'
    assert quarterly(datetime(2019, 11, 1)) == '191227'
    assert quarterly(datetime(2019, 12, 27)) == '200327'
    assert quarterly(datetime(2019, 12, 1)) == '191227'
    assert quarterly(datetime(2019, 12, 18)) == '200327'
