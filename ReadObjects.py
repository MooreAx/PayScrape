'''
Reads scraped data into class instances
'''

import LineProcessor as LP
import ClassObjects as CO

PID = "76854"

#read data from file
with open(f'Pairings/{PID}.txt', 'r') as file:
    s = file.read()

lines = s.splitlines()

#create empty lists for storing objects
Pairings = []
DutyPeriods = []
Flights = []
Deadheads = []
Rests = []

#read distinct lines
h_dict = LP.process_Header(lines[0])
p_dict = LP.process_Pairing(lines[1])
crew = LP.process_Crew(lines[3])
pairing = CO.Pairing(
    pid = h_dict["PID"],
    start_time = p_dict["StartTime"],
    end_time = p_dict["EndTime"],
    crew = crew
    )
Pairings.append(pairing)
print(pairing)

#read remaining lines
for line in lines[4:]:
    match LP.line_type(line):
        case "Duty":
            dp_dict = LP.process_DutyPeriod(line)
            dutyperiod = CO.DutyPeriod(
                start_time = dp_dict["Start"],
                end_time = dp_dict["End"])
            DutyPeriods.append(dutyperiod)
            print(dutyperiod)

        case "Deadhead":
            dh_dict = LP.process_Deadhead(line)
            deadhead = CO.Deadhead(
                flight_number = dh_dict["FlightNumber"],
                origin = dh_dict["Origin"],
                destination = dh_dict["Destination"],
                departure_time = dh_dict["OutTime"],
                arrival_time = dh_dict["InTime"])
            Deadheads.append(deadhead)
            print(deadhead)

        case "Flight":
            f_dict = LP.process_Flight(line)
            flight = CO.Flight(
                flight_number = f_dict["FlightNumber"],
                origin = f_dict["Origin"],
                destination = f_dict["Destination"],
                departure_time = f_dict["OutTime"],
                arrival_time = f_dict["InTime"])
            Flights.append(flight)
            print(flight)

        case "Rest":
            r_dict = LP.process_Rest(line)
            rest = CO.Rest(
                location = r_dict["Location1"],
                start_time = r_dict["Start"], 
                end_time = r_dict["End"])
            Rests.append(rest)
            print(rest)

