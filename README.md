# release-stats

* Clone https://github.com/mozilla/releasewarrior.git
* Set `RELEASES_DIR` environment variable to the path to the releasewarrior checkout's `releases` directory
* Set `DATA_DIR` to the directory used to store the graph data
* Set `TC_CLIENT_ID` and `TC_ACCESS_TOKEN` for taskcluster auth, obtained from https://tools.taskcluster.net/auth/clients/
* `pip install -r requirements.txt`
* `python3 scripts/releasewarrior2graphdata.py`
