import csv
import datetime


# class Packages holds the object info for all packages.
class Packages:
    def __init__(self, ID, address, city, state, zipcode, deadline, mass, status, addressID, timeDelivered):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.mass = mass
        self.status = status
        self.addressID = addressID
        self.timeDelivered = timeDelivered

    #  this replaces the default string function to print the important package info.
    def __str__(self):
        return "ID: %s | Address: %s | City: %s | Deadline: %s | Zipcode: %s | Weight: %s | Status: %s | Time Delivered: %s" % (
            self.ID, self.address, self.city, self.deadline, self.zipcode, self.mass, self.status, self.timeDelivered)


# function printAtTime receives package object and the status. This will be used when the status is en route or at hub.
def printAtTime(self, statusTime):
    print("ID: %s | Address: %s | City: %s | Deadline: %s | Zipcode: %s | Weight: %s | Status: %s" % (
        self.ID, self.address, self.city, self.deadline, self.zipcode, self.mass, statusTime))


# function loadPackages receives a file containing all package info and the hash table to insert the packages into.
def loadPackages(fileName, myHash):
    with open(fileName) as allPackages:
        packageData = csv.reader(allPackages, delimiter=',')
        next(packageData)  # skip header.
        for package in packageData:
            startDateTime = datetime.datetime(100, 1, 1, 8, 0, 0)  # set each package to 8:00 am.
            startTime = startDateTime.time()
            # package object.
            p = Packages(package[0], package[1], package[2], package[3], package[4], package[5], package[6],
                         "at the hub",
                         package[7], startTime)

            # insert the package into the hash table.
            myHash.insert(int(package[0]), p)
