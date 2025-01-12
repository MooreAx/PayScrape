#Use regex to process and extract info from strings
#amazing website to create regex strings: https://regex101.com/

import re

def line_type(line):
	#returns the type of line from the scrape (from which objects can be constructed)
	if re.search(r"^DUTY END .+", line):
		line_type = "Duty"
	elif re.search(r"^\d+ DHD-.+", line):
		line_type = "Deadhead"
	elif re.search(r"^\d+ FLT .+", line):
		line_type = "Flight"
	elif re.search(r"^\d+ REST .+", line):
		line_type = "Rest"
	else:
		line_type = "Other"
	return(line_type)

def process_Header(line):
	#line 0
	#example: PAIRING ID: 76854 FOR: 5788 - MOORE, A GENERATED: 11-Jan-25 23:39 UTC
	pattern = r"PAIRING ID: (\d*) FOR: (\d*) - (.*, .) GENERATED: (\d{1,2}-...-\d\d \d{1,2}:\d\d UTC)"
	
	match = re.search(pattern, line)

	if match:
		#use dict to store match results
		result = dict(
			PID = match.group(1),
			Searcher = match.group(2),
			Generated = match.group(3)
			)
	else:
		result = dict()

	return(result)


def process_Pairing(line):
	#line 1
	#example: CHECK-IN/START: 18-Dec-24 15:00 LCL FINISHED: 21-Dec-24 19:34 LCL
	pattern = r"CHECK-IN\/START: (\d{1,2}-...-\d\d \d{1,2}:\d\d LCL) FINISHED: (\d{1,2}-...-\d\d \d{1,2}:\d\d LCL)"

	match = re.search(pattern, line)

	if match:
		result = dict(
			StartTime = match.group(1),
			EndTime = match.group(2)
			)
	else:
		result = dict()

	return(result)


def process_DutyPeriod(line):

	#example: DUTY END 9.9 / 9:52 HRS [19-Dec-24 16:30 UTC - 20-Dec-24 02:22 UTC] DUTY FLT HRS: 5.4
	pattern = r"DUTY END (\d{1,2}.\d) \/ (\d{1,2}:\d{2}) HRS \[(\d{1,2}-...-\d\d \d{1,2}:\d\d UTC) - (\d{1,2}-...-\d\d \d{1,2}:\d\d UTC)] DUTY FLT HRS: (\d{1,2}.?\d?)"

	match = re.search(pattern, line)

	if match:
		result = dict(
			DecimalHrs = match.group(1),
			Hrs = match.group(2),
			Start = match.group(3),
			End = match.group(4)
			)
	else:
		result = dict()

	return(result)

def process_Flight(line):

	#example: 10 FLT #223 CYBK CYRT 19-Dec-24 19:13 19-Dec-24 20:07 C-GDSS/ATR42 0.9 159sm
	pattern = r"\d{1,3} FLT #(\d+) (\S+) (\S+) (\d{1,2}-...-\d{1,2} \d{1,2}:\d\d) (\d{1,2}-...-\d{1,2} \d{1,2}:\d\d) (\S+)\/(\S+) (\d+.?\d?) (\d?,?\d?\d?\d)sm"

	match = re.search(pattern, line)

	if match:
		result = dict(
			FlightNumber = match.group(1),
			Origin = match.group(2),
			Destination = match.group(3),
			OutTime = match.group(4),
			InTime = match.group(5),
			Registration = match.group(6),
			Type = match.group(7),
			Distance = match.group(8)
			)
	else:
		result = dict()

	return(result)


def process_Crew(line):

	#example: [CA] Troy Sciberras, [FO] Alex Moore, [FA] Jonathan Ollinik
	pattern = r"\[\S+\] [^,]+"

	crew = re.findall(pattern, line) #list object

	return(crew)


def process_Rest(line):
	
	#example: 4 REST CYBK CYBK 19-Dec-24 00:30 19-Dec-24 10:30 10 0sm
	pattern = r"\d+ REST (\S+) (\S+) (\d{1,2}-...-\d{1,2} \d{1,2}:\d\d) (\d{1,2}-...-\d{1,2} \d{1,2}:\d\d) (\d+.?\d?) (\d?,?\d?\d?\d)sm"

	match = re.search(pattern, line)

	if match:
		result = dict(
			Location1 = match.group(1),
			Location2 = match.group(2),
			Start = match.group(3),
			End = match.group(4),
			Hrs = match.group(5),
			Distance = match.group(6)
			)
	else:
		result = dict()

	return(result)


def process_Deadhead(line):

	#example: 19 DHD-MO309 CYRT CYWG 21-Dec-24 17:30 21-Dec-24 19:19 1.8 912sm
	pattern = r"\d+ DHD-(\S+) (\S+) (\S+) (\d{1,2}-...-\d{1,2} \d{1,2}:\d\d) (\d{1,2}-...-\d{1,2} \d{1,2}:\d\d) (\d+.?\d?) (\d?,?\d?\d?\d)sm"

	match = re.search(pattern, line)

	if match:
		result = dict(
			FlightNumber = match.group(1),
			Origin = match.group(2),
			Destination = match.group(3),
			OutTime = match.group(4),
			InTime = match.group(5),
			Hrs = match.group(6),
			Distance = match.group(7)
			)
	else:
		result = dict()

	return(result)