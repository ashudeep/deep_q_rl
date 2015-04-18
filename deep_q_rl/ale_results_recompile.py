""" This script runs a pre-trained network with the game
visualization turned off.

Usage:

ale_run_watch.py NETWORK_PKL_FILE [ ROM ]
"""
'''
__author__ = "Ashudeep Singh"
__email__ = "ashudeep21@gmail.com"
'''

import subprocess
import sys, argparse

DEFAULT_ROM = 'breakout'
DEFAULT_EPOCHS = 1

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-r', '--rom', dest="rom", default=DEFAULT_ROM,
	help='ROM to run (default: %(default)s)')
parser.add_argument('--nn_file', type=str, default=None,
	help='Pickle file containing trained net.')

def main(args):
	parameters, unknown = parser.parse_known_args(args)
	run_test(parameters)

def run_test(parameters):
	if parameters.nn_file == None:
		print "Please provide the NETWORK_PKL_FILE"
		parser.print_help()
		exit(1)
	command = ['./ale_run.py', '--glue-port', '4097', '--steps-per-epoch', '0',
               '--nn_file', parameters.nn_file,
               '-e', DEFAULT_EPOCHS]

	command.extend(['--rom', parameters.rom])
	print command
	p1 = subprocess.Popen(command)
    
	p1.wait()

if __name__ == "__main__":
	main(sys.argv[1:])
