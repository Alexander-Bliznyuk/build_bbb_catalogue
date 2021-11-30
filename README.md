This script generates a comprehensible catalogue of BigBlueButton recordings
storage. It categorizes the recordings by meeting id and by date. Such a
catalogue primarily serves ordinary non-technician users enabling them to
browse backups/archives. Maybe some technicians will find this script handy
too, because it's a simple solution to take a quick look at BigBlueButton
media storage contents.

<pre>
This script generates a comprehensible catalogue of BigBlueButton recordings
storage. It categorizes the recordings by meeting id and by date. Such a
catalogue primarily serves ordinary non-technician users enabling them to
browse backups/archives. Maybe some technicians will find this script handy
too, because it's a simple solution to take a quick look at BigBlueButton
media storage contents.

optional arguments:
  -h, --help            show this help message and exit
  --recordings-root RECORDINGS_ROOT
                        location of bbb storage; in server environment, it's usually /var/bigbluebutton/published;
                        this script will enter every presentation/<internal-meeting-id> subfolder;
                        defaults to current working directory
  --catalogue-dir CATALOGUE_DIR
                        where to save links to bbb recordings; defaults to current working directory
  --verbose             print errors

</pre>
