#!/usr/bin/python3

from netmiko import ConnectHandler
import re, sys, os, keyring

# This particular script is purely concerned with retrieving both the ARP and MAC address tables from the devices listed in devicesList.
# It uses the netmiko library in order to connect to the device.  https://pynet.twb-tech.com/blog/automation/netmiko.html
# Once it's got the data it writes into a folder called 'data', each in a seperate file named after the hostname of the device

class Operator:
    def __init__(self):
        pass

    def loadList(self):
        print("# Loading Device List")
        # Open the devicesList file that contains the IP and username to the devices that we're getting the data from
        self.devicesList = open('./devicesList', 'r')
        self.lines = self.devicesList.readlines()
        for self.line in self.lines:
            
            try:
                self.line = self.line.rstrip()
                self.type, self.ipAddress, self.username = self.line.split(",")
                # Retrieve password from keychain
                self.password = keyring.get_password("ipMacDumper", self.username)
                # Create new device object
                Device(self.type, self.ipAddress, self.username, self.password)
            except:
                pass
                
    def getEachEnvironment(self):
        print("# Getting Switch Data")
        for device in Device.devices:
            self.hostname, self.deviceArpTable, self.deviceMacTable = device.retrieveEnvironment()
            self.writeToFile(self.hostname, self.deviceArpTable, self.deviceMacTable)

    def writeToFile(self, hostname, arpTable, macTable):

        if os.path.exists('./data'):
            pass
        else:
            os.makedirs('./data')

        try:
            self.arpFilename = hostname + "-arp.log"
            self.arpFile = open('./data/' + self.arpFilename, 'w')
            for line in arpTable:
                self.arpFile.write(line + "\n")
            self.arpFile.close()
        except:
            print("Couldn't write Arp File ")

        try:
            self.macFilename = hostname + "-mac.log"
            self.macFile = open('./data/' + self.macFilename, 'w')
            for line in macTable:
                self.macFile.write(line + "\n")
            self.macFile.close()
        except:
            print("Couldn't write Mac File ")


class Device:

    devices = []

    def __init__(self, type, ipAddress, username, password):
        self.details = {'device_type': type,
                        'ip': ipAddress,
                        'username': username,
                        'password': password}
        self.arpTable = ""
        self.macAddressTable = ""

        self.devices.append(self)

    def retrieveEnvironment(self):

        try:
            self.connect = ConnectHandler(**self.details)
            if self.connect.find_prompt():
                self.hostname = self.connect.find_prompt().replace('#', '')
                self.arpTable = self.connect.send_command("show ip arp")
                self.arpTable = self.arpTable.split("\n")
                self.macAddressTable = self.connect.send_command("show mac address-table")
                self.macAddressTable = self.macAddressTable.split("\n")

            else:
                print("We don't have a prompt on " + self.details['ip'])

            self.connect.disconnect()

            return self.hostname, self.arpTable, self.macAddressTable
        except:
            print("Something went wrong while connecting to " + self.details['ip'])
            sys.exit()


admin = Operator()
admin.loadList()
admin.getEachEnvironment()
