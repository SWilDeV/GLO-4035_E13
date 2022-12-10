import csv
import geopy.distance

if __name__ == '__main__':
    dataBrut = []
    dataPairs = []
    pairMatch = []
    idGroups = []
    with open("dataV4.csv", 'r') as csvFile:
        dataReader = csv.reader(csvFile)
        for row in dataReader:
            dataBrut.append([row[1], row[3], row[4], row[5]])
        dataBrutSorted = sorted(dataBrut, key=lambda x: int(x[0]))
        for i in range(len(dataBrutSorted) - 1):
            if dataBrutSorted[i][0] == dataBrutSorted[i+1][0]:
                dataPairs.append([dataBrutSorted[i][0], dataBrutSorted[i][3], dataBrutSorted[i][1], dataBrutSorted[i][2], dataBrutSorted[i+1][1], dataBrutSorted[i+1][2]])
        found = []
        for row in dataPairs:
            if row[0] not in found:
                newLine = []
                newLine.append(row[0])
                found.append(row[0])
                for otherRow in dataPairs:
                    if otherRow[0] not in found:
                        coord1Start = (row[2], row[3])
                        coord1End = (row[4], row[5])
                        coord2Start = (otherRow[2], otherRow[3])
                        coord2End = (otherRow[4], otherRow[5])
                        if geopy.distance.geodesic(coord1Start, coord2Start).m < 100 or geopy.distance.geodesic(coord1Start, coord2End).m < 100 or geopy.distance.geodesic(coord1End, coord2Start).m < 100 or geopy.distance.geodesic(coord1End, coord2End).m < 100:
                            found.append(otherRow[0])
                            newLine.append(otherRow[0])
                idGroups.append(newLine)
        for row in idGroups:
            print(row)
    with open("intersectionV4.scv", 'w') as csvFile:
        dataWriter = csv.writer(csvFile)
