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
    # vary with OS and installation method
    # look at all profiles
    # if this rglob took too long, we could guess at the profile location
    recoveries = list(Path.home().rglob('sessionstore-backups/recovery.js*'))

    # method from https://unix.stackexchange.com/a/389360
    # and suffix nuance from https://unix.stackexchange.com/a/385026
    for recovery in recoveries:
        with open(recovery, "rb") as f:
            if recovery.suffix == '.jsonlz4':
                _ = f.read(8)  # magic
                data = json.loads(
                    lz4.block.decompress(f.read()).decode("utf-8")
                )
            else:
                data = json.load(f)

            for window in data["windows"]:
                for tab in window["tabs"]:
                    i = int(tab["index"]) - 1
                    url = tab["entries"][i]["url"]
                    print(url)
