import platform
import json
import lz4.block
from pathlib import Path

"""
This program lists your open Firefox tabs. It does not require Firefox
to be running, as it looks in the session backup. It looks in all of your
profiles.
"""


def cli():
    # the recovery file is in the Firefox profile, the location of which can
    # vary with OS and installation method; these lists may not be complete;
    # no idea if this will work in Windows
    locations = {
        'Linux': ['.mozilla/firefox/', 'snap/firefox/common/.mozilla/firefox'],
        'Darwin': ['Library/Application Support/Firefox/Profiles'],
        'Windows': ['\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles']
    }

    # look at all profiles
    recoveries = [
        recovery for sublist in [
            (Path.home() / folder).rglob(
                'sessionstore-backups/recovery.js*'
            ) for folder in locations[platform.system()]
        ] for recovery in sublist
    ]

    # method from https://unix.stackexchange.com/a/389360
    # and suffix nuance from https://unix.stackexchange.com/a/385026
    for recovery in recoveries:
        with open(recovery, 'rb') as f:
            if recovery.suffix == '.jsonlz4':
                _ = f.read(8)  # magic
                data = json.loads(
                    lz4.block.decompress(f.read()).decode('utf-8')
                )
            else:
                data = json.load(f)

            for window in data['windows']:
                for tab in window['tabs']:
                    print(tab['entries'][int(tab['index']) - 1]['url'])
