from datetime import date, datetime, timedelta

"""A lot of this is reformatting date objects and time strings..."""


class Session:
    """Blueprints for session objects which hold, most crucially, the experiment name, & start day & time."""

    def __init__(self, name, doy_start, ut_start, duration):
        self.name = name
        self.doy = int(doy_start)
        self.ut = ut_start
        self.duration = int(duration)

    def get_week_num(self):
        """Get the number of the week of the year."""
        return get_week_from_date_string(self.get_start_date_dmy())

    def get_start_date_dmy(self):
        """Get the date of the start of the session in dd-mm-yyyy form"""
        day_num = self.doy
        year = date.today().year
        date_dmy = datetime(year, 1, 1) + timedelta(day_num - 1)
        d = date_dmy.strftime('%d-%m-%Y')
        return d

    def get_lt_finish(self):
        """Get the local time finish for the experiment."""
        time_zone_shift_value = 2  # hours
        tl = self.ut.split(":")
        start_hour_ut = int(tl[0])
        finish_hour_ut = start_hour_ut + self.duration
        finish_hour_lt = finish_hour_ut + time_zone_shift_value
        finish_hour_lt = finish_hour_lt % 24
        finish_lt = f"{finish_hour_lt}:{tl[1]}"
        return finish_lt

    def get_start_date(self):
        """Get the date of the start of the session in dd-mm form."""
        day_num = self.doy
        year = date.today().year
        date_dmy = datetime(year, 1, 1) + timedelta(day_num - 1)
        d = date_dmy.strftime('%d-%m')
        return d

    def get_name_of_start_day(self):
        """Get the name of the day on which the session begins."""
        day_num = self.doy
        year = date.today().year
        d = datetime(year, 1, 1) + timedelta(day_num - 1)
        return d.strftime("%A")

    def get_lt_shift_start(self):
        """Get local time start of the observer's shift (1 hour before session starts)."""
        time_zone_shift_value = 2  # hours
        prep_time = 1
        tl = self.ut.split(":")
        h = int(tl[0]) + time_zone_shift_value - prep_time
        m = int(tl[1])
        h = h % 24
        lt = f"{h:02}:{m:02}"
        return lt

    def get_lt_shift_end(self):
        """Get local time end of the observer's shift (0.5 hours after session ends)."""
        exp_lt_end = self.get_lt_finish()
        tl = exp_lt_end.split(":")
        m_exp = int(tl[1])
        m_shift = m_exp + 30
        m = m_shift % 60
        h_shift = int(tl[0])
        h = h_shift + (m_shift // 60)
        lt = f"{h:02}:{m:02}"
        return lt

    def get_lt_start(self):
        """Get session start in local time."""
        time_zone_shift_value = 2  # hours
        tl = self.ut.split(":")
        h = int(tl[0]) + time_zone_shift_value
        m = int(tl[1])
        h = h % 24
        lt = f"{h:02}:{m:02}"
        return lt

    def get_finish_doy(self):
        """Get day of year for which the experiment ends."""
        start_hour = int(self.ut.split(":")[0])
        finish_hour = start_hour + self.duration
        doy_finish = self.doy + (finish_hour // 24)
        return doy_finish


# Related functions:


def get_week_from_date_string(date_string):
    return datetime.strptime(date_string, "%d-%m-%Y").date().isocalendar().week
