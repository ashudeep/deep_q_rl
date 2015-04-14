#! /usr/bin/env python
"""This script launches all of the processes necessary to train a
deep Q-network on an ALE game.

All unrecognized command line arguments will be passed on to
rl_glue_ale_agent.py
"""
import subprocess
import sys
import os
import argparse

DEFAULT_BASE_ROM_PATH = "../roms/"
DEFAULT_ROM = 'breakout.bin'
DEFAULT_PORT = 4096
DEFAULT_STEPS_PER_EPOCH = 50000
DEFAULT_EPOCHS = 100
DEFAULT_STEPS_PER_TEST = 10000
DEFAULT_FRAME_SKIP = 4

def main(args):
    # Check for glue_port command line argument and set it up...
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom1', dest="rom1", default=DEFAULT_ROM,
                        help='ROM to run (default: %(default)s)')
    parser.add_argument('--rom2', dest="rom2", default=DEFAULT_ROM,
                        help='Second ROM to run (default: %(default)s)')
    parser.add_argument('--ratio', dest="steps_ratio", default=DEFAULT_STEPS_RATIO,
                        help='Default ratio of the steps from each games \
                        (default: %(default)s)')
    parser.add_argument('-e', '--epochs', dest="epochs", type=int,
                        default=DEFAULT_EPOCHS,
                        help='Number of training epochs (default: %(default)s)')
    parser.add_argument('-s', '--steps-per-epoch', dest="steps_per_epoch",
                        type=int, default=DEFAULT_STEPS_PER_EPOCH,
                        help='Number of steps per epoch (default: %(default)s)')
    parser.add_argument('-t', '--test-length', dest="test_steps",
                        type=int, default=DEFAULT_STEPS_PER_TEST,
                        help='Number of steps per test (default: %(default)s)')
    parser.add_argument('--merge', dest="merge_frames", default=False,
                        action="store_true",
                        help='Tell ALE to send the averaged frames')
    parser.add_argument('--display-screen', dest="display_screen", 
                        action='store_true', default=False,
                        help='Show the game screen.')
    parser.add_argument('--experiment-prefix', dest="experiment_prefix",
                        default=None,
                        help='Experiment name prefix '
                        '(default is the name of the game)')
    parser.add_argument('--frame-skip', dest="frame_skip",
                        default=DEFAULT_FRAME_SKIP, type=int,
                        help='Every how many frames to process '
                        '(default: %(default)s)')
    parser.add_argument('--glue-port', dest="glue_port", type=int,
                        default=DEFAULT_PORT,
                        help='rlglue port (default: %(default)s)')
    parameters, unknown = parser.parse_known_args(args)

    my_env = os.environ.copy()

    close_fds = True
    full_rom_paths=[]
    my_envs=[]
    p1=[]
    p2=[]
    for index, rom in enumerate([rom1, rom2]):
        if parameters.rom.endswith('.bin'):
            rom = parameters.rom
        else:
            rom = "%s.bin" % parameters.rom
        full_rom_paths.append(os.path.join(DEFAULT_BASE_ROM_PATH, rom))
        my_env = os.environ.copy()
        my_env["RLGLUE_PORT"] = str(parameters.glue_port)+index
        my_envs.append(my_env)
        # Start RLGLue
        p1.append(subprocess.Popen(['rl_glue'], env=my_env, close_fds=close_fds))

        # Start ALE
        command = ['../ale/ale', '-game_controller', 'rlglue', '-send_rgb', 'true',
               '-restricted_action_set', 'true', '-frame_skip',
                str(parameters.frame_skip)]
        if not parameters.merge_frames:
            command.extend(['-disable_color_averaging', 'true'])
        if parameters.display_screen:
            command.extend(['-display_screen', 'true'])
        command.append(full_rom_path)
        p2.append(subprocess.Popen(command, env=my_env, close_fds=close_fds))

    # Start RLGlue Experiment
    p3 = subprocess.Popen(['./rl_glue_ale_experiment.py', '--epoch_length',
                           str(parameters.steps_per_epoch),
                           '--test_length', str(parameters.test_steps),
                           '--num_epochs', str(parameters.epochs)],
                          env=my_env, close_fds=close_fds)

    # Start RLGlue Agent
    command = ['./rl_glue_ale_agent.py']
    if parameters.experiment_prefix:
        command.extend(['--exp_pref', parameters.experiment_prefix])
    p4 = subprocess.Popen(command + unknown, env=my_env, close_fds=close_fds)

    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
