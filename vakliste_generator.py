from openpyxl import Workbook
from openpyxl.styles import Border, Side
from openpyxl.styles import Color, Fill, PatternFill, Font, Alignment
#import datetime
from datetime import date, datetime, timedelta
import itertools
import sys
###

def generate_workbook():
    """Main function to generate the Vakliste workbook."""

    # initialise:
    workbook = Workbook()
    sheet = workbook.active

    # fill out prelimaries:

    sheet.column_dimensions['A'].width = 12.5

    ###

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
                sheet[box] = "DATE"

        if r == 5:
                sheet[box] = "DAY"

        if r == 6:
                sheet[box] = "D.O.Y."

        if r == 7:
            sheet[box] = "START (LT)"

        if r > 7:
            sheet[box] = " "

    #

    # pretend load in file with form: name, doy, ut, duration
    # eg. r41159, 165, 18:30, 24
    # then create session object:
   # sess_test = Session('r41159', 165, '18:30', 24)

   # print(sess_test.get_start_date())

    ###
  #  d = datetime.strptime(sess_test.get_start_date(), "%d-%m-%Y").date()

  #  print(d.isocalendar().weekday)
  #  print(d.isocalendar().week)
  #  print(d.strftime("%A"))    # name of day

  #  print(sess_test.get_lt_start())

  #  print(sess_test.get_finish_doy())
   #
   # print(sess_test.get_lt_finish())
    print("******************")

    ##
    observers_input = ["AB", "CD", "EF", "GH"]
    observers = []

    colour_list = ["00FF0000", "00800080", "003366FF", "00008080", "0000FFFF", "009999FF"]
    i = 0
    for who in observers_input:
        color = colour_list[i]
        i += 1
        obs = Observer(who, color)
        observers.append(obs)

    # How to distribute the observers equally between the shifts?

    ###

    exp_list = get_exp_list_from_file("exps.txt")



    exp_list = sorted(exp_list, key=lambda exp: exp.doy)

    for exp in exp_list:
        print(exp.name, exp.doy)

    print(len(exp_list))

 #   observers_name_list = [o.name for o in observers]


    schedule = distribute_shifts(observers, exp_list)
    reverse_lookup = create_reverse_lookup(schedule)


    ###

    for staff, shifts in schedule.items():
        print (staff.name, ": ", len(shifts))
    ###


    # inverted_schedule = {b: a for a, b in schedule.items()}   # cant invert 1 to many ???
    # print(inverted_schedule)


    print("***********************************************")

    print("EXP CODE, D.O.Y., DATE, NAME, START (UT), START (LT), WEEK #, ONDUTY")
    for exp in exp_list:
        #on_duty = {it for it in dict if exp.name in dict[it]}
        #on_duty = staff in schedule.items() if exp.name in schedule.items()

        on_duty = reverse_lookup.get(exp.name)

        print(exp.name, exp.doy, exp.get_start_date(), exp.get_name_of_start_day(), exp.ut, exp.get_lt_shift_start(), exp.get_week_num(), on_duty.name)

    print("***********************************************")

    ###


    my_red = '00FF0000'
    my_green = '0000FF00'
    my_red_fill = PatternFill(patternType='solid', fgColor=Color(my_red))




   # alpha = "ABCDEFGHIJKLNOPQRSTUVWXYZ"
    alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ", "KK", "LL", "MM", "NN", "OO", "PP", "QQ", "RR", "SS", "TT", "UU", "VV", "WW", "XX", "YY", "ZZ", "AAA"]
    i = 1
    j = 8
    k = 1

    for exp in exp_list:
        sheet[f"{alpha[i]}1"] = f"{exp.get_week_num()}"
        sheet[f"{alpha[i]}1"].fill = my_red_fill


        sheet[f"{alpha[i]}2"] = f"{exp.name}"
        sheet[f"{alpha[i]}2"].font = Font(color = my_red)


        sheet[f"{alpha[i]}4"] = f"{exp.get_start_date()}"
        sheet[f"{alpha[i]}4"].font = Font(color = my_green)

        sheet[f"{alpha[i]}5"] = f"{exp.get_name_of_start_day()}"
        sheet[f"{alpha[i]}5"].font = Font(color = my_green)
        sheet[f"{alpha[i]}5"].alignment = Alignment(shrinkToFit=False, horizontal='center')

        sheet[f"{alpha[i]}6"] = f"{exp.doy}"
        sheet[f"{alpha[i]}7"] = f"{exp.get_lt_start()}"

        duration = 24
        if duration >= 24:
            k = 2

        for l in range(k):
            j = j + l
            sheet[f"A{j}"] = (reverse_lookup.get(exp.name)).name
            sheet[f"A{j}"].font = Font(color = reverse_lookup.get(exp.name).colour)

            #

            if k == 1:
                sheet[f"{alpha[i]}{j}"] = f"{exp.get_lt_shift_start()}-{exp.get_lt_shift_end()}"
            elif k == 2:
                if l == 0:
                    sheet[f"{alpha[i]}{j}"] = f"{exp.get_lt_shift_start()}-08:00"
                elif l == 1:
                    sheet[f"{alpha[i]}{j}"] = f"08:00-{exp.get_lt_shift_end()}"
            sheet[f"{alpha[i]}{j}"].alignment = Alignment(shrinkToFit=True, horizontal='center')

           # sheet[f"{alpha[i]}{j}"] = "XXX"
        # sheet[f"{alpha[i]}{j}"].fill = PatternFill(patternType='solid', fgColor = reverse_lookup.get(exp.name).colour)
            sheet[f"{alpha[i]}{j}"].font = Font(color = reverse_lookup.get(exp.name).colour)
        #
        i += 1
        j += 1



    ### STYLE STUFF:

    set_border(sheet, 'A1:A7')

    ###

    # save the file
    workbook.save(filename="test.xlsx")


    ###



def set_border(ws, cell_range):
    thin = Side(border_style="thin", color="000000")
    for row in ws[cell_range]:
        for cell in row:
            cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)



def create_reverse_lookup(schedule):
    reverse_lookup = {}
    for staff, shifts in schedule.items():
        for shift in shifts:
            reverse_lookup[shift] = staff
    return reverse_lookup

def distribute_shifts(staff_list, shifts_list):

    schedule = {staff: [] for staff in staff_list}
    staff_cycle = itertools.cycle(staff_list)
    for shift in shifts_list:
        current_staff = next(staff_cycle)
        schedule[current_staff].append(shift.name)

    return schedule

def get_week_from_date_string(date_string):

    return datetime.strptime(date_string, "%d-%m-%Y").date().isocalendar().week

def get_exp_list_from_file(filename):

    exp_list = []
    file = open(filename,'r')
    lines = file.readlines()
    for l in lines:
        lc = l.split()
        exp = Session(lc[0],lc[1],lc[2],24)
        exp_list.append(exp)
    file.close()

    return exp_list

class Observer:

    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        return self.colour

class Session:

    def __init__(self, name, doy_start, ut_start, duration):
        self.name = name
        self.doy = int(doy_start)
        self.ut = ut_start
        self.duration = int(duration)

    def get_week_num(self):

        return get_week_from_date_string(self.get_start_date_dmy())

    def get_start_date_dmy(self):

        day_num = self.doy
        year = date.today().year
        date_dmy = datetime(year, 1, 1) + timedelta(day_num - 1)
        d = date_dmy.strftime('%d-%m-%Y')

        return d


    def get_lt_finish(self):

        time_zone_shift_value = 2 # hours

        tl = self.ut.split(":")
        start_hour_ut = int(tl[0])
        finish_hour_ut = start_hour_ut + self.duration
        finish_hour_lt = finish_hour_ut +  time_zone_shift_value
        finish_hour_lt = finish_hour_lt % 24
        finish_lt = f"{finish_hour_lt}:{tl[1]}"
        return finish_lt


    def get_start_date(self):

        day_num = self.doy
        year = date.today().year
        date_dmy = datetime(year, 1, 1) + timedelta(day_num - 1)
        d = date_dmy.strftime('%d-%m')

        return d

    def get_name_of_start_day(self):

        day_num = self.doy
        year = date.today().year
        d = datetime(year, 1, 1) + timedelta(day_num - 1)
        return d.strftime("%A")

    def get_lt_shift_start(self):

        time_zone_shift_value = 2 # hours
        prep_time = 1
        tl = self.ut.split(":")
        h = int(tl[0]) + time_zone_shift_value - prep_time
        m = int(tl[1])
        h = h % 24
        lt = f"{h:02}:{m:02}"

        return lt


    def get_lt_shift_end(self):

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

        time_zone_shift_value = 2 # hours
        tl = self.ut.split(":")
        h = int(tl[0]) + time_zone_shift_value
        m = int(tl[1])
        h = h % 24
        lt = f"{h:02}:{m:02}"

        return lt




    def get_finish_doy(self):

        start_hour = int(self.ut.split(":")[0])
        finish_hour = start_hour + self.duration

        if finish_hour > 24:
            doy_finish = self.doy + 1
        elif finish_hour < 24:
            doy_finish = self.doy

        return doy_finish



if __name__ == '__main__':

    generate_workbook()

    # test stuff:
