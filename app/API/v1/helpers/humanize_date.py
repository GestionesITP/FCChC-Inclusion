import humanize
from datetime import datetime, timezone


def min_unit(diff):
    if diff < 10:
        return "seconds"
    if diff < 360:
        return "minutes"
    if diff < 720:
        return "hours"
    return "days"


def get_time_ago(past_date):

    humanize.i18n.activate("es_ES")
    now = datetime.now(timezone.utc)
    diff = past_date
    second_diff = diff.seconds
    delta = humanize.precisedelta(
        past_date - now, minimum_unit=min_unit(second_diff), format="%d")
    return "Hace %s" % delta
