from DistanceList import getDistanceList

# holds the list of address IDs and their millage between each other sorted by length of distance.
greedyTable = []


# function setGreedyTable sets up the table of sorted addresses and their distances between each other.
def setGreedyTable():
    # first adds 10 empty lists to the greedy table list.
    for i in range(10):
        greedyTable.append([])

    distanceList = getDistanceList()
    # separates each pair of address ID's and their distance between each other by number. The lower the mileage, the
    # earlier the pair will be put in a bucket. This way, when looking for the next best location, the beginning buckets
    # are searched first.
    for miles in distanceList:
        m = miles[2]
        if m < 1.0:
            greedyTable[0].append(miles)
        elif m < 2.0:
            greedyTable[1].append(miles)
        elif m < 3.0:
            greedyTable[2].append(miles)
        elif m < 4.0:
            greedyTable[3].append(miles)
        elif m < 5.0:
            greedyTable[4].append(miles)
        elif m < 6.0:
            greedyTable[5].append(miles)
        elif m < 7.0:
            greedyTable[6].append(miles)
        elif m < 8.0:
            greedyTable[7].append(miles)
        elif m < 9.0:
            greedyTable[8].append(miles)
        else:
            greedyTable[9].append(miles)


# function getGreedyTable returns the greedyTable.
def getGreedyTable():
    return greedyTable


# function closestNeighborAlgorithm receives the current location and a list of addresses to skip.
# returns the closest neighbor and the best mileage between the current and next location.
def closestNeighborAlgorithm(currLocation, skipAddresses):
    found = False
    bucketNum = 0
    closestNeighbor = 0
    bestMiles = 50.5
    # continues until the next closes location is found. First it skips the any address pairs that contain an address to skip.
    # Then it looks if either of the two addresses are equal to the current location.
    # If they are, it saves the closest neighbor as the other address.
    # If any further pairs with the current address in the current bucket have a lower mileage number, then the next
    # location is replaced.
    while (not found) and bucketNum < 10:
        bucket = greedyTable[bucketNum]
        for item in bucket:
            skipItem = False
            # skip addresses with no available packages
            for a in skipAddresses:
                # print(a)
                if int(a) == int(item[0]):
                    skipItem = True
                if int(a) == int(item[1]):
                    skipItem = True
            if skipItem:
                continue
            # if the items closest neighbor
            if item[0] == currLocation:
                if int(item[2]) < bestMiles:
                    bestMiles = item[2]
                    closestNeighbor = item[1]
                    found = True
            elif item[1] == currLocation:
                if int(item[2]) < bestMiles:
                    bestMiles = item[2]
                    closestNeighbor = item[0]
                    found = True
        bucketNum += 1
    return closestNeighbor, bestMiles
