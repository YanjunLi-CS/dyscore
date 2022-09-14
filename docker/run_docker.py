#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
run_docker.py: 
"""

import pathlib
import signal
import docker
import argparse
from docker import types

mounts = []
command_args = []


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rec_file', required=True, help='The PDB file name of the receptor.')
    parser.add_argument('--lig_dir', required=True, help='The ligand directory.')
    parser.add_argument('--out_dir', required=True, help='The output directory.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--ref_file', default=None, help='THe reference ligand file')
    group.add_argument('--box', default='', help='min_x,min_y,min_z,max_x,max_y,max_z:'
                                                   'Coordination of the box for ligand binding site.')
    group.add_argument('--detect', action='store_true')

    parser.add_argument('--no_dock', action='store_true', help='Not run docking for the input molecules')
    parser.add_argument('--mf', action='store_true', help='Use molecular fingerprint model DyScore-MF')
    parser.add_argument('-w', '--weight_dir', required=True, help='The directory storing the model weights.')
    args = parser.parse_args()
    return args


_ROOT_MOUNT_DIRECTORY = '/mnt/'


def _create_mount(mount_name: str, path: str, read_only: bool=True):
    """Create a mount point for each file and directory used by the model."""
    path = pathlib.Path(path).absolute()
    target_path = pathlib.Path(_ROOT_MOUNT_DIRECTORY, mount_name)

    if path.is_dir():
        source_path = path
        mounted_path = target_path
    else:
        source_path = path.parent
        mounted_path = pathlib.Path(target_path, path.name)

    if not source_path.exists():
        raise ValueError(f'Failed to find source directory "{source_path}" to '
                         'mount in Docker container.')
    print('Mounting %s -> %s', source_path, target_path)
    mount = types.Mount(target=str(target_path), source=str(source_path),
                      type='bind', read_only=read_only)
    return mount, str(mounted_path)


def main():
    args = get_arguments()

    # Add signal handler to ensure CTRL+C also stops the running container.
    signal.signal(signal.SIGINT,
                  lambda unused_sig, unused_frame: container.kill())

    dyscore_path = pathlib.Path(__file__).parent.parent
    weight_path = pathlib.Path(args.weight_dir)
    if dyscore_path == weight_path or dyscore_path in weight_path.parents:
        raise ValueError(
            f'The download directory {args.weight_path} should not be a subdirectory '
            f'in the DyScore repository directory. If it is, the Docker build is '
            f'slow since the large databases are copied during the image creation.')

    # Mount path of receptor file
    mount, mounted_rec_file = _create_mount(f'rec_path', args.rec_file)
    mounts.append(mount)

    if args.ref_file:
        # Mount path of reference file
        mount, mounted_ref_path = _create_mount(f'ref_path', args.ref_file)
        mounts.append(mount)
        command_args.extend(['--ref',  f'{mounted_ref_path}'])

    # Mount path of ligand path
    mount, mounted_lig_path = _create_mount(f'lig_path', args.lig_dir)
    mounts.append(mount)

    # Mount path of output
    mount, mounted_output_path = _create_mount(f'output_path', args.out_dir, read_only=False)
    mounts.append(mount)

    # Mount path of model weights
    mount, mounted_weight_path = _create_mount(f'weight_path', args.weight_dir)
    mounts.append(mount)

    command_args.extend(['--rec', f'{mounted_rec_file}'])
    command_args.extend(['--lig', f'{mounted_lig_path}'])
    command_args.extend(['--box', f'{args.box}'])
    command_args.extend(['--out', f'{mounted_output_path}'])
    command_args.extend(['--weight', f'{mounted_weight_path}'])

    detect_flag = 'true' if args.detect else 'false'
    command_args.extend(['--detect', f'{detect_flag}'])

    dock_flag = 'false' if args.no_dock else 'true'
    command_args.extend(['--dock', f'{dock_flag}'])

    mf_flag = 'true' if args.mf else 'false'
    command_args.extend(['--mf', f'{mf_flag}'])
    print('run_dyscore', f' '.join(command_args))

    client = docker.from_env()
    container = client.containers.run(
        image='dyscore',
        command=command_args,
        remove=True,
        detach=True,
        mounts=mounts,
        user='dyscore-user')

    for line in container.logs(stream=True):
        print(line.strip().decode('utf-8'))


if __name__ == '__main__':
    main()
