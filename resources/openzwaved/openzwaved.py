# This file is part of Jeedom.
#
# Jeedom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Jeedom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
import sys
import argparse
import os
from ozwave import globals,server_utils,rest_server
try:
	from tornado.httpserver import HTTPServer
	from tornado.ioloop import IOLoop
except Exception as e:
	print(globals.MSG_CHECK_DEPENDENCY, 'error')
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

if not os.path.exists('/tmp/python-openzwave-eggs'):
	os.makedirs('/tmp/python-openzwave-eggs')
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-openzwave-eggs'

parser = argparse.ArgumentParser(description='Ozw Daemon for Jeedom plugin')
parser.add_argument("--device", help="Device", type=str)
parser.add_argument("--port", help="Port for OZW server", type=str)
parser.add_argument("--loglevel", help="Log Level for the daemon", type=str)
parser.add_argument("--config_folder", help="Read or Write", type=str)
parser.add_argument("--data_folder", help="Handle to read or write", type=str)
parser.add_argument("--pid", help="Value to write", type=str)
parser.add_argument("--callback", help="Value to write", type=str)
parser.add_argument("--apikey", help="Value to write", type=str)
parser.add_argument("--suppressRefresh", help="Value to write", type=str)
parser.add_argument("--disabledNodes", help="Value to write", type=str)
parser.add_argument("--cycle", help="Cycle to send event", type=str)
args = parser.parse_args()

if args.device:
	globals.device = args.device
if args.port:
	globals.port_server = args.port
if args.loglevel:
	globals.log_level = args.loglevel
if args.config_folder:
	globals.config_folder = args.config_folder
if args.data_folder:
	globals.data_folder = args.data_folder
if args.pid:
	globals.pidfile = args.pid
if args.callback:
	globals.callback = args.callback
if args.apikey:
	globals.apikey = args.apikey
if args.cycle:
	globals.cycle = float(args.cycle)
if args.suppressRefresh:
	globals.suppress_refresh = args.suppressRefresh
if args.disabledNodes:
	if args.disabledNodes != '':
		globals.disabled_nodes = [int(disabled_node_id) for disabled_node_id in args.disabledNodes.split(',')]

server_utils.start_server()
if __name__ == '__main__':
	server_utils.write_pid()
	try:
		http_server = HTTPServer(globals.app)
		http_server.listen(globals.port_server, address=globals.socket_host)
		IOLoop.instance().start()
	except Exception, ex:
		print "Fatal Error: %s" % str(ex)