"""
 Auto-create a roster spreadsheet from a list of experiments and on-duty observers.
"""

from openpyxl import Workbook
from openpyxl.styles import Border, Side, Color, PatternFill, Font, Alignment
import itertools
from session import Session
from observer import Observer


def generate_workbook():
    """Main function to generate the Vakliste workbook/spreadsheet for presentation."""

    debug = True

    # initialise: #
    workbook = Workbook()
    sheet = workbook.active

    # fill out preliminaries: #
    # set width & height & that sorta stuff:
    sheet.column_dimensions['A'].width = 12.5

    # fill in the first column (integrate this later into a complete fill-out function)
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
    if debug:
        print("******************")

    # define colour and colour list:
    # name = color # compliment
    red = "00FF0000"  # cyan
    purple = "00800080"  # 008000
    blue = "003366FF"  # FFCC33
    teal = "00008080"  # 800000
    cyan = "0000FFFF"  # red
    lavender = "009999FF"  # FFFF99
    # need to think about what colours would actually look nice, these above are just place-holders

    # list of all colours we would like in the spreadsheet:
    colour_list = [red, purple, blue, teal, cyan, lavender]

    # mock data (probably load this in from config file in real implementation)
    observers_input = ["AB", "CD", "EF", "GH"]

    # create list of observer objects:
    obs_list = get_observer_list(observers_input, colour_list)

    # create list of experiment objects:
    exp_list = get_exp_list_from_file("exps.txt")

    # sort the list into ascending d.o.y. (not really necessary?)
    exp_list = sorted(exp_list, key=lambda x: x.doy)

    if debug:
        for exp in exp_list:
            print(exp.name, exp.doy)
        print("******************")
        print(len(exp_list))

    # distribute the experiments equally between the observers:
    schedule = distribute_shifts(obs_list, exp_list)
    # flip the dictionary so that given an experiment, can get an observer
    reverse_lookup = create_reverse_lookup(schedule)

    if debug:
        print("number of shifts per person:")
        for staff, shifts in schedule.items():
            print(staff.name, ": ", len(shifts))
        print("******************")

    if debug:
        print("******************")
        print("")
        print("EXP, D.O.Y., DATE, NAME, START (UT), START (LT), WEEK #, ON-DUTY")
        for exp in exp_list:
            on_duty = reverse_lookup.get(exp.name)
            print(exp.name, exp.doy, exp.get_start_date(), exp.get_name_of_start_day(), exp.ut,
                  exp.get_lt_shift_start(),
                  exp.get_week_num(), on_duty.name)
        print("******************")
    #
    my_red_fill = PatternFill(patternType='solid', fgColor=Color(red))
    alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z", "AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II", "JJ", "KK", "LL", "MM",
             "NN", "OO", "PP", "QQ", "RR", "SS", "TT", "UU", "VV", "WW", "XX", "YY", "ZZ", "AAA"]

    #########################################################################################

    # configure start points
    i = 1
    j = 8
    # start filling out the heard of the spreadsheet
    for exp in exp_list:
        #
        sheet[f"{alpha[i]}1"] = f"{exp.get_week_num()}"
        sheet[f"{alpha[i]}1"].fill = my_red_fill
        #
        sheet[f"{alpha[i]}2"] = f"{exp.name}"
        sheet[f"{alpha[i]}2"].font = Font(color=red)
        #
        sheet[f"{alpha[i]}4"] = f"{exp.get_start_date()}"
        sheet[f"{alpha[i]}4"].font = Font(color=teal)
        #
        sheet[f"{alpha[i]}5"] = f"{exp.get_name_of_start_day()}"
        sheet[f"{alpha[i]}5"].font = Font(color=teal)
        sheet[f"{alpha[i]}5"].alignment = Alignment(shrinkToFit=False, horizontal='center')
        #
        sheet[f"{alpha[i]}6"] = f"{exp.doy}"
        sheet[f"{alpha[i]}7"] = f"{exp.get_lt_start()}"

        # place holder:
        duration = 24
        # check if session overflows to following day
        k = 1 + (duration // 24)
        for l in range(k):
            j = j + l
            sheet[f"A{j}"] = (reverse_lookup.get(exp.name)).name
            sheet[f"A{j}"].font = Font(color=reverse_lookup.get(exp.name).colour)
            # if no overflow
            if k == 1:
                sheet[f"{alpha[i]}{j}"] = f"{exp.get_lt_shift_start()}-{exp.get_lt_shift_end()}"
            # if overflows
            elif k == 2:
                if l == 0:
                    sheet[f"{alpha[i]}{j}"] = f"{exp.get_lt_shift_start()}-08:00"
                elif l == 1:
                    sheet[f"{alpha[i]}{j}"] = f"08:00-{exp.get_lt_shift_end()}"

            sheet[f"{alpha[i]}{j}"].alignment = Alignment(shrinkToFit=True, horizontal='center')
            sheet[f"{alpha[i]}{j}"].font = Font(color=reverse_lookup.get(exp.name).colour)
        #
        i += 1
        j += 1
    # style the spreadsheet
    set_border(sheet, 'A1:A7')

    ###
    # save the file
    workbook.save(filename="test.xlsx")

    #########################################################################################


def set_border(ws, cell_range):
    """Give the cell a border."""
    thin = Side(border_style="thin", color="000000")
    for row in ws[cell_range]:
        for cell in row:
            cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)


def create_reverse_lookup(schedule):
    """Get experiment given who is on duty."""
    reverse_lookup = {}
    for staff, shifts in schedule.items():
        for shift in shifts:
            reverse_lookup[shift] = staff
    return reverse_lookup


def distribute_shifts(staff_list, shifts_list):
    """Associate an experiment with an on-duty observer."""
    schedule = {staff: [] for staff in staff_list}
    staff_cycle = itertools.cycle(staff_list)
    for shift in shifts_list:
        current_staff = next(staff_cycle)
        schedule[current_staff].append(shift.name)
    return schedule


def get_observer_list(observers_input, colour_list):
    """Create list of observer objects."""
    observers = []
    i = 0
    for who in observers_input:
        color = colour_list[i]
        i += 1
        obs = Observer(who, color)
        observers.append(obs)
    return observers


def get_exp_list_from_file(filename):
    """Create list of experiment objects."""
    exp_list = []
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        lc = line.split()
        exp = Session(lc[0], lc[1], lc[2], 24)
        exp_list.append(exp)
    file.close()
    return exp_list


if __name__ == '__main__':
    # parse inputs (month?)
    # create object lists
    # create schedule
    # create workbook (passing in object lists and schedule)
    generate_workbook()
