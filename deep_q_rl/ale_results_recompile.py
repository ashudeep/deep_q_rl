""" This script runs a pre-trained network with the game
visualization turned off.

Usage:

ale_run_watch.py NETWORK_PKL_FILE [ ROM ]

__author__ = "Ashudeep Singh"
__email__ = "ashudeep21@gmail.com"
"""
import subprocess
import sys

def main():
	parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-r', '--rom', dest="rom", default=DEFAULT_ROM,
                        help='ROM to run (default: %(default)s)')
    parser.add_argument('--nn_file', type=str, default=None,
                            help='Pickle file containing trained net.')
    parameters, unknown = parser.parse_known_args(args)
    run_test(parameters)

def run_test(parameters):
    command = ['./ale_run.py', '--glue-port', '4097', '--steps-per-epoch', '0',
               '--test-length', '10000', '--nn_file', parameters.nn_file]

    if len(sys.argv) > 2:
        command.extend(['--rom', parameters.rom])

    p1 = subprocess.Popen(command)
    
    p1.wait()

if __name__ == "__main__":
    main()
