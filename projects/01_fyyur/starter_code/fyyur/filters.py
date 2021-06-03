import babel

from . import app


def format_datetime(value, format='medium'):
    dt_format = format
    if format == 'full':
        dt_format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        dt_format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(value, dt_format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime
