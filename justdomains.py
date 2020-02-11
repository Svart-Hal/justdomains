#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__	=	"Jason Brown"
__email__	=	"jason.brown@svarthal.io"
__version__	=	"0.2"
__license__	=	"Apache"
__date__	=	"20200211"


import urllib.request
from os import chown
from os import chmod
from os import system
from os import remove
from shutil import move
import subprocess
from datetime import datetime


def main():
	'''
        Write the header file
	'''

	dnstime = datetime.today().strftime('%y%m%d%H%M')

	header = open('header.txt', 'w')
	header.write('$TTL 30 \n@ IN SOA rpz.justdomains.svarthal.net. hostmaster.svarthal.net. '+dnstime+' 300 1800 604800 30\n NS localhost.\n\n\n')
	header.close()

	'''
		Fetch new malware file and write it to disk
	'''

	justdomains = urllib.request.urlopen('https://mirror1.malwaredomains.com/files/justdomains')
	with open ('justdomains.txt', 'b+w') as malware:
		malware.write(justdomains.read())

	add_cname = '\t CNAME \t.'

	with open ('justdomains.txt', 'r') as cname:
		append_lines = [''.join([x.strip(), add_cname, '\n']) for x in cname.readlines()]

	with open('justdomains.txt', 'w') as append:
		append.writelines(append_lines)
	append.close()

	'''
		Open files and write to disk
	'''

	with open('header.txt', 'r') as header, open('justdomains.txt', 'r') as justdomains, open('db.justdomains', 'w') as dbfile:
		dbfile.write(header.read() + justdomains.read().strip())
	dbfile.close()

	remove('header.txt')
	remove('justdomains.txt')

	chown('db.justdomains', 0, 115)
	chmod('db.justdomains', 0o644)
	move('db.justdomains', '/etc/bind/db.justdomains')

if __name__ == '__main__':
	main()