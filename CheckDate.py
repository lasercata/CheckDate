#!/bin/python3
# -*- coding: utf-8 -*-

'''This script allow you to list files modified after a certain date'''

auth = 'Lasercata'
last_update = '2021.06.09'
version = '1.0'


##-import
from os import system, walk, stat
from os import chdir, mkdir, getcwd
from os.path import exists, abspath

from datetime import datetime as dt

import argparse


##-ini
alf = 'abcdefghijklmnopqrstuvwxyz'


##-Useful function
def set_good_len(word, mx, opposite=False):
    '''return word formated to have length of mx'''
    
    while len(word) < mx:
        if opposite:
            word = ' ' + word
        
        else:
            word += ' '
    
    return word


##-main
class CheckDate:
    '''Class which help to list files modified after a certain date.'''
    
    def __init__(self, date, path='.', ext=[], exclude=[], hide_err=False):
        '''
        Initiate CheckDate.
        
        - date : the date in datetime.datetime format ;
        - path : The path where to search ;
        - ext : The list of extensions of the files (search only in these ones) ;
        - exclude : The list of filenames' patterns to exclude.
        '''
        
        if not exists(path):
            raise ValueError('CheckDate: Path "{}" not found'.format(path))
        
        elif True in [type(k) not in (list, tuple, set) for k in (ext, exclude)]:
            raise ValueError('`ext` and `exclude` should be lists, tuple, or sets, but different found (ext: {}, exclude: {})'.format(type(ext), type(exclude)))
        
        self.date = date
        self.date_str = str(date).replace(' ', ' at ')
        self.path = path
        self.ext = ext
        self.exclude = exclude
        self.hide_err = hide_err
        
    
    def check(self):
        '''Check if the last modification date is greater than the given date.'''

        ret = {} # Dict of the form : {'path/to/file1': last_m, ...}
    
        for r, d, f in walk(self.path): # root path str, directories list, files list
            for fn in f:
    
                if ((True in [fn[-len(k):] == k for k in self.ext]) or (self.ext == [])) and (True not in [k in fn for k in self.exclude]):
                    try:
                        last_m = dt.fromtimestamp(stat(r + '/' + fn).st_mtime)
                    
                    except Exception as err:
                        if not self.hide_err:
                            print('CheckDate: file "{}": {}'.format(fn, err))
    
                    if last_m > self.date:
                        ret[r + '/' + fn] = last_m
    
        return ret


    def gcheck(self, show_last_m=False, sorted_=True, reverse=True):
        '''
        Use self.check and print the result to stdout.
        
        - show_last_m : A bool indicating if show the last modification date for each file ;
        - sorted_ : A bool indicating if sort the files by last modification date ;
        - reverse : Used with stored_ to reverse the order of the list.
        '''
        
        d = self.check()
        
        if len(d) != 0 and show_last_m:
            mx = max(len(str(d[k])) for k in d) + 1
        
        elif show_last_m:
            mx = 0
        
        if sorted_:
            l = sorted(d, key=lambda n: d[n], reverse=reverse)
        else:
            l = list(d.keys())
        
        if len(d) == 0:
            print('No file modified after the {} in "{}"'.format(self.date_str, abspath(self.path)))
            return None #Stop.
        
        else:
            print('\nFiles modified after the {} :\n'.format(self.date_str))
        
        for fn in l:
            if not(show_last_m):
                print('\t' + fn)
            
            else:
                print('\t' + set_good_len(str(d[fn]), mx) + fn)
        
        print('')


##-Using interface
class Parser:
    '''Class which allow to use CheckDate in command-line.'''

    def __init__(self):
        '''Initiate Parser'''

        self.parser = argparse.ArgumentParser(
            prog='CheckDate',
            description='List files modified after a given date.',
            epilog='Examples :\n\tCheckDate 09/06/2021\n\tCheckDate 2021.06.09 -hr 15 -m 43 -e .py,.txt\n\tCheckDate 09.06.2021 -x .pyc -s',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        self.parser.add_argument(
            '-v', '--version',
            help='Show CheckDate version and exit',
            nargs=0,
            action=self.Version
        )

        self.parser.add_argument(
            'date',
            help='Date of the format dd/mm/yyyy or yyyy/mm/dd or dd.mm.yyyy or yyyy.mm.dd'
        )

        self.parser.add_argument(
            '-hr', '--hour',
            help='Precise the hour with the date. Use 24h format. Default is 0.'
        )

        self.parser.add_argument(
            '-m', '--minute',
            help='Precise the minute with the date. Default is 0.'
        )

        self.parser.add_argument(
            '-sec', '--second',
            help='Precise the seconds with the date. Default is 0.'
        )

        self.parser.add_argument(
            '-ms', '--microsecond',
            help='Precise the microseconds with the date. Default is 0.'
        )

        self.parser.add_argument(
            '-p', '--path',
            help='Path where to search. If not provided, search in current (".").'
        )

        self.parser.add_argument(
            '-e', '--extension',
            help='Format of the filenames extensions. Read only in the files with one of these extensions. "," (comma, without spaces) between them.'
        )

        self.parser.add_argument(
            '-x', '--exclude',
            help='Patterns to exclude. "," (comma, without spaces) between them.'
        )
        
        self.parser.add_argument(
            '-s', '--sorted',
            help='Sort the files by last modification date, older first. Reverse order with `-r` flag.',
            action='store_true'
        )

        self.parser.add_argument(
            '-d', '--show_last_modification',
            help='Show last modification date along file names.',
            action='store_true'
        )

        self.parser.add_argument(
            '-r', '--reverse',
            help='Used with `-s` flag : reverse the list order.',
            action='store_true'
        )

        self.parser.add_argument(
            '-S', '--silent',
            help='Hide errors.',
            action='store_true'
        )


    def parse(self):
        '''Parse the args'''

        #------Get arguments
        args = self.parser.parse_args()
        
        #---date
        if args.hour == None:
            h = 0
        else:
            h = args.hour

        if args.minute == None:
            m = 0
        else:
            m = args.minute

        if args.second == None:
            sec = 0
        else:
            sec = args.second

        if args.microsecond == None:
            ms = 0
        else:
            ms = args.microsecond
        
        date_ = args.date
        
        if len(date_) != 10 or ('/' not in date_ and '.' not in date_):
            print('CheckDate: The argument `date` should be of the format dd/mm/yyyy or yyyy/mm/dd or dd.mm.yyyy or yyyy.mm.dd !')
            self.parser.exit()
        
        d = date_.split(('.', '/')['/' in date_])
        
        if len(d[0]) == 2:
            day, month, year = d
        else:
            year, month, day = d
        
        try:
            date = dt(int(year), int(month), int(day), int(h), int(m), int(sec), int(ms))
        
        except ValueError as err:
            if 'invalid literal for int() with base 10:' in str(err):
                msg = 'Integers are required'
            
            else:
                msg = str(err)
                
            print('CheckDate: Wrong date: {}'.format(msg))
            self.parser.exit()


        #---ext, exclude, path
        if args.extension == None:
            ext = []
        else:
            ext = args.extension.split(',')
        
        if args.exclude == None:
            exclude = []
        else:
            exclude = args.exclude.split(',')
        
        path = (args.path, '.')[args.path == None]

        #------Search
        Checker = CheckDate(date, path, ext, exclude, args.silent)
        
        Checker.gcheck(args.show_last_modification, args.sorted, args.reverse)


    class Version(argparse.Action):
        '''Class used to show Synk version.'''

        def __call__(self, parser, namespace, values, option_string):

            print(f'CheckDate v{version}')
            parser.exit()




##-run
if __name__ == '__main__':
    app = Parser()
    app.parse()

