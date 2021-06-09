# CheckDate
Command line program (python3 argparse) that list files modified after a given date.

## Installing
Download the script `CheckDate.py` ;

Make it executable : 

```bash
$ chmod +x CheckDate.py
```

If your are on Linux, you can copy that script to the `/bin` folder to be able to run it from anywhere :
```bash
$ sudo cp CheckDate.py /bin/CheckDate
```

## Usage
```
$./CheckDate.py -h
usage: CheckDate [-h] [-v] [-hr HOUR] [-m MINUTE] [-sec SECOND] [-ms MICROSECOND] [-p PATH] [-e EXTENSION]
                 [-x EXCLUDE] [-s] [-d] [-r] [-S]
                 date

List files modified after a given date.

positional arguments:
  date                  Date of the format dd/mm/yyyy or yyyy/mm/dd or dd.mm.yyyy or yyyy.mm.dd

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show CheckDate version and exit
  -hr HOUR, --hour HOUR
                        Precise the hour with the date. Use 24h format. Default is 0.
  -m MINUTE, --minute MINUTE
                        Precise the minute with the date. Default is 0.
  -sec SECOND, --second SECOND
                        Precise the seconds with the date. Default is 0.
  -ms MICROSECOND, --microsecond MICROSECOND
                        Precise the microseconds with the date. Default is 0.
  -p PATH, --path PATH  Path where to search. If not provided, search in current (".").
  -e EXTENSION, --extension EXTENSION
                        Format of the filenames extensions. Read only in the files with one of these extensions. ","
                        (comma, without spaces) between them.
  -x EXCLUDE, --exclude EXCLUDE
                        Patterns to exclude. "," (comma, without spaces) between them.
  -s, --sorted          Sort the files by last modification date, older first. Reverse order with `-r` flag.
  -d, --show_last_modification
                        Show last modification date along file names.
  -r, --reverse         Used with `-s` flag : reverse the list order.
  -S, --silent          Hide errors.

Examples :
        CheckDate 09/06/2021
        CheckDate 2021.06.09 -hr 15 -m 43 -e .py,.txt
        CheckDate 09.06.2021 -x .pyc -s
```
