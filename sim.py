from networktables import NetworkTables

enrty = "/recorder/start"
NetworkTables.startServer()

NetworkTables.getEntry(enrty).setBoolean(False)
while True:

    input('\npress enter to START recording\n')
    NetworkTables.getEntry(enrty).setBoolean(True)
    input('\npress enter to END recording\n')
    NetworkTables.getEntry(enrty).setBoolean(False)
