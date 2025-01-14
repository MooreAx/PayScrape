#Read in time zone info

import pandas as pd
import os
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

#note the r prefix is for "raw string" and avoids the escape characters
path = r"C:\Users\moore\OneDrive\Programming\Flying Misc"
file = "AerodromesXYZ.xlsx"
filepath = os.path.join(path,file)

aerodromes = pd.read_excel(filepath)

#initialize timezone finder
tf = TimezoneFinder()

#Look up the time zone using timezone finder. #apply method with axis=1 is equivalent to "rowwise() in r".
#Lamda is an anonymous function with the argument "row", i.e. a row of data
aerodromes["TimeZone"] = aerodromes.apply(lambda row: tf.timezone_at(lat=row["y"], lng=row["x"]), axis=1)

#convert df to nested dictionary
airport_info_dict = pd.Series(aerodromes.apply(
	lambda row: {
	"Name": row["Airport"],
	"Lat": row["y"],
	"Lon": row["x"],
	"Elevation": row["z"],
	"TimeZone": row["TimeZone"]},
	axis=1).values, index=aerodromes.Aerodrome).to_dict()

print(airport_info_dict["YWG"]["Elevation"])

def get_airport_info(aerodrome, parameter):
	return(airport_info_dict[aerodrome][parameter])

def string_to_datetime_utc(string, aerodrome, date_format = "%d-%b-%y %H:%M"):
	naive_datetime = datetime.strptime(string, date_format)
	tz = pytz.timezone(get_airport_info(aerodrome, "TimeZone"))
	localized_datetime = tz.localize(naive_datetime)
	utc_time = localized_datetime.astimezone(pytz.utc)
	return(utc_time)

def string_to_datetime_lcl(string, aerodrome, date_format = "%d-%b-%y %H:%M"):
	naive_datetime = datetime.strptime(string, date_format)
	tz = pytz.timezone(get_airport_info(aerodrome, "TimeZone"))
	localized_datetime = tz.localize(naive_datetime)
	return(localized_datetime)


print(string_to_datetime_utc("11-Jan-25 23:39", "YWG"))