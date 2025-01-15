#create class objects for a pairing
#for calculating status as a northern pairing
CYYQ_Latitude = 58 + 44/60 + 26/3600 #degrees north

class Flight:
	def __init__(self, flight_number, origin, destination, departure_time, arrival_time, distance):
		self.flight_number = flight_number
		self.origin = origin
		self.destination = destination
		self.departure_time = departure_time
		self.arrival_time = arrival_time
		self.flight_hrs = (arrival_time - departure_time).total_seconds() / 3600
		self.distance = distance
		self.scheduled_flight_hrs = self.distance / 260 + 0.1 # plus 6 minutes per sector

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
		self.flight_hrs = (arrival_time - departure_time).total_seconds() / 3600

	# returns a printable representation of the object
	def __repr__(self):
		return(f"Deadhead({self.flight_number}, {self.origin}, {self.destination}, {self.departure_time}, {self.arrival_time})")


class DutyPeriod:
	def __init__(self, start_time, end_time):
		self.start_time = start_time
		self.end_time = end_time
		self.flights = [] #list to store flight objects
		self.deadheads = [] #list to store deadhead objects
		self.rests = []
		self.duty_hrs = (end_time - start_time).total_seconds() / 3600
		self.min_credits = max(4, self.duty_hrs/2)
		
	def add_flight(self, flight):
		if isinstance(flight, Flight):
			self.flights.append(flight)
		else:
			raise TypeError("expected Flight object")

	def add_deadhead(self, deadhead):
		if isinstance(deadhead, Deadhead):
			self.deadheads.append(deadhead)
		else:
			raise TypeError("expected Deadhead object")

	def add_rest(self, rest):
		if isinstance(rest, Rest):
			self.rests.append(rest)
		else:
			raise TypeError("expected Rest object")

	@property
	def flight_hrs(self):
		return sum(flight.flight_hrs for flight in self.flights)

	@property
	def scheduled_flight_hrs(self):
		return sum(flight.scheduled_flight_hrs for flight in self.flights)

	@property
	def flight_credits(self):
		return self.flight_hrs if self.flight_hrs > 1.1 * self.scheduled_flight_hrs else self.scheduled_flight_hrs

	@property
	def credits(self):
		return max(self.min_credits, self.flight_credits)

	# returns a printable representation of the object
	def __repr__(self):
		return(f"DutyPeriod({self.start_time}, {self.end_time}, {self.duty_hrs}, Flights: {self.flights})")


class Pairing:
	def __init__(self, pid, start_time, end_time, crew):
		self.pid = pid
		self.start_time = start_time
		self.end_time = end_time
		self.crew = crew
		self.dutyperiods = [] #list to store duty period objects
		self.restperiods = []
		self.trip_hrs = (end_time - start_time).total_seconds() / 3600
	
	def add_dutyperiod(self, dutyperiod):
		self.dutyperiods.append(dutyperiod)

	def add_rest(self, restperiod):
		self.restperiods.append(restperiod)

	@property
	def northern_rest(self):
		return any(rest.northern_rest for rest in self.restperiods)

	@property
	def min_trip_credits(self):
		return self.trip_hrs / 3.55 if self.northern_rest else self.trip_hrs / 4

	@property
	def duty_period_credits(self):
		return sum(dutyperiod.credits for dutyperiod in self.dutyperiods)

	@property
	def trip_credits(self):
		return max(self.min_trip_credits, self.duty_period_credits)

	def __repr__(self):
		return(f"Pairing({self.pid}, {self.start_time}, {self.end_time}, Crew: {self.crew}, DutyPeriods: {self.dutyperiods}, RestPeriods: {self.restperiods})")

class Rest:
	def __init__(self, location, start_time, end_time, latitude):
		self.location = location
		self.start_time = start_time
		self.end_time = end_time
		self.rest_hrs = (start_time - end_time) / 3600
		self.latitude = latitude

		if self.latitude >= CYYQ_Latitude:
			self.northern_rest = True
		else:
			self.northern_rest = False

	def __repr__(self):
		return(f"Rest({self.location}, {self.start_time}, {self.end_time})")

