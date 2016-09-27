# Personal homepage grading

Grading script for the [personal homepage assignment](https://docs.google.com/document/d/1ZwtuYi0_lizxj2xwxICOrXXUa22ow7nUQ1GMr-uW4DU/edit). This is intended for staff.

1. Download the [class survey data](https://docs.google.com/spreadsheets/d/1aQkPiTDqfxBtZDBCWAkU7Sizlf_KLoMEzJkbwhXBgjo/edit#gid=209566137).
    * `File`->`Download as`->`Comma-separated values`
    * This file is used to map GitHub usernames to Cornell NetIDs.
1. From this directory, run:

    ```bash
    mv <path/to/responses>.csv ResponseForm.csv
    # remove the header row
    # http://stackoverflow.com/a/27099557/358804
    sed -i '1d' ResponseForm.csv
    python2 grader.py
    ```

1. View the results in `homepage_grade.csv`.
