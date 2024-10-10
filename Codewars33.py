import datetime

def most_frequent_days(year):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    first_day_of_year = datetime.date(year, 1, 1).weekday()
    last_day_of_year = datetime.date(year, 12, 31).weekday()

    if datetime.date(year, 12, 31).timetuple().tm_yday == 365:
        return [days_of_week[first_day_of_year]]

    frequent_days = [days_of_week[first_day_of_year]]

    if last_day_of_year != first_day_of_year:
        next_day = (first_day_of_year + 1) % 7
        frequent_days.append(days_of_week[next_day])

    return sorted(frequent_days, key=lambda day: days_of_week.index(day))
