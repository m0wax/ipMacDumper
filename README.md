# ipMacDumper

There are two main scripts involved here:

<b>getMyMacs.py</b> - This script loads in a bunch of devices from the devicesList and retrieves the relevant credentials from the Gnome Keychain.  It then SSH's into each one and grabs the ARP/MAC table and writes it to a file in a directory called 'Data' (you may have to create this).<br>
<b>nmapper.py</b> - This script loads all the MAC addresses in and checks to see if we've seen the MAC before on previous runs.  If it has then we do nothing.  If it hasn't, then it scans them (this functionality isn't quite there yet) but the logic should work.<br><br>
Download all these files into a folder and create a folder called 'data' beside them.  Grab the appropriate modules through PIP and everything should work.
