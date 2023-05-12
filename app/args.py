import argparse


# pylint: disable=line-too-long
parser = argparse.ArgumentParser(
    prog='',
    description='retrieve images and image metadata from jsonplaceholder albums'
)
parser.add_argument(
    '-a', '--albums',
    nargs='*',
    help='one or more albums to retrieve'
)
parser.add_argument(
    '-i', '--images',
    nargs='*',
    help='one or more images to retrieve'
)
parser.add_argument(
    '-r', '--regex',
    help='only retrieve images with titles matching the given regex'
)
parser.add_argument(
    '-s', '--save',
    action='store_true',
    help='save images to current directory or to directory specified by --out'
)
parser.add_argument(
    '-o', '--out',
    help='specify output directory'
)
parser.add_argument(
    '-q', '--quiet',
    action='store_true'
)


def cleanup_comma_seperated_args(args):
    """Accept comma seperated ints as well as space seperated"""
    for i, arg in enumerate(args):
        if arg and arg[-1] == ',':
            # raises ValueError
            args[i] = int(arg[:-1])
        else:
            args[i] = int(arg)
