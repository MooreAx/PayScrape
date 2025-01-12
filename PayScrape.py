#Scrape pairing info from VMO

import pandas as pd
import requests
from bs4 import BeautifulSoup
import string


#VMO link without PID
base_url = "https://cav.vmosolutions.net/cwa/pri/F7DF8AE5115C4BF7AA2ED3C74FC5B9A0859B9AA700FA40D09A11563B37DA0266?PID="

#PID (pairing ID)
PID = "76854"

#full link
url = base_url + PID

page = requests.get(url)

#Parse HTML contect
soup = BeautifulSoup(page.text, "html.parser")

def print_line(soup_obj):
    elements = [element.strip() for element in soup_obj.stripped_strings]
    combined_text = " ".join(elements)
    return(combined_text)

#s is a string that stores info extracted from the soup
s = ""

header1 = soup.find("div", id="mdivTop")
temp = print_line(header1)
s = temp
print(temp)

header2 = soup.find("div", id ="secTimes")
temp = print_line(header2)
s = s + '\n' + temp
print(temp)

rows = soup.find_all("tr")
for row in rows:
    temp = print_line(row)
    s = s + '\n' + temp
    print(temp)

lines = s.splitlines()

#write pairing to file
with open(f'Pairings/{PID}.txt', 'w') as file:
    file.write(s)


import LineProcessor as LP
import ClassObjects as CO

Pairings = []
DutyPeriods = []
Flights = []
Deadheads = []
Rests = []

print("\n\n")

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
            deadhead = CO.Flight(
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

