from datetime import datetime


def close_object(target, sum):
    target.invested_amount += sum
    target.fully_invested = True
    target.close_date = datetime.now()
