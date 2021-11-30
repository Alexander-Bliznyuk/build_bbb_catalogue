#!/usr/bin/env python3

import argparse
import sys
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from os import path, symlink, readlink, scandir, getcwd, makedirs


def get_link_name_for_part_of_meeting(link_name: str) -> str:
    dest_dir = path.dirname(link_name)
    dest_basename = path.basename(link_name)
    part = 1
    while path.exists(link_name):
        part += 1
        link_name = '%s/%d_%s' % (dest_dir, part, dest_basename)

    return link_name


def mklink(src: str, link_name: str):
    if not path.exists(src):
        return

    resulting_link_name = link_name

    if path.exists(link_name):
        if readlink(link_name) == src:
            return
        resulting_link_name = get_link_name_for_part_of_meeting(link_name)

    symlink(src, resulting_link_name)


parser = argparse.ArgumentParser(description="This script generates a comprehensible catalogue of BigBlueButton "
                                             "recordings storage. It categorizes the recordings by meeting id and by "
                                             "date. Such a catalogue primarily serves ordinary non-technician users "
                                             "enabling them to browse backups/archives. Maybe some technicians will "
                                             "find this script handy too, because it's a simple solution to take a "
                                             "quick look at BigBlueButton media storage contents.")
parser.add_argument("--recordings-root",
                    help="location of bbb storage;\
                         in server environment, it's usually '/var/bigbluebutton/published';\
                         this script will enter every 'presentation/<internal-meeting-id>' subfolder;\
                         defaults to current working directory")
parser.add_argument("--catalogue-dir",
                    help="where to save links to bbb recordings; defaults to current working directory")
parser.add_argument("--verbose", help="print errors", action="store_true")
args = parser.parse_args()

recordings_root = args.recordings_root or getcwd()
recordings_dir = path.join(path.realpath(recordings_root), 'presentation')
catalogue_dir = path.realpath(args.catalogue_dir) if args.catalogue_dir else getcwd()

for recording_dir in scandir(recordings_dir):
    if not path.isdir(recording_dir.path):
        continue

    try:
        xml_root = ElementTree.parse(path.join(recording_dir.path, 'metadata.xml')).getroot()
    except FileNotFoundError:
        if args.verbose:
            print('no metadata.xml in ' + recording_dir.path, file=sys.stderr)
        continue

    meeting_id = xml_root.find('meta/meetingId').text
    meeting_date = datetime.fromtimestamp(float(xml_root.find('start_time').text) / 1000)

    descriptive_dir = path.join(catalogue_dir, 'by_code', meeting_id)
    path.isdir(descriptive_dir) or makedirs(descriptive_dir)

    date_dir = path.join(catalogue_dir, 'by_date', str(meeting_date.year), meeting_date.strftime('%m-%d'))
    path.isdir(date_dir) or makedirs(date_dir)

    mklink(
        path.join(recording_dir.path, 'video', 'webcams.webm'),
        path.join(descriptive_dir, meeting_date.strftime('%y-%m-%d.webm'))
    )

    mklink(
        path.join(recording_dir.path, 'video', 'webcams.webm'),
        path.join(date_dir, meeting_id + ".webm")
    )
