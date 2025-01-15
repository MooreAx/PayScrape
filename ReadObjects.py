'''
Reads scraped data into class instances
'''

import LineProcessor as LP
import ClassObjects as CO
import DateTimeCalcs as DT
from datetime import datetime

PID = "78267"

#read data from file
with open(f'Pairings/{PID}.txt', 'r') as file:
    s = file.read()

lines = s.splitlines()

#all pairings start & end at pilot's base
pilotbase = "CYWG"

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
    start_time = DT.lcl_string_to_utc_datetime(p_dict["StartTime"], pilotbase),
    end_time = DT.lcl_string_to_utc_datetime(p_dict["EndTime"], pilotbase),
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
                start_time = DT.utc_string_to_utc_datetime(dp_dict["Start"]),
                end_time = DT.utc_string_to_utc_datetime(dp_dict["End"]))
            DutyPeriods.append(dutyperiod)
            print(dutyperiod)

        case "Deadhead":
            dh_dict = LP.process_Deadhead(line)
            deadhead = CO.Deadhead(
                flight_number = dh_dict["FlightNumber"],
                origin = dh_dict["Origin"],
                destination = dh_dict["Destination"],
                departure_time = DT.lcl_string_to_utc_datetime(dh_dict["OutTime"], dh_dict["Origin"]),
                arrival_time = DT.lcl_string_to_utc_datetime(dh_dict["InTime"], dh_dict["Destination"]))
            Deadheads.append(deadhead)
            print(deadhead)

        case "Flight":
            f_dict = LP.process_Flight(line)
            flight = CO.Flight(
                flight_number = f_dict["FlightNumber"],
                origin = f_dict["Origin"],
                destination = f_dict["Destination"],
                departure_time = DT.lcl_string_to_utc_datetime(f_dict["OutTime"], f_dict["Origin"]),
                arrival_time = DT.lcl_string_to_utc_datetime(f_dict["InTime"], f_dict["Destination"]),
                distance = float(f_dict["Distance"]))
            Flights.append(flight)
            print(flight)

        case "Rest":
            r_dict = LP.process_Rest(line)
            rest = CO.Rest(
                location = r_dict["Location1"],
                start_time = DT.lcl_string_to_utc_datetime(r_dict["Start"], r_dict["Location1"]),
                end_time = DT.lcl_string_to_utc_datetime(r_dict["End"], r_dict["Location1"]),
                latitude = DT.get_airport_info(r_dict["Location1"],"Lat"))
            Rests.append(rest)
            print(rest)


print("\n", "\n")

#assign flights to duty periods
for flight in Flights[:]:
    for dutyperiod in DutyPeriods:
        if flight.departure_time >= dutyperiod.start_time and flight.arrival_time <= dutyperiod.end_time:
            dutyperiod.add_flight(flight)
            Flights.remove(flight)
            break #exit duty period loop, go to next flight

#assign deadheads to duty periods
for deadhead in Deadheads[:]:
    for dutyperiod in DutyPeriods:
        if deadhead.departure_time >= dutyperiod.start_time and deadhead.arrival_time <= dutyperiod.end_time:
            dutyperiod.add_deadhead(deadhead)
            Deadheads.remove(deadhead)
            break #go to next deadhead

#assign rest to pairings
for rest in Rests[:]:
    for pairing in Pairings:
        if rest.start_time >= pairing.start_time and rest.end_time <= pairing.end_time:
            pairing.add_rest(rest)
            Rests.remove(rest)
            break #go to next rest

#assign duty periods to pairing
for dutyperiod in DutyPeriods[:]:
    for pairing in Pairings:
        if dutyperiod.start_time >= pairing.start_time and dutyperiod.end_time <= pairing.end_time:
            pairing.add_dutyperiod(dutyperiod)
            DutyPeriods.remove(dutyperiod)
            break #go to next duty period


def utc(dt):
    return dt.strftime('%Y-%m-%d %H:%MZ')

print('\n\n')

#print summary of pairing

for p in Pairings:
    print(f'--> PAIRING {p.pid} from {utc(p.start_time)} to {utc(p.end_time)}...............................[{round(p.trip_hrs,2):6.2f} hr] / {round(p.min_trip_credits,2):5.2f} cr]')
    for d in p.dutyperiods:
        print(f'  --> DUTY PERIOD from {utc(d.start_time)} to {utc(d.end_time)}.......[{round(d.duty_hrs, 2):5.2f} hr / {round(d.min_credits,2):4.2f} cr]')
        for f in d.flights:
            print(f'     --> FLT {str(f.flight_number).rjust(4)} from {f.origin} to {f.destination}: {round(f.flight_hrs,2):4.2f} hr vs {round(f.scheduled_flight_hrs,2):4.2f} hr skd')
        print(f'  ..................................{round(d.flight_hrs,2):5.2f}......{round(d.scheduled_flight_hrs,2):5.2f}...........................{round(d.credits,2):5.2f} cr')
    print(f'...............................................................................{round(p.duty_period_credits,2):5.2f} cr...................{round(p.trip_credits,2):5.2f} cr')
    print('\n\n')