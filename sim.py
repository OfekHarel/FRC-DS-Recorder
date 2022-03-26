from networktables import NetworkTables

enrty = "/recorder/start"
fms_entry = '/FMSInfo/MatchNumber'
NetworkTables.startServer()

count = 0
done = False
while True:
    NetworkTables.getEntry(fms_entry).setNumber(count)
    done = False
    NetworkTables.getEntry(enrty).setBoolean(False)

    input('press enter to start recording')

    NetworkTables.getEntry(enrty).setBoolean(True)
    print(NetworkTables.getEntry(enrty).getBoolean(False))

    while not done:
        if not NetworkTables.getEntry(enrty).getBoolean(False):
            done = True
            count += 1