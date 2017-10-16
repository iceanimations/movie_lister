import argparse
import os
import sys
import csv
import time
import collections
import subprocess
import json


DEFAULT_EXTS = [".mov", ".avi", ".mp4", ".mpeg", ".mkv"]

MovieFileInfo = collections.namedtuple(
        "MovieFileInfo", ['name', 'mtime', 'size', 'duration'])


def get_movie_data(movie_file):
    try:
        subprocess.check_output
        stdout = subprocess.check_output(
                ['ffprobe', '-v', 'quiet', '-print_format', 'json',
                 '-show_format', movie_file], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        raise

    data = json.loads(stdout)
    return data


def list_movies(directory=None, output=None):

    if directory is None:
        directory = os.path.abspath('.')

    if output is None:
        output = os.path.join(os.path.abspath('.'), 'movie_info.csv')
        print output

    name, ext = os.path.splitext(output)
    output = ''.join([name, '.csv'])

    if os.path.exists(output):
        count = 1
        while os.path.exists(output):
            output = '.'.join([name+'_%d' % count, '.csv'])
            count += 1

    output = open(output, 'w+')

    directory = os.path.normpath(directory)

    stdout_writer = csv.writer(sys.stdout)
    writer = csv.writer(output)
    for _file in os.listdir(directory):
        basename, ext = os.path.splitext(_file)
        if ext.lower() in DEFAULT_EXTS:
            full_path = os.path.join(directory, _file)
            stat = os.stat(full_path)
            mtime = time.asctime(time.localtime(stat.st_mtime))
            size = stat.st_size
            try:
                duration = get_movie_data(full_path)["format"]["duration"]
            except subprocess.CalledProcessError:
                duration = 'ERROR Fetching Info'
            info = MovieFileInfo(full_path, mtime, size, duration)
            stdout_writer.writerow(info)
            writer.writerow(info)

    output.close()


def build_parser():
    parser = argparse.ArgumentParser(
            description="Lists movie files and their details")
    parser.add_argument('-d', '--dir', dest="directory",
                        help="The directory to read from")
    parser.add_argument('-o', '--output', dest="output",
                        help="The output should go to this (CSV) file")
    return parser


def main():
    args = build_parser().parse_args()
    list_movies(args.directory, args.output)

if __name__ == "__main__":
    main()
