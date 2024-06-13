from openpyxl import Workbook
#import datetime
from datetime import date, datetime, timedelta

###

def generate_workbook():
    """Main function to generate the Vakliste workbook."""

    # initialise:
    workbook = Workbook()
    sheet = workbook.active

    # fill out prelimaries:

    col = "A"
    max_rows = 20


    for r in range(max_rows):
        box = "A%s" % r

        if r == 1:
            sheet[box] = "WEEK"

        if r == 2:
             sheet[box] = "SESS."

        if r == 3:
            sheet[box] = "TELE."

        if r == 4:
                sheet[box] = "DAY"

        if r == 5:
            sheet[box] = "START (LT)"

        if r > 5:
            sheet[box] = " "

    #

    # pretend load in file with form: name, doy, ut, duration
    # eg. r41159, 165, 18:30, 24
    # then create session object:
    sess_test = Session('r41159', 165, '18:30', 24)

    print(sess_test.get_start_date())

    ###
    d = datetime.strptime(sess_test.get_start_date(), "%d-%m-%Y").date()

    print(d.isocalendar().weekday)
    print(d.isocalendar().week)
    print(d.strftime("%A"))

    print(sess_test.get_lt_start())

    print(sess_test.get_finish_doy())

    print(sess_test.get_lt_finish())

    ##
    observers = ["ab","cd","ef"]


    ###

    # save the file
    workbook.save(filename="test.xlsx")


class Session:

    def __init__(self, name, doy_start, ut_start, duration):
        self.name = name
        self.doy = doy_start
        self.ut = ut_start
        self.duration = duration

    def get_start_date(self):

        day_num = self.doy
        year = date.today().year
        date_dmy = datetime(year, 1, 1) + timedelta(day_num - 1)
        date_dm = date_dmy.strftime('%d-%m-%Y')

        return date_dm

    def get_lt_start(self):

        time_zone_shift_value = 2 # hours
        tl = self.ut.split(":")
        tl[0] = f"{int(tl[0]) + time_zone_shift_value}"
        lt = f"{tl[0]}:{tl[1]}"

        #need to mod 24....

        return lt


    def get_finish_doy(self):

        start_hour = int(self.ut.split(":")[0])
        finish_hour = start_hour + self.duration

        if finish_hour > 24:
            doy_finish = self.doy + 1
        elif finish_hour < 24:
            doy_finish = self.doy

        return doy_finish

    def get_lt_finish(self):

        time_zone_shift_value = 2 # hours

        tl = self.ut.split(":")
        start_hour_ut = int(tl[0])
        finish_hour_ut = start_hour_ut + self.duration
        finish_hour_lt = finish_hour_ut +  time_zone_shift_value
        if finish_hour_lt >= 24:
            finish_hour_lt = finish_hour_lt % 24
        finish_lt = f"{finish_hour_lt}:{tl[1]}"
        return finish_lt



if __name__ == '__main__':

    generate_workbook()

    # test stuff:
