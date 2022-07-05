# open all files for editing
new_route = open("route_tests\WaterRoute220629.exp", "r")
old_route = open("route_tests\WaterRoute220531.exp", "r")
edited_file = open("edited_route_full.exp", "w")
error_output = open("error_output.txt", "w")

# we want to parse through the new route, and convert it to the old formatting style
for line in new_route:

    # initialization of variables to write
    route_name = line[0:20]
    id_number = line[28:38]
    m_code_l = line[26:41]
    m_code_no_l = line[28:40]
    error_parsing_values = line[53:110]
    measured_flow = line[69:78]
    date_scheme = "062522062622"
    account_specific_info = line[122:251]
    remainder_of_line = line[267:]
    has_acct_id = False

    # parse through route of old format to find information not contained in new
    for section in old_route:
        # grab account id from old routing format
        if id_number in section:
            acct_id = section[250:].split(' ')[0]
            has_acct_id = True

    ## ERROR OUTPUTTING ##
    # if there is no account id, likely a newly added home as of this month, so add to error output
    if not has_acct_id:
        error_output.write("ID Number: " + id_number + " did not have a previous account.\n")
        acct_id = "ERROR"
    # error output for flow read issue
    if not measured_flow.isnumeric():
        error_output.write("ID Number: " + id_number + " had a flow reading error.\n")
    # error output for no flow this month
    if measured_flow == "000000000":
        error_output.write("ID Number: " + id_number + " had no flow this month.\n")


    # printing for debugging purposes
    print(acct_id)
    print(id_number)
    print(measured_flow)

    # write out the new file
    edited_file.write(route_name + "ES1000" + m_code_l + m_code_no_l + error_parsing_values
                      + date_scheme + account_specific_info + acct_id + remainder_of_line)


# close all files once done editing
new_route.close()
edited_file.close()
error_output.close()
old_route.close()



