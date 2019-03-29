'''
This program is run on the desktop.

It starts the compute server that waits
for the roborio to send a path to be generated
'''

from networktables import NetworkTables
from remote_path import RemotePath

NetworkTables.initialize(server="10.65.17.2")
RemotePath().start_compute_server()