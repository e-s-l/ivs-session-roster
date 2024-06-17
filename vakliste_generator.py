"""
 Auto-create a roster spreadws from a list of experiments and on-duty observers.
"""

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side, Color, PatternFill, Font, Alignment
import itertools
from session import Session
from observer import Observer


def generate_workbook():
    """Main function to generate the Vakliste workbook/spreadws for presentation."""

    debug = True

    # initialise: #
    wb = Workbook()
    ws = wb.active

    #########################################################################################


    # define colour and colour list:
    # name = color # compliment
    red = "00FF0000"  # cyan
    purple = "00800080"  # 008000
    blue = "003366FF"  # FFCC33
    teal = "00008080"  # 800000
    cyan = "0000FFFF"  # red
    lavender = "009999FF"  # FFFF99
    # need to think about what colours would actually look nice, these above are just place-holders

    # list of all colours we would like in the spreadws:
    colour_list = [red, purple, blue, teal, cyan, lavender]

    #########################################################################################

    # mock data (probably load this in from config file in real implementation)
    observers_input = ["AB", "CD", "EF", "GH"]

    # create list of observer objects:
    obs_list = get_observer_list(observers_input, colour_list)

    # create list of experiment objects:
    exp_list = get_exp_list_from_file("experiments_nn_ns.txt")

    # sort the list into ascending d.o.y. (not really necessary?)
    exp_list = sorted(exp_list, key=lambda x: x.doy)

    if debug:
        print("------------------------------------------------------")
        print(f"Number of Experiments this month: {len(exp_list)}")

    # distribute the experiments equally between the observers:
    schedule = distribute_shifts(obs_list, exp_list)
    # flip the dictionary so that given an experiment, can get an observer
    reverse_lookup = create_reverse_lookup(schedule)

    if debug:
        print("Number of shifts per person on-duty:")
        for staff, shifts in schedule.items():
            print(staff.name, ": ", len(shifts))
        print("------------------------------------------------------")

    if debug:
        print("EXP, TELE, D.O.Y., DATE, NAME, START (UT), SHIFT (LT), DUR, WEEK #, ON-DUTY")
        for exp in exp_list:
            on_duty = reverse_lookup.get(exp.name)
            print(exp.name, exp.tele, exp.doy, exp.get_start_date(), exp.get_name_of_start_day(), exp.ut,
                  exp.get_lt_shift_start(), exp.duration,
                  exp.get_week_num(), on_duty.name)
        print("------------------------------------------------------")
    #

    #########################################################################################

    setup_worksheet(ws, exp_list, reverse_lookup, colour_list)

    #########################################################################################

    # save the file
    wb.save(filename="test.xlsx")

    #########################################################################################

def setup_worksheet(ws, exp_list, reverse_lookup, colour_list):

    # fill out preliminaries: #
    # set width & height & that sorta stuff...

    populate_worksheet(ws, exp_list, reverse_lookup, colour_list)

    style_worksheet(ws, colour_list)


    #########################################################################################

def populate_worksheet(ws, exp_list, reverse_lookup, colour_list):

    ###############################################
    [red, purple, blue, teal, cyan, lavender] =  colour_list
    # FIRST COLUMN:
    # fill in the first column (integrate this later into a complete fill-out function)
    #
    set_header_cell(ws, 1, 1, "Week", "")
    set_header_cell(ws, 2, 1, "SESSION", red)
    set_header_cell(ws, 3, 1, "TELESCOPE", blue)
    set_header_cell(ws, 4, 1, "DATE", teal)
    set_header_cell(ws, 5, 1, "DAY", teal)
    set_header_cell(ws, 6, 1, "d.o.y.", "")
    set_header_cell(ws, 7, 1, "START (LT)", blue)

    ###############################################

  #  my_red_fill = PatternFill(patternType='solid', fgColor=Color(red))

    #########################################################################################

    # configure start points
    i = 2
    j = 8
    # start filling out the heard of the spreadws
    for exp in exp_list:
        #
        set_header_cell(ws, 1, i, f"{exp.get_week_num()}", "")
        set_header_cell(ws, 2, i, f"{exp.name}", red)
        set_header_cell(ws, 3, i, f"{exp.tele}", blue)
        set_header_cell(ws, 4, i, f"{exp.get_start_date()}", teal)
        set_header_cell(ws, 5, i, f"{exp.get_name_of_start_day()}", teal)
        set_header_cell(ws, 6, i, f"{exp.doy}", "")
        set_header_cell(ws, 7, i, f"{exp.get_lt_start()}", blue)

        # place holder:
        dur_hr, dur_min = exp.get_duration()
        # check if session overflows to following day
        k = 1 + (dur_hr // 24)
        for l in range(k):
            j = j + l

            set_header_cell(ws, j, 1, (reverse_lookup.get(exp.name)).name, reverse_lookup.get(exp.name).colour)

            # if no overflow
            if k == 1:
                set_header_cell(ws, j, i, f"{exp.get_lt_shift_start()}-{exp.get_lt_shift_end()}", color=reverse_lookup.get(exp.name).colour)

            # if overflows
            elif k == 2:
                if l == 0:
                    set_header_cell(ws, j, i, f"{exp.get_lt_shift_start()}-{exp.get_lt_shift_end()}", color=reverse_lookup.get(exp.name).colour)
                elif l == 1:
                    set_header_cell(ws, j, i, f"{exp.get_lt_shift_start()}-{exp.get_lt_shift_end()}", color=reverse_lookup.get(exp.name).colour)

        #
        i += 1
        j += 1

    #########################################################################################

def style_worksheet(ws, colour_list):

    [red, purple, blue, teal, cyan, lavender] =  colour_list

    alternating_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
    border_style = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    center_alignment = Alignment(horizontal='center', vertical='center')
    #
    for row in ws.iter_rows(min_row=7, max_row=ws.max_row):
        for cell in row:
         #   cell.border = border_style
            if row[0].row % 2 == 0:  # Apply fill to even rows
                cell.fill = alternating_fill


    ###
    for row in ws.iter_rows(min_row=ws.max_row, max_row=ws.max_row):
        for cell in row:
            cell.border = Border(bottom=Side(style='thick'))


    for col in ws["A"]:
        col.border = Border(left=Side(style='thick'), right=Side(style='thick'))

    ws[f"A{ws.max_row}"].border = Border(left=Side(style='thick'), bottom=Side(style='thick'), right=Side(style='thick'))

    for row in ws.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.border = Border(bottom=Side(style='thick'), top=Side(style='thick'))

    ws["A1"].border = Border(left=Side(style='thick'), bottom=Side(style='thick'), right=Side(style='thick'), top=Side(style='thick'))

    for row in ws.iter_rows(min_row=7, max_row=7):
        for cell in row:
            cell.border = Border(bottom=Side(style='thick'))

    for row in ws.iter_cols(ws.max_column):
        for cell in row:
            cell.border = Border(right=Side(style='thick'))

    ws["A7"].border = Border(left=Side(style='thick'), bottom=Side(style='thick'), right=Side(style='thick'))

    ws.column_dimensions['A'].width = 20

    for cc in ws.columns:
        ws.column_dimensions[get_column_letter(cc[0].column)].width = 15


    ###

    for row in ws.iter_rows(min_row=1, max_row=7):
        for cell in row:
            if cell.value == "Nn":
                cell.fill = PatternFill(patternType='lightUp', fgColor=Color(lavender))
            if cell.value == "Ns":
                cell.fill = PatternFill(patternType='lightUp', fgColor=Color(teal))



   # for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
   #     for cell in row:
   #         cell.border = Border(left=Side(style='thin'), right=Side(style='thin'))


def set_header_cell(ws, i, j, value, color):

    ws.cell(row=i, column=j).value = value
    ws.cell(row=i, column=j).alignment = Alignment(shrinkToFit=False, horizontal='center', vertical='center')

    if not color:
         ws.cell(row=i, column=j).font = Font(bold=True)
    else:
        ws.cell(row=i, column=j).font = Font(color=color, bold=True)

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
        exp = Session(lc[0], lc[1], lc[2], lc[3], lc[4])
        #name, telescopes, doy_start, ut_start, duration):
        exp_list.append(exp)
    file.close()
    return exp_list


if __name__ == '__main__':
    # parse inputs (month?)
    # create object lists
    # create schedule
    # create workbook (passing in object lists and schedule)
    generate_workbook()
