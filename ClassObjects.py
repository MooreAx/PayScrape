#create class objects for a pairing

class Flight:
	def __init__(self, flight_number, origin, destination, departure_time, arrival_time):
		self.flight_number = flight_number
		self.origin = origin
		self.destination = destination
		self.departure_time = departure_time
		self.arrival_time = arrival_time

	# returns a printable representation of the object
	def __repr__(self):
		return(f"Flight({self.flight_number}, {self.origin}, {self.destination}, {self.departure_time}, {self.arrival_time})")


class Deadhead:
	def __init__(self, flight_number, origin, destination, departure_time, arrival_time):
		self.flight_number = flight_number
		self.origin = origin
		self.destination = destination
		self.departure_time = departure_time
		self.arrival_time = arrival_time

	# returns a printable representation of the object
	def __repr__(self):
		return(f"Deadhead({self.flight_number}, {self.origin}, {self.destination}, {self.departure_time}, {self.arrival_time})")


class DutyPeriod:
	def __init__(self, start_time, end_time):
		self.start_time = start_time
		self.end_time = end_time
		self.flights = [] #list to store flight objects
		self.deadheads = [] #list to store deadhead objects

	def add_flight(self, flight):
		if isinstance(flight, Flight):
			self.flights.append(flight)
		else:
			raise TypeError("Only Flight objects can be added to a DutyPeriod")

	def add_deadhead(self, deadhead):
		if isinstance(deadhead, Flight):
			self.deadheads.append(deadhead)
		else:
			raise TypeError("Only Flight objects (including deadheads) can be added to a DutyPeriod")

	def add_deadhead(self, deadhead):
		if isinstance(deadhead, Deadhead):
			self.deadheads.append(deadhead)
		else:
			raise TypeError("Only Flight objects can be added to a DutyPeriod")

	# returns a printable representation of the object
	def __repr__(self):
		return(f"DutyPeriod({self.start_time}, {self.end_time}, Flights: {self.flights})")


class Pairing:
	"""Pairing. Only pairing id will be known upfront"""
	def __init__(self, pid, start_time, end_time, crew):
		self.pid = pid
		self.start_time = start_time
		self.end_time = end_time
		self.crew = crew
		self.dutyperiods = [] #list to store duty period objects
		self.restperiods = []
		
	def set_attribute(self, captain = None, fo = None, fa1 = None, fa2 = None, observer = None):
		if captain:
			self.captain = captain
		if fo:
			self.fo = fo
		if fa1:
			self.fa1 = fa1
		if fa2:
			self.fa2 = fa2
		if observer:
			self.observer = observer

	def add_dutyperiod(self, dutyperiod):
		self.dutyperiods.append(dutyperiod)

	def add_rest(self, restperiod):
		self.restperiods.append(restperiod)

	def __repr__(self):
		return(f"Pairing({self.pid}, {self.start_time}, {self.end_time}, Crew: {self.crew}, DutyPeriods: {self.dutyperiods}, RestPeriods: {self.restperiods})")

class Rest:
	def __init__(self, location, start_time, end_time):
		self.location = location
		self.start_time = start_time
		self.end_time = end_time

	def __repr__(self):
		return(f"Rest({self.location}, {self.start_time}, {self.end_time})")



