import datetime
# beginning time of work day: 8:00 am.
START_TIME = datetime.datetime(100, 1, 1, 8, 0, 0)


# function MilesPerHour receives the total mileage traveled by a truck and returns the time of day based off 18 MPH.
def MilesPerHour(miles):
    MPH = miles / 18
    t1CurrentTime = START_TIME + datetime.timedelta(hours=MPH)
    return t1CurrentTime.time()

