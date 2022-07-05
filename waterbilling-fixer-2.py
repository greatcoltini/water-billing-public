import os

# global errors list
errors = []


# PARSES THE OLD ROUTE, ADDING THE NEW FLOW CALCULATED FROM THIS MONTH'S METER READS
# DOES NOT ACCOUNT FOR NEW METERS ADDED HERE... MUST MANUALLY ADJUST.
def parse_route(last_month, this_month):
    print("Parsing old route and adding new route flow data...")
    # open all files for editing
    old_route = open(last_month, "r")
    edited_file = open("edited_route_full_from_old.exp", "w")
    for line in old_route:

        # initialization of variables to write
        route_number = line[0:20]
        up_to_meter = line[20:41]
        meter_id = line[28:38]
        spacing_to_flow = line[52:68]
        measured_flow = line[69:88]
        spacing_to_date = line[89:108]
        date = "062522062622"
        spacing_to_routing = line[123:130]
        routing_info = line[131:147]
        remainder = line[148:]

        # parse through new route, find id, add meter info
        new_route = open(this_month, "r")
        for section in new_route:
            # grab account id from old routing format
            compare_id = section[28:38]
            if meter_id == compare_id:
                measured_flow = section[68:78]
                routing_info = section[131:147]
                route_number = section[0:20]
                break
        new_route.close()

        # write out the new file
        edited_file.write(route_number + up_to_meter + meter_id + spacing_to_flow + measured_flow + spacing_to_date +
                          date + spacing_to_routing + routing_info + remainder)

    # close the files
    old_route.close()
    edited_file.close()


# CALCULATES WHICH METERS MAY BE IDENTIFIABLE AS NEW METERS
# COMPARES NEW ROUTE IDS WITH OLD ROUTE, IF MISMATCH, MAY BE NEW METER
def calculate_new_meters(last_month_imp, this_month_imp):
    print("Determining which meters are new additions...")
    # loop through each line of the new route, finding id
    new_route_compare = open(this_month_imp, "r")

    # we loop through the new route meters, and check if mismatch from old route, if so we know it's a new install
    for section in new_route_compare:
        meter_id = section[28:38]
        new_meter = True
        old_route_compare = open(last_month_imp, "r")
        for line in old_route_compare:
            compare_id = line[28:38]
            if meter_id == compare_id:
                new_meter = False
                break
        if new_meter:
            error = "Meter: " + str(meter_id) + " is a newly added meter.\n"
            errors.append(error)


# WRITES ERRORS TO OUTPUT FILE FROM GLOBAL ERRORS LIST
def write_errors():
    print("Writing errors to file error_output.txt...\n")
    print("Total of " + str(len(errors)) + " errors.\n")
    error_output = open("error_output.txt", "w")
    for string in errors:
        error_output.write(string)
    error_output.close()


def main():
    # run our functions
    # take user input, to send to parse_route
    last_month_imp = input("Enter the path of last month's route information: ")
    this_month_imp = input("Enter the path of this month's route information: ")
    assert os.path.exists(last_month_imp), "Error: no file at presented path " + str(last_month_imp)
    assert os.path.exists(this_month_imp), "Error: no file at presented path " + str(last_month_imp)

    parse_route(last_month_imp, this_month_imp)
    calculate_new_meters(last_month_imp, this_month_imp)
    write_errors()


if __name__ == "__main__":
    main()
