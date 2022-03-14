"""
Justin Simons
student ID: 001120973
"""
# main file for the program.

from Packages import loadPackages
from HashTable import HashTable
from DistanceList import loadDistanceList
from Greedy import setGreedyTable
from Trucks import sendTrucks, printAllTruckInfo, printTotalMiles, printPackageAtTime, printAllPackagesAtTime

# instance of hash table for all packages.
hTable = HashTable()

# Load addresses to Table.
loadPackages('packageData.csv', hTable)
# Load distances from one location to another for all addresses.
loadDistanceList('distanceData.csv')
# sets the greedy table to sort the distances of all addresses.
setGreedyTable()
# starts the main delivery function.
sendTrucks(hTable)

# this holds the user interface code. The user can choose from 5 different options.
if __name__ == '__main__':
    # loop until user is satisfied.
    isExit = True
    print("Welcome to the Delivery Truck Program.")
    while isExit:
        print("\nOptions:")
        print("1. Print all packages along with their info.")
        print("2. Print the total miles traveled by both trucks.")
        print("3. Print the info of one package at a specific time.")
        print("4. Print all packages and their info at a certain time.")
        print("5. Exit the Program.")
        option = input("Chose an option (1,2,3,4, or 5): ")
        if option == "1":
            printAllTruckInfo()
        elif option == "2":
            printTotalMiles()
        elif option == "3":
            printPackageAtTime(hTable)
        elif option == "4":
            printAllPackagesAtTime(hTable)
        elif option == "5":
            isExit = False
        else:
            print("Wrong option, please try again!")

