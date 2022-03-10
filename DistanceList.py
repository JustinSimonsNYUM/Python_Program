import csv

# list of only the address IDs
tempDistanceList = []
# holds the address IDs and their millage between each other
distanceList = []


# returns distanceList.
def getDistanceList():
    return distanceList


# function loadDistanceList receives a file with all address distances between each other.
def loadDistanceList(fileName):
    # first adds a list of all pairs of address ID's.
    i = 1
    numRows = 26
    while i <= numRows:
        j = 0
        while j < i:
            tempDistanceList.append([i, j])
            j += 1
        i += 1

    milesList = []
    # take all distance numbers from the file and add it to the miles list.
    with open(fileName) as allPackages:
        packageData = csv.reader(allPackages, delimiter=',')
        next(packageData)  # skip header
        lastPoint = 0
        for package in packageData:
            lastPoint += 1
            m = 0
            while m < lastPoint:
                milesList.append(package[m])
                m += 1
    # combine the list of address ID pairs and the distance between the two for the final distance list.
    x = 0
    for addresses in tempDistanceList:
        addressesAndMiles = addresses + [float(milesList[x])]
        distanceList.append(addressesAndMiles)
        x += 1

