from Greedy import closestNeighborAlgorithm
from deliveryTime import MilesPerHour
import datetime
from Packages import printAtTime

# truck1 and truck2 holds the first and second delivery route of the trucks with the packages delivered.
truck1 = [[], []]
truck2 = [[], []]
totalMilesAfterRoute = []
# list of packages to only be delivered on truck two. Holds first the package ID and then the address ID.
t2OnlyPackages = [[3, 8], [18, 3], [36, 7], [38, 19]]
# list of all packages. first will be the package ID and the second will be true or false to show if it's available for delivery.
availablePackages = []
# list of addresses to skip.
skipAddresses = []
# Package IDs that need to be delivered by 10:30.
tenThirtyPackages = [1, 6, 13, 14, 16, 20, 25, 29, 30, 31, 34, 37, 40]
# package IDs that need to be delivered by 9:00.
ninePackages = [15]
# package IDs must be delivered on the same truck in the same route.
beTogether = [13, 14, 15, 16, 19, 20]


# function setInitAvailablePackages sets all packages to availablePackages with their ID, addressID, and true if ready or false if not.
def setInitAvailablePackages(packageTable):
    i = 1
    while i <= 40:
        p = packageTable.search(i)
        # these packages won't be available for delivery until 9:05.
        if (i == 6) or (i == 9) or (i == 25) or (i == 28) or (i == 32):
            availablePackages.append([p.ID, p.addressID, False])
        else:
            availablePackages.append([p.ID, p.addressID, True])
        i += 1


# function addNineFivePackages sets packages 6,25,28,and 32 to available packages as true at 9:05 am.
def addNineFivePackages():
    for ap in availablePackages:
        if (int(ap[0]) == 6) or (int(ap[0]) == 25) or (int(ap[0]) == 28) or (int(ap[0]) == 32):
            ap[2] = True


# function addTenTwentyPackage sets package 9 to available packages as true and changes the address to correct one at 10:20.
def addTenTwentyPackage(packageTable):
    for ap in availablePackages:
        if int(ap[0]) == 9:
            ap[1] = 19
            ap[2] = True

    p = packageTable.search(9)
    p.address = "410 S State St"
    p.city = 'Salt Lake City'
    p.zipcode = 84111
    p.addressID = 19


# function sendTrucks holds the code that sends both trucks 1 and 2.
def sendTrucks(packageTable):
    # call setInitAvailablePackages to set all available packages.
    setInitAvailablePackages(packageTable)
    # trucks total miles.
    t1TotalMiles = 0
    t2TotalMiles = 0
    # truck location and best miles' info.
    t1CurrentLocation, t1NextLocation, t1BestMiles = 0, 0, 0
    t2CurrentLocation, t2NextLocation, t2BestMiles = 0, 0, 0
    # trucks bucket number.
    t1Bucket = 0
    t2Bucket = 0
    # number of delivery on the truck route. 1-16
    t1BucketValue = 0
    t2BucketValue = 0
    # trucks back to base is set to true if the truck has been sent back to the hub to pick up more packages.
    t1BtB = False
    t2BtB = False
    # trucks bucket2 is set to true to show that the 9:05 packages have been delivered at the hub and the truck
    # has gone back to base to pick them up. Thus, the current location is set to 0 and starts the next bucket route.
    t1Bucket2 = False
    t2Bucket2 = False
    # the trucks can only deliver 16 packages at a time.
    MAX_BUCKET = 16
    # 9:05 and 10:20 date times are set.
    nineFive = datetime.datetime(100, 1, 1, 9, 5, 0)
    tenTwenty = datetime.datetime(100, 1, 1, 10, 20, 0)
    # trucks tenTwentyDone is set to true when the time is past 10:20.
    t1TenTwentyDone = False
    t2TenTwentyDone = False
    # trucks nineFiveDone is set to true when the time is past 9:05.
    t1NineFiveDone = False
    t2NineFiveDone = False

    deliveredPackages = 0
    # while-loop continues until all 40 packages have been delivered.
    while deliveredPackages < 40:
        # ---------------------truck1's packages ----------------
        # if-statement is true when 16 packages have been delivered.
        if t1BucketValue >= MAX_BUCKET:
            t1Bucket += 1
            t1BucketValue = 0
            t1CurrentLocation = 0

        skipAddresses.clear()
        # these three values are used to see if priority packages still needs to be delivered or not.
        beTogetherFound = False
        ninePackageFound = False
        tenThirtyPackageFound = False

        # first checks if the packages that must be together still need to be delivered.
        # checks all packages to see if their available and if they are in the beTogether list.
        for ap in availablePackages:
            if ap[2]:
                for bt in beTogether:
                    if int(ap[0]) == bt:
                        beTogetherFound = True
        # second, checks to see if any packages that must be delivered by 9:00 still need to be delivered.
        # if-statement is skipped if beTogetherFound is True.
        if not beTogetherFound:
            # checks all packages to see if their available and if they are in the ninePackages list.
            for ap in availablePackages:
                if ap[2]:
                    for np in ninePackages:
                        if int(ap[0]) == np:
                            ninePackageFound = True
        # third, checks to see if any packages that must be delivered by 10:30 still need to be delivered.
        # if-statement is skipped if beTogetherFound and ninePackageFound is True.
        if (not ninePackageFound) and (not beTogetherFound):
            # checks all packages to see if their available and if they are in the tenThirtyPackages list.
            for ap in availablePackages:
                if ap[2]:
                    for tp in tenThirtyPackages:
                        if int(ap[0]) == tp:
                            tenThirtyPackageFound = True
        skipAddressNum = 0
        # apFound set to true when an available package is found.
        apFound = False
        # find next closest location for truck 1.
        while not apFound:
            # breaks loop if all 26 addresses are checked and no best next location is found.
            if skipAddressNum > 26:
                break
            # if-statement is true if its past 9:05 and the truck is at the hub.
            if (int(t1CurrentLocation == 0)) and t1NineFiveDone and (not t1BtB):
                t1BtB = True
            # calls closestNeighborAlgorithm to get the next closest location along with the miles between the two addresses.
            t1NextLocation, t1BestMiles = closestNeighborAlgorithm(t1CurrentLocation, skipAddresses)
            # if-statement is true if its past 9:05 and the trucks next best location is the hub.
            if (int(t1NextLocation == 0)) and t1NineFiveDone and (not t1BtB):
                t1BtB = True
            # elif-statement executes if the truck doesn't need to return to the hub and next location is 0.
            elif int(t1NextLocation) == 0:
                skipAddresses.append(0)
                skipAddressNum += 1
                continue
            #  first go through those that need to be delivered on the same route. If one is available, set the current
            #  location to next location when the packages address equals the next location.
            if beTogetherFound:
                # goes through all available packages to see if any need to be delivered to the next best location.
                for ap in availablePackages:
                    # if the package is True, thus available, it's location is checked to see if it matches the next location.
                    if ap[2]:
                        for bt in beTogether:
                            if int(ap[0]) == bt:
                                if int(ap[1]) == int(t1NextLocation):
                                    apFound = True
                                    t1CurrentLocation = t1NextLocation
                                    break
                    if apFound:
                        break
                    # if no available packages address equals the next location, add the address to skipAddresses.
                    # this makes it possible to keep trying to find the next best location until an available package
                    # can be delivered.
                    if int(ap[0]) == 40:
                        skipAddresses.append(int(t1NextLocation))
                        skipAddressNum += 1
            #  next go through those that need to be delivered before 9:00. if one is available, set the current
            #  location to next location when the packages address equals the next location.
            elif ninePackageFound:
                # goes through all available packages to see if any need to be delivered to the next best location.
                for ap in availablePackages:
                    # if the package is True, thus available, it's location is checked to see if it matches the next location.
                    if ap[2]:
                        for np in ninePackages:
                            if int(ap[0]) == np:
                                if int(ap[1]) == int(t1NextLocation):
                                    apFound = True
                                    t1CurrentLocation = t1NextLocation
                                    break
                    if apFound:
                        break
                    # if no available packages address equals the next location, add the address to skipAddresses.
                    if int(ap[0]) == 40:
                        skipAddresses.append(int(t1NextLocation))
                        skipAddressNum += 1
            # lastly, go through those that need to be delivered before 10:30. if one is available, set the current
            # location to next location when the packages address equals the next location.
            elif tenThirtyPackageFound:
                # goes through all available packages to see if any need to be delivered to the next best location.
                for ap in availablePackages:
                    # if-statement is true if a 9:05 package is available and the truck has gone back to the hub.
                    # this is only executed once since the truck only picks up the packages once.
                    if (int(ap[0]) == 6) or (int(ap[0]) == 25):
                        if t1BtB and ap[2] and (not t1Bucket2):
                            t1CurrentLocation = 0
                            # adds the miles it takes to get from the current location back to the hub.
                            t1TotalMiles += t1BestMiles
                            # if the truck is not at the hub, start next truck route and set bucket value to 0.
                            if t1BucketValue != 0:
                                t1Bucket += 1
                                t1BucketValue = 0
                            t1Bucket2 = True
                            break
                        elif not t1Bucket2:
                            continue
                    # if the package is True, thus available, it's location is checked to see if it matches the next location.
                    if ap[2]:
                        for tp in tenThirtyPackages:
                            if int(ap[0]) == tp:
                                if int(ap[1]) == int(t1NextLocation):
                                    apFound = True
                                    t1CurrentLocation = t1NextLocation
                                    break
                    if apFound:
                        break
                    # if no available package address equals the next location, add the address to skipAddresses.
                    if int(ap[0]) == 40:
                        skipAddresses.append(int(t1NextLocation))
                        skipAddressNum += 1
            # else-statement executes only if all priority packages have been delivered first.
            else:
                # goes through all available packages to see if any need to be delivered to the next best location.
                for ap in availablePackages:
                    # these packages can only be on truck 2.
                    if (int(ap[0]) == 3) or (int(ap[0]) == 18) or (int(ap[0]) == 36) or (int(ap[0]) == 38):
                        continue
                    # if-statement is true if a 9:05 package is available and the truck has gone back to the hub.
                    # this is only executed once since the truck only picks up the packages once.
                    if (int(ap[0]) == 6) or (int(ap[0]) == 25) or (int(ap[0]) == 28) or (int(ap[0]) == 32):
                        if t1BtB and ap[2] and (not t1Bucket2):
                            t1CurrentLocation = 0
                            # adds the miles it takes to get from the current location back to the hub.
                            t1TotalMiles += t1BestMiles
                            # if the truck is not at the hub, start next truck route and set bucket value to 0.
                            if t1BucketValue != 0:
                                t1Bucket += 1
                                t1BucketValue = 0
                            t1Bucket2 = True
                            break
                        elif not t1Bucket2:
                            continue
                    # skip package 9 if it's not past 10:20.
                    if int(ap[0]) == 9:
                        if not t1TenTwentyDone:
                            continue
                    # if the package is True, thus available, it's location is checked to see if it matches the next location.
                    if ap[2]:
                        if int(ap[1]) == int(t1NextLocation):
                            apFound = True
                            t1CurrentLocation = t1NextLocation
                            break
                    # if no available packages address equals the next location, add the address to skipAddresses.
                    if int(ap[0]) == 40:
                        skipAddresses.append(int(t1NextLocation))
                        skipAddressNum += 1

        multiPackages = False
        # goes through all packages to deliver those that are available and their location matches the next location.
        for ap in availablePackages:
            # skips these packages since they can only be delivered on truck 2.
            if (int(ap[0]) == 3) or (int(ap[0]) == 18) or (int(ap[0]) == 36) or (int(ap[0]) == 38):
                continue
            # skips these 9:05 packages until the truck has gone back to the hub to pick them up.
            if (int(ap[0]) == 6) or (int(ap[0]) == 25) or (int(ap[0]) == 28) or (int(ap[0]) == 32):
                if not t1Bucket2:
                    continue
            # skips package 9 until it's past 10:20.
            if int(ap[0]) == 9:
                if not t1TenTwentyDone:
                    continue
            # if the packages address equals the next location, and it's available, then its delivered.
            if (int(ap[1]) == int(t1NextLocation)) and ap[2]:
                # break loop if 16 packages have already been delivered.
                if t1BucketValue >= MAX_BUCKET:
                    break
                else:
                    t1Package = packageTable.search(int(ap[0]))
                    t1Package.status = "delivered"
                    ap[2] = False
                    # if-statement executes if it's the first package delivered to this address on this route.
                    # it adds the best miles to the total miles to determine the time it was delivered.
                    if not multiPackages:
                        t1TotalMiles += t1BestMiles
                        t1Package.timeDelivered = MilesPerHour(t1TotalMiles)
                        multiPackages = True
                    # else-statement executes if this is not the first package delivered to this address on this route.
                    # sets the same delivered time as the first package.
                    else:
                        t1Package.timeDelivered = MilesPerHour(t1TotalMiles)
                    # checks if the time is past 9:05. If true, it sets nineFiveDone to true.
                    if (MilesPerHour(t1TotalMiles) >= nineFive.time()) and (not t1NineFiveDone):
                        if (not t1NineFiveDone) and (not t2NineFiveDone):
                            addNineFivePackages()
                        t1NineFiveDone = True
                    # checks if the time is past 10:20. If true, it sets tenTwentyDone to true.
                    if (MilesPerHour(t1TotalMiles) >= tenTwenty.time()) and (not t1TenTwentyDone):
                        if (not t1TenTwentyDone) and (not t2TenTwentyDone):
                            addTenTwentyPackage(packageTable)
                        t1TenTwentyDone = True
                    # adds the package to the current trucks load
                    truck1[t1Bucket].append(t1Package)
                    t1BucketValue += 1
                    deliveredPackages += 1
        # break while loop if 40 packages have been delivered
        if deliveredPackages >= 40:
            break

        # -----------------------truck2's packages -------------------

        # if-statement is true when 16 packages have been delivered.
        if t2BucketValue >= MAX_BUCKET:
            t2Bucket += 1
            t2BucketValue = 0
            t2CurrentLocation = 0
        skipAddresses.clear()
        skipAddressNum = 0
        # ninePackageFound is set to true if a 9:00 package is found.
        ninePackageFound = False
        # tenThirtyPackageFound is set to true if a 10:30 package is found.
        tenThirtyPackageFound = False

        # first checks if any priority packages still need to be delivered.
        # checks all packages to see if their available and if they are in the ninePackages list.
        for ap in availablePackages:
            if ap[2]:
                for np in ninePackages:
                    if int(ap[0]) == np:
                        ninePackageFound = True

        # if-statement is skipped if ninePackageFound is True.
        if not ninePackageFound:
            # checks all packages to see if their available and if they are in the tenThirtyPackages list.
            for ap in availablePackages:
                if ap[2]:
                    for tp in tenThirtyPackages:
                        if int(ap[0]) == tp:
                            tenThirtyPackageFound = True

        # apFound set to true when an available package is found.
        apFound = False
        # find the next best location for truck 2.
        while not apFound:
            # breaks the loop if all 26 addresses have been checked and no next best address is found for a package.
            if skipAddressNum > 26:
                break
            # if-statement is true if its past 9:05 and the truck is at the hub.
            if (int(t2CurrentLocation == 0)) and t2NineFiveDone and (not t2BtB):
                t2BtB = True
            # calls closestNeighborAlgorithm function to get the next location and the miles between the two addresses.
            t2NextLocation, t2BestMiles = closestNeighborAlgorithm(t2CurrentLocation, skipAddresses)
            # if-statement is true if its past 9:05 and the trucks next best location is the hub.
            if (int(t2NextLocation == 0)) and t2NineFiveDone and (not t2BtB):
                t2BtB = True
            # elif-statement executes if the truck doesn't need to return to the hub.
            elif int(t2NextLocation) == 0:
                skipAddresses.append(0)
                skipAddressNum += 1
                continue

            # first go through those that need to be delivered before 9:00 if true.
            if ninePackageFound:
                # goes through all available packages to see if any need to be delivered to the next best location.
                for ap in availablePackages:
                    # if the package is True, thus available, it's location is checked to see if it matches the next location.
                    if ap[2]:
                        for np in ninePackages:
                            if int(ap[0]) == np:
                                if int(ap[1]) == int(t1NextLocation):
                                    apFound = True
                                    t1CurrentLocation = t1NextLocation
                                    break
                    if apFound:
                        break
                    # if no available packages address equals the next location, add the address to skipAddresses.
                    if int(ap[0]) == 40:
                        skipAddresses.append(int(t1NextLocation))
                        skipAddressNum += 1
            # next go through those that need to be delivered before 10:30 if true.
            elif tenThirtyPackageFound:
                # goes through all available packages to see if any need to be delivered to the next best location.
                for ap in availablePackages:
                    #  must be delivered together. Only put on truck 1.
                    if (int(ap[0]) == 13) or (int(ap[0]) == 14) or (int(ap[0]) == 15) or (int(ap[0]) == 16) or (
                            int(ap[0]) == 19) or (int(ap[0]) == 20):
                        continue
                    # if-statement is true if a 9:05 package is available and the truck has gone back to the hub.
                    # this is only executed once since the truck only picks up the packages once.
                    if (int(ap[0]) == 6) or (int(ap[0]) == 25):
                        if t2BtB and ap[2] and (not t2Bucket2):
                            t2CurrentLocation = 0
                            # adds the miles it takes to get from the current location back to the hub.
                            t2TotalMiles += t2BestMiles
                            # if the truck is not at the hub, start next truck route and set bucket value to 0.
                            if t2BucketValue != 0:
                                t2Bucket += 1
                                t2BucketValue = 0
                            t2Bucket2 = True
                            break
                        elif not t2Bucket2:
                            continue
                    # if the package is True, thus available, it's location is checked to see if it matches the next location.
                    if ap[2]:
                        for tp in tenThirtyPackages:
                            if int(ap[0]) == tp:
                                if int(ap[1]) == int(t2NextLocation):
                                    apFound = True
                                    t2CurrentLocation = t2NextLocation
                                    break
                    if apFound:
                        break
                    # if no available packages address equals the next location, add the address to skipAddresses.
                    if int(ap[0]) == 40:
                        skipAddresses.append(int(t2NextLocation))
                        skipAddressNum += 1
            #  lastly go through the remaining packages.
            else:
                # goes through all available packages to see if any need to be delivered to the next best location.
                for ap in availablePackages:
                    # must be delivered together. Only put on truck 1.
                    if (int(ap[0]) == 13) or (int(ap[0]) == 14) or (int(ap[0]) == 15) or (int(ap[0]) == 16) or (
                            int(ap[0]) == 19) or (int(ap[0]) == 20):
                        continue
                    # if-statement is true if a 9:05 package is available and the truck has gone back to the hub.
                    # this is only executed once since the truck only picks up the packages once.
                    if (int(ap[0]) == 6) or (int(ap[0]) == 25) or (int(ap[0]) == 28) or (int(ap[0]) == 32):
                        if t2BtB and ap[2] and (not t2Bucket2):
                            t2CurrentLocation = 0
                            # adds the miles it takes to get from the current location back to the hub.
                            t2TotalMiles += t2BestMiles
                            # if the truck is not at the hub, start next truck route and set bucket value to 0.
                            if t2BucketValue != 0:
                                t2Bucket += 1
                                t2BucketValue = 0
                            t2Bucket2 = True
                            break
                        elif not t2Bucket2:
                            continue
                    if int(ap[0]) == 9:
                        if not t2TenTwentyDone:
                            continue
                    # if the package is True, thus available, it's location is checked to see if it matches the next location.
                    if ap[2]:
                        if int(ap[1]) == int(t2NextLocation):
                            apFound = True
                            t2CurrentLocation = t2NextLocation
                            break
                    # if no available packages address equals the next location, add the address to skipAddresses.
                    if int(ap[0]) == 40:
                        skipAddresses.append(int(t2NextLocation))
                        skipAddressNum += 1

        multiPackages = False
        # goes through all packages to deliver all those that are available and their location matches the next location.
        for ap in availablePackages:
            # these packages will only be on truck 1.
            if (int(ap[0]) == 13) or (int(ap[0]) == 14) or (int(ap[0]) == 15) or (int(ap[0]) == 16) or (
                    int(ap[0]) == 19) or (int(ap[0]) == 20):
                continue
            # skips these 9:05 packages until the truck has gone back to the hub to pick them up.
            if (int(ap[0]) == 6) or (int(ap[0]) == 25) or (int(ap[0]) == 28) or (int(ap[0]) == 32):
                if not t2Bucket2:
                    continue
            # skips package 9 until its past 10:20.
            if int(ap[0]) == 9:
                if not t2TenTwentyDone:
                    continue
            # if the package address equals the next location, and it's available, then it's delivered.
            if (int(ap[1]) == int(t2NextLocation)) and ap[2]:
                # if-statement breaks loop if 16 packages have been delivered already on this route.
                if t2BucketValue >= MAX_BUCKET:
                    break
                else:
                    t2Package = packageTable.search(int(ap[0]))
                    t2Package.status = "delivered"
                    ap[2] = False
                    # if-statement executes if it's the first package delivered to this address on this route.
                    # it adds the best miles to the total miles to determine the time it was delivered.
                    if not multiPackages:
                        t2TotalMiles += t2BestMiles
                        t2Package.timeDelivered = MilesPerHour(t2TotalMiles)
                        multiPackages = True
                    # else-statement executes if this is not the first package delivered to this address on this route.
                    # sets the same delivered time as the first package.
                    else:
                        t2Package.timeDelivered = MilesPerHour(t2TotalMiles)
                    # checks if the time is past 9:05. If true, it sets nineFiveDone to true.
                    if (MilesPerHour(t2TotalMiles) >= nineFive.time()) and (not t2NineFiveDone):
                        if (not t1NineFiveDone) and (not t2NineFiveDone):
                            addNineFivePackages()
                        t2NineFiveDone = True
                    # checks if the time is past 10:20. If true, it sets tenTwentyDone to true.
                    if (MilesPerHour(t2TotalMiles) >= tenTwenty.time()) and (not t2TenTwentyDone):
                        if (not t1TenTwentyDone) and (not t2TenTwentyDone):
                            addTenTwentyPackage(packageTable)
                        t2TenTwentyDone = True
                    # adds the package to the current truck route.
                    truck2[t2Bucket].append(t2Package)
                    t2BucketValue += 1
                    deliveredPackages += 1

    # totals the miles traveled by both trucks.
    totalMilesAfterRoute.append(t1TotalMiles + t2TotalMiles)


# function printAllTruckInfo prints all packages delivered in order by truck and truck route.
def printAllTruckInfo():
    print('')
    bucketNum = 0
    # first prints all packages in truck1 route 1 then 2.
    for bucket in truck1:
        bucketNum += 1
        print('Truck 1 route number ' + str(bucketNum))
        for item in bucket:
            print(item)
    bucketNum = 0
    # first prints all packages in truck2 route 1 then 2.
    for bucket in truck2:
        bucketNum += 1
        print('Truck 2 route number ' + str(bucketNum))
        for item in bucket:
            print(item)


# function printTotalMiles prints the total mileage traveled by both trucks.
def printTotalMiles():
    print('\nTotal Miles traveled by both trucks: ' + str(totalMilesAfterRoute[0]))


# function printPackageAtTime receives the package hash table and prints one package with its status based on chosen time.
def printPackageAtTime(table):
    packageID = -1
    # while-loop continues until the user enters an integer between 1 and 40 for the package ID.
    while True:
        try:
            packageID = int(input("\nChoose a package ID (1-40): "))
        # ValueError occurs if a non integer is entered.
        except ValueError:
            print("Sorry, you entered an incorrect value. Try again.")
            continue
        # asks user to try again if integer is not between 1 and 40.
        if (int(packageID) < 0) or (int(packageID) > 40):
            print("The number entered is out of range. Please try again.")
        else:
            break

    print("\nEnter a time between 8:00 and 18:00")
    hour = 0
    minute = 0
    # while-loop continues until user enters an integer between 8 and 18 for the Hour.
    while True:
        try:
            hour = int(input("Hour: "))
        # ValueError occurs if a non integer is entered.
        except ValueError:
            print("Sorry, you entered an incorrect value. Try again.")
            continue
        # asks user to try again if integer is not between 8 and 18.
        if (hour < 8) or (hour > 18):
            print("incorrect Time. Try again.")
            continue
        else:
            break

    # while-loop continues until user enters an integer between 0 and 60 for the Minutes.
    while True:
        try:
            minute = int(input("Minute: "))
        # ValueError occurs if a non integer is entered.
        except ValueError:
            print("Sorry, you entered an incorrect value. Try again.")
            continue
        # asks user to try again if integer is not between 0 and 60.
        if (minute < 0) or (minute >= 60) or (minute is None):
            print("incorrect Time. Try again.")
            continue
        else:
            break

    # if-else-statements add 1 minute to the user chosen time for better comparison.
    if minute < 59:
        minute += 1
    else:
        minute = 0
        hour += 1
    # userTime is the user entered time.
    userTime = datetime.datetime(100, 1, 1, hour, minute, 0)
    package = table.search(packageID)

    print('')
    # if the package's delivery time is less than the user time, then print the package with status delivered and delivery time.
    if package.timeDelivered < userTime.time():
        print(package)
    # else-statement prints the package as either en route or at the hub.
    else:
        correctBucket = False
        # inT1 and inT2 are set to true if its in truck 1 or in truck 2.
        inT1 = False
        inT2 = False
        bucket = 0
        # while-loop continues until the correct truck and bucket number is found.
        while not correctBucket:
            # gets the route for truck 1 and 2
            truckLoadT1 = truck1[bucket]
            truckLoadT2 = truck2[bucket]
            # for-loop searches all packages in the route to see if the chosen package is present.
            # if so, the truck and route number is identified for the chosen package.
            for p in truckLoadT1:
                if packageID == int(p.ID):
                    correctBucket = True
                    inT1 = True
                    break
            # for-loop searches all packages in the route to see if the chosen package is present.
            # if so, the truck and route number is identified for the chosen package.
            for p in truckLoadT2:
                if packageID == int(p.ID):
                    correctBucket = True
                    inT2 = True
                    break
            # if-statement executes if the package is not found in the current route. Thus, the next route is checked.
            if not correctBucket:
                bucket += 1

        # if it's in truck 1, then print the package with status en route truck 1 or at the hub.
        if inT1:
            truckLoad = truck1[bucket]
            enRoute = False
            # for-loop determines if the package is en route or not by checking if any other packages on the route are delivered.
            for p in truckLoad:
                if p.timeDelivered < userTime.time():
                    enRoute = True

            if enRoute:
                printAtTime(package, "en route - truck 1.")
            else:
                printAtTime(package, "at the hub.")

        # elif it's in truck 2, then print the package with status en route truck 2 or at the hub.
        elif inT2:
            truckLoad = truck2[bucket]
            enRoute = False
            # for-loop determines if the package is en route or not by checking if any other packages on the route are delivered.
            for p in truckLoad:
                if p.timeDelivered < userTime.time():
                    enRoute = True

            if enRoute:
                printAtTime(package, "en route - truck 2.")
            else:
                printAtTime(package, "at the hub.")


# function printAllPackagesAtTime receives the package hash table and prints all packages with the status based on chosen time.
def printAllPackagesAtTime(table):
    print("\nEnter a time between 8:00 and 18:00")
    hour = 0
    minute = 0
    # while-loop continues until user enters an integer between 8 and 18 for the Hour.
    while True:
        try:
            hour = int(input("Hour: "))
        # ValueError occurs if a non integer is entered.
        except ValueError:
            print("Sorry, you entered an incorrect value. Try again.")
            continue
        # asks user to try again if integer is not between 8 and 18.
        if (hour < 8) or (hour > 18):
            print("incorrect Time. Try again.")
            continue
        else:
            break
    # while-loop continues until user enters an integer between 0 and 60 for the Minute.
    while True:
        try:
            minute = int(input("Minute: "))
        # ValueError occurs if a non integer is entered.
        except ValueError:
            print("Sorry, you entered an incorrect value. Try again.")
            continue
        # asks user to try again if integer is not between 0 and 60.
        if (minute < 0) or (minute >= 60) or (minute is None):
            print("incorrect Time. Try again.")
            continue
        else:
            break

    strMin = str(minute)
    # adds a 0 to the front of the string minute if it's less than 10. This makes the following print statement proper.
    if minute < 10:
        strMin = '0%s' % minute

    print("                    -----------------ALL PACKAGES AS OF %s:%s----------------------" % (hour, strMin))
    print('')
    # if-else-statements add 1 minute to the user chosen time for better comparison.
    if minute < 59:
        minute += 1
    else:
        minute = 0
        hour += 1
    # userTime is the user entered time.
    userTime = datetime.datetime(100, 1, 1, hour, minute, 0)
    pID = 1
    # while-loop continues through all 40 packages until all are printed.
    while pID <= 40:
        # gets the current package.
        package = table.search(pID)
        #  if-statement prints the package as delivered if its delivered time is before the user selected time.
        if package.timeDelivered < userTime.time():
            print(package)
        # else-statement prints the package as either en route or at the hub.
        else:
            correctBucket = False
            # inT1 and inT2 are set to True if the package is in truck 1 or in truck 2.
            inT1 = False
            inT2 = False
            bucket = 0
            # while-loop continues until the correct truck and truck route are found.
            while not correctBucket:
                # gets the current truck route for truck 1 and 2.
                truckLoadT1 = truck1[bucket]
                truckLoadT2 = truck2[bucket]
                # for-loop searches all packages in the route to see if the chosen package is present.
                # if so, the truck and route number is identified for the chosen package.
                for p in truckLoadT1:
                    if pID == int(p.ID):
                        correctBucket = True
                        inT1 = True
                        break

                # for-loop searches all packages in the route to see if the chosen package is present.
                # if so, the truck and route number is identified for the chosen package.
                for p in truckLoadT2:
                    if pID == int(p.ID):
                        correctBucket = True
                        inT2 = True
                        break
                # if-statement executes if the package is not found in the current route. Thus, the next route is checked.
                if not correctBucket:
                    bucket += 1
            # if the package is in truck 1, then checks if its en route or at the hub.
            if inT1:
                # gets the current route for truck 1.
                truckLoad = truck1[bucket]
                enRoute = False
                # checks if the package is en route by checking if any of the packages in the current route are delivered.
                for p in truckLoad:
                    if p.timeDelivered < userTime.time():
                        enRoute = True
                if enRoute:
                    printAtTime(package, "en route - truck 1.")
                else:
                    printAtTime(package, "at the hub.")

            # if the package is in truck 2, then checks if its en route or at the hub.
            if inT2:
                # gets the current route for truck 2.
                truckLoad = truck2[bucket]
                enRoute = False
                # checks if the package is en route by checking if any of the packages in the current route are delivered.
                for p in truckLoad:
                    if p.timeDelivered < userTime.time():
                        enRoute = True
                if enRoute:
                    printAtTime(package, "en route - truck 2.")
                else:
                    printAtTime(package, "at the hub.")

        pID += 1
