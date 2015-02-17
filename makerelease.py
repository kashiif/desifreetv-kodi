#!/usr/bin/env python
import os
import zipfile
import shutil

ADDON_NAME = 'DesiFreeTV'
ADDON_ID = 'plugin.video.desifreetv'
ADDON_VER = '0.1.0'


DIR_TEMP = 'tmp'
DIR_SRC = 'src'

def zipdir(path, zip_file):
    for root, dirs, files in os.walk(path):
        for file in files:
            path_for_zip_entry = os.path.relpath(os.path.join(root, file), os.path.join(path, '..'))
            # Second argument [optional] allows you to zip a directory from any working directory,
            # without getting the full absolute paths in the zip archive.
            zip_file.write(os.path.join(root, file), path_for_zip_entry)


def prepare_dir_to_zip():
    dest = os.path.join(DIR_TEMP, ADDON_ID)
    shutil.copytree(DIR_SRC, dest, ignore=shutil.ignore_patterns('*.pyc', '*.pyo', 'xbmcenv.py'))
    return dest

if __name__ == '__main__':

    # clean temp directory
    if os.path.exists(DIR_TEMP):
        shutil.rmtree(DIR_TEMP)

    dest = '.\\' + prepare_dir_to_zip() + os.sep
    print 'dest', dest

    zip_filename = '%s-%s.zip' % (ADDON_ID, ADDON_VER)

    zip_file = None
    try:
        zip_file = zipfile.ZipFile(zip_filename, 'w')
        zipdir(dest, zip_file)

    finally:
        zip_file.close()

    print '%s file created' % zip_filename
