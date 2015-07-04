# File: B (Python 2.2)

from PandaModules import *
import whrandom
OFF = 0
FLYING = 1
LANDED = 2
states = {
    OFF: 'off',
    FLYING: 'Flying',
    LANDED: 'Landed' }
NUM_BUTTERFLIES = (6, 36, 5)
NUM_BUTTERFLY_AREAS = (4, 1, 4)
BUTTERFLY_SPEED = 2.0
BUTTERFLY_HEIGHT = (2.2000000000000002, 3.2000000000000002, 2.2000000000000002)
BUTTERFLY_TAKEOFF = (1.3999999999999999, 1.8, 1.3999999999999999)
BUTTERFLY_LANDING = (1.3999999999999999, 1.8, 1.3999999999999999)
MAX_LANDED_TIME = 20.0
TTC = 0
DG = 1
ESTATE = 2
ButterflyPoints = [
    [
        (Point3(84.0, -116.0, 3.5), Point3(95.0, -144.0, 2.6000000000000001), Point3(94.0, -145.0, 2.6000000000000001), Point3(95.0, -149.0, 2.6000000000000001), Point3(50.0, -155.0, 2.6000000000000001), Point3(51.0, -147.0, 2.6000000000000001), Point3(51.0, -145.0, 2.6000000000000001), Point3(14.0, -99.0, 3.1000000000000001), Point3(17.0, -94.0, 3.1000000000000001), Point3(50.0, -79.0, 3.1000000000000001), Point3(47.0, -86.0, 3.1000000000000001), Point3(54.0, -127.0, 2.6000000000000001), Point3(84.0, -113.0, 3.7999999999999998)),
        (Point3(-57.0, -70.0, 0.10000000000000001), Point3(-55.0, -68.0, 0.10000000000000001), Point3(-90.0, -77.0, 0.59999999999999998), Point3(-90.0, -72.0, 0.10000000000000001), Point3(-133.0, -50.0, 0.59999999999999998), Point3(-129.0, -48.0, 0.59999999999999998), Point3(-127.0, -25.0, 0.10000000000000001), Point3(-125.0, -22.0, 0.10000000000000001), Point3(-123.0, -22.0, 0.10000000000000001), Point3(-103.0, -10.0, -3.0), Point3(-104.0, -13.0, -2.5), Point3(-100.0, -28.0, -2.7000000000000002), Point3(-89.0, -41.0, -4.4000000000000004), Point3(-58.0, -34.0, -4.0999999999999996), Point3(-69.0, -18.0, -1.8999999999999999), Point3(-65.0, -19.0, -1.8999999999999999), Point3(-65.0, -16.0, -1.8999999999999999), Point3(6.0, -49.0, -0.10000000000000001), Point3(2.6000000000000001, -47.0, 0.10000000000000001), Point3(-33.600000000000001, -43.0, 0.0)),
        (Point3(-53.0, 3.0, -1.8), Point3(-58.0, 2.0, -1.8), Point3(-58.0, 2.0, -1.8), Point3(-76.0, 2.0, -1.8), Point3(-69.0, 11.0, -1.8), Point3(-100.0, 14.0, -4.0999999999999996), Point3(-104.0, 17.0, -2.6000000000000001), Point3(-125.0, 34.0, 0.10000000000000001), Point3(-124.0, 30.0, 0.10000000000000001), Point3(-113.0, 73.0, 0.59999999999999998), Point3(-33.0, 78.0, 0.10000000000000001), Point3(-65.0, 48.0, -3.0), Point3(-51.0, 33.0, -3.0), Point3(-30.0, 71.0, 0.10000000000000001), Point3(-26.0, 71.0, 0.10000000000000001), Point3(-23.0, 69.0, 0.10000000000000001), Point3(-23.0, 64.0, 0.10000000000000001), Point3(-5.0, 42.0, 0.10000000000000001), Point3(-22.0, 22.0, 0.10000000000000001), Point3(-27.0, 22.0, 0.10000000000000001)),
        (Point3(14.0, 93.0, 3.1000000000000001), Point3(17.0, 93.0, 3.1000000000000001), Point3(20.0, 122.0, 2.6000000000000001), Point3(21.0, 127.0, 2.6000000000000001), Point3(23.0, 123.0, 2.6000000000000001), Point3(32.0, 130.0, 2.6000000000000001), Point3(48.0, 148.0, 2.6000000000000001), Point3(64.0, 111.0, 2.6000000000000001), Point3(32.0, 82.0, 2.6000000000000001), Point3(63.0, 90.0, 3.1000000000000001), Point3(68.0, 85.0, 3.1000000000000001), Point3(65.0, 85.0, 3.1000000000000001), Point3(70.0, 95.0, 3.1000000000000001))],
    [
        (Point3(-7.9000000000000004, 22.899999999999999, 0.050000000000000003), Point3(-8.0, 17.0, 2.1000000000000001), Point3(-7.5, 18.0, 2.1000000000000001), Point3(-27.5, 70.700000000000003, 0.050000000000000003), Point3(-30.0, 70.0, 1.0), Point3(-31.0, 69.0, 1.0), Point3(-1.0, 53.0, 2.2000000000000002), Point3(-0.5, 53.0, 2.2000000000000002), Point3(35.0, 71.5, 1.0), Point3(33.0, 69.0, 0.050000000000000003), Point3(45.0, 61.0, 0.050000000000000003), Point3(55.0, 62.0, 0.050000000000000003), Point3(80.0, 74.0, 0.050000000000000003), Point3(80.0, 73.0, 0.050000000000000003), Point3(76.0, 46.0, 0.050000000000000003), Point3(76.0, 45.0, 0.050000000000000003), Point3(77.0, 41.0, 0.050000000000000003), Point3(62.0, 28.0, 0.050000000000000003), Point3(48.0, 24.0, 0.050000000000000003), Point3(83.0, 122.0, 0.050000000000000003), Point3(82.0, 123.0, 0.050000000000000003), Point3(81.0, 81.0, 0.050000000000000003), Point3(38.0, 77.0, 0.050000000000000003), Point3(-26.0, 69.0, 0.050000000000000003), Point3(-26.0, 70.0, 0.050000000000000003), Point3(-61.0, 71.0, 0.050000000000000003), Point3(-61.0, 70.0, 0.050000000000000003), Point3(-78.0, 79.0, 0.050000000000000003), Point3(-99.0, 106.0, 0.050000000000000003), Point3(-99.0, 108.0, 0.050000000000000003), Point3(-80.0, 123.0, 0.050000000000000003), Point3(-77.0, 125.0, 0.050000000000000003), Point3(-32.0, 162.0, 0.050000000000000003), Point3(-3.0, 186.5, 2.2000000000000002), Point3(-3.2000000000000002, 186.80000000000001, 2.2000000000000002), Point3(-1.0, 185.0, 2.2000000000000002), Point3(39.0, 165.0, 0.050000000000000003), Point3(42.0, 162.0, 0.050000000000000003), Point3(62.0, 145.0, 0.050000000000000003), Point3(64.0, 145.0, 0.050000000000000003), Point3(59.0, 102.0, 0.050000000000000003), Point3(32.700000000000003, 93.700000000000003, 0.050000000000000003), Point3(31.199999999999999, 90.799999999999997, 0.050000000000000003), Point3(29.800000000000001, 140.09999999999999, 0.050000000000000003), Point3(16.5, 146.30000000000001, 0.050000000000000003), Point3(15.300000000000001, 146.90000000000001, 0.050000000000000003), Point3(-24.300000000000001, 128.59999999999999, 0.050000000000000003), Point3(-67.900000000000006, 117.90000000000001, 0.050000000000000003), Point3(-41.600000000000001, 88.400000000000006, 0.050000000000000003), Point3(-13.6, 120.3, 0.050000000000000003), Point3(26.0, 117.8, 0.050000000000000003), Point3(22.600000000000001, 112.3, 0.050000000000000003), Point3(-8.1999999999999993, 107.90000000000001, 0.050000000000000003), Point3(-18.100000000000001, 97.0, 0.050000000000000003), Point3(-21.399999999999999, 92.900000000000006, 0.050000000000000003), Point3(-2.1000000000000001, 74.0, 0.050000000000000003), Point3(19.800000000000001, 93.5, 0.050000000000000003), Point3(21.399999999999999, 95.400000000000006, 0.050000000000000003), Point3(19.199999999999999, 97.5, 0.050000000000000003), Point3(-10.699999999999999, 143.30000000000001, 0.050000000000000003), Point3(38.200000000000003, 120.7, 0.050000000000000003), Point3(34.100000000000001, 101.5, 0.050000000000000003), Point3(32.399999999999999, 96.5, 0.050000000000000003), Point3(72.900000000000006, 121.8, 0.050000000000000003))],
    [
        (Point3(-40, -137, 0.025000000000000001), Point3(2.3500000000000001, -167.94999999999999, 0.025000000000000001), Point3(70.799999999999997, -125.3, 0.025000000000000001), Point3(63.490000000000002, -67.400000000000006, 0.025000000000000001), Point3(17.5, -59.25, 0.623), Point3(-51.869999999999997, -107.0, 0.72299999999999998), Point3(-20.324999999999999, -48.716000000000001, 4.8840000000000003), Point3(51.030000000000001, -67.244, 0.24399999999999999), Point3(20.02, -34.271000000000001, 7.1050000000000004), Point3(24.731000000000002, -20.905000000000001, 9.2469999999999999)),
        (Point3(88, -57.399999999999999, 0.025000000000000001), Point3(92.346999999999994, -7.71, 0.16900000000000001), Point3(129.38999999999999, 0.84999999999999998, 0.025000000000000001), Point3(121.14, 37, 0.025000000000000001), Point3(126, 30.300000000000001, 0.025000000000000001), Point3(100.3, 21.199999999999999, 0.050000000000000003), Point3(103.42, 1.544, 0.025000000000000001), Point3(82.370000000000005, -45, 0.025000000000000001), Point3(103.8, 4.306, 0.050000000000000003), Point3(119.19499999999999, -42.042000000000002, 0.025000000000000001)),
        (Point3(10, 98.5, -0.028000000000000001), Point3(11.65, 92.519999999999996, -0.079000000000000001), Point3(-16.25, 86.670000000000002, 0.216), Point3(-65.299999999999997, 67.799999999999997, 0.025000000000000001), Point3(-41.600000000000001, 67.0, 0.025000000000000001), Point3(-34.799999999999997, 68.900000000000006, 0.025000000000000001), Point3(-32.271999999999998, 56.649999999999999, 1.1919999999999999), Point3(-63.956000000000003, 39.677999999999997, 0.28100000000000003), Point3(-79.650000000000006, 36.990000000000002, 0.025000000000000001), Point3(-14.769, 72.399000000000001, 0.24399999999999999)),
        (Point3(-79.599999999999994, 36.899999999999999, 0.025000000000000001), Point3(-57.600000000000001, 27.239999999999998, 2.355), Point3(-69.641999999999996, -28.137, 3.98), Point3(-111, -58.100000000000001, 0.025000000000000001), Point3(-152.22300000000001, 25.626999999999999, 0.025000000000000001), Point3(-104.40000000000001, 43.5, 0.27800000000000002), Point3(-85.25, 10.513, 0.111), Point3(-43.600000000000001, 1.6439999999999999, 3.8380000000000001), Point3(-48.993000000000002, -21.968, 3.98), Point3(-30.088000000000001, -5.9870000000000001, 7.0250000000000004))]]
unusedIndexes = [
    [
        range(0, len(ButterflyPoints[TTC][0])),
        range(0, len(ButterflyPoints[TTC][1])),
        range(0, len(ButterflyPoints[TTC][2])),
        range(0, len(ButterflyPoints[TTC][3]))],
    [
        range(0, len(ButterflyPoints[DG][0]))],
    [
        range(0, len(ButterflyPoints[ESTATE][0])),
        range(0, len(ButterflyPoints[ESTATE][1])),
        range(0, len(ButterflyPoints[ESTATE][2])),
        range(0, len(ButterflyPoints[ESTATE][3]))]]
usedIndexes = [
    [
        [],
        [],
        [],
        []],
    [
        []],
    [
        [],
        [],
        [],
        []]]
estateIndexes = { }

def generateEstateIndices(avId):
    estateIndexes[avId] = ([
        range(0, len(ButterflyPoints[ESTATE][0])),
        range(0, len(ButterflyPoints[ESTATE][1])),
        range(0, len(ButterflyPoints[ESTATE][2])),
        range(0, len(ButterflyPoints[ESTATE][3]))], [
        [],
        [],
        [],
        []])


def clearEstateIndices(avId):
    if estateIndexes.has_key(avId):
        del estateIndexes[avId]
    


def getFirstRoute(playground, area, avId = None):
    (curPos, curIndex) = __getCurrentPos(playground, area, avId)
    (destPos, destIndex, time) = getNextPos(curPos, playground, area, avId)
    return (curPos, curIndex, destPos, destIndex, time)


def __getCurrentPos(playground, area, avId = None):
    if avId != None:
        if estateIndexes.has_key(avId):
            unusedI = estateIndexes[avId][0][area]
            usedI = estateIndexes[avId][1][area]
        else:
            return (ButterflyPoints[playground][area][0], 0)
    else:
        unusedI = unusedIndexes[playground][area]
        usedI = usedIndexes[playground][area]
    if len(unusedI) == 0:
        index = whrandom.choice(usedI)
        return (ButterflyPoints[playground][area][index], index)
    
    index = whrandom.choice(unusedI)
    unusedI.remove(index)
    usedI.append(index)
    return (ButterflyPoints[playground][area][index], index)


def getNextPos(currentPos, playground, area, avId = None):
    if avId != None:
        if estateIndexes.has_key(avId):
            unusedI = estateIndexes[avId][0][area]
            usedI = estateIndexes[avId][1][area]
        else:
            return (ButterflyPoints[playground][area][0], 0, 4.0)
    else:
        unusedI = unusedIndexes[playground][area]
        usedI = usedIndexes[playground][area]
    nextPos = currentPos
    while nextPos == currentPos:
        if len(unusedI) == 0:
            index = whrandom.choice(usedI)
            nextPos = ButterflyPoints[playground][area][index]
        else:
            index = whrandom.choice(unusedI)
            nextPos = ButterflyPoints[playground][area][index]
            if nextPos != currentPos:
                unusedI.remove(index)
                usedI.append(index)
            
    dist = Vec3(nextPos - currentPos).length()
    time = dist / BUTTERFLY_SPEED + BUTTERFLY_TAKEOFF[playground] + BUTTERFLY_LANDING[playground]
    return (nextPos, index, time)


def recycleIndex(index, playground, area, avId = None):
    if avId != None:
        if estateIndexes.has_key(avId):
            unusedI = estateIndexes[avId][0][area]
            usedI = estateIndexes[avId][1][area]
        else:
            return None
    else:
        unusedI = unusedIndexes[playground][area]
        usedI = usedIndexes[playground][area]
    if usedI.count(index) > 0:
        usedI.remove(index)
    
    if unusedI.count(index) == 0:
        unusedI.append(index)
    

