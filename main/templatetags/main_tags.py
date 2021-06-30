from django import template
import datetime

register = template.Library()


@register.filter
def split_timesince(self):
    duration = datetime.date.today() - self
    return duration.days


@register.filter
def calculate_fee(due):
    curr = datetime.date.today()
    late_fee = 0.5
    return "{:.2f}".format((curr-due).days*late_fee)


@register.filter
def check_date(due):
    curr = datetime.date.today()
    if curr > due:
        return 1
    elif curr < due:
        return -1
    else:
        return 0


@register.filter
def convert_to_days(self):
    curr = datetime.date.today()
    time_left = self - curr
    return time_left.days
