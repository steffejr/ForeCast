from BeautifulSoup import BeautifulSoup
import urllib2, time, getopt, sys

atotal = []

def get_data(url):
	try: v = urllib2.urlopen(url).read()
	except: return ''
	try: v = v.strip()
	except: return ''
	return v

def get_group(a200, atotal):
	s = '+'.join(a200)
	f = 'sn'
	url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (s, f)
	v = get_data(url)
	a = v.split("\r\n")
	for s in a:
		if s.find('N/A') == -1:
			aa = s.split('"')
			s = ''.join(aa)
			aa = s.split(',')
			try:
				if aa[1] != '':
					if aa[0] != aa[1]:
						atotal.append(s)
			except: continue

def get_symbols(a1, atotal, verbose):
	i = 0
	j = 0
	a200 = []
	for e in a1:
		try: a200.append(e)
		except: break
		i += 1
		if i == 200:
			j += 1
			if verbose:
				print j,
				sys.stdout.flush()
			get_group(a200, atotal)
			a200 = []
			i = 0
	get_group(a200, atotal)
	if verbose:
		print "\n" + `len(atotal)`
		sys.stdout.flush()

def get_1_character_symbols(verbose):
	global atotal
	a1 = []
	for i in range(65, 65+26):
		a1.append(chr(i))
	get_symbols(a1, atotal, verbose)

def get_2_character_symbols(verbose):
	global atotal
	a1 = []
	for i in range(65, 65+26):
		for j in range(65, 65+26):
			a1.append(chr(i)+chr(j))
	get_symbols(a1, atotal, verbose)

def get_3_character_symbols(verbose):
	global atotal
	a1 = []
	for i in range(65, 65+26):
		for j in range(65, 65+26):
			for k in range(65, 65+26):
				a1.append(chr(i)+chr(j)+chr(k))
	get_symbols(a1, atotal, verbose)

def get_4_character_symbols(verbose):
	global atotal
	a1 = []
	for i in range(65, 65+26):
		for j in range(65, 65+26):
			for k in range(65, 65+26):
				for l in range(65, 65+26):
					a1.append(chr(i)+chr(j)+chr(k)+chr(l))
	get_symbols(a1, atotal, verbose)

def get_5_character_symbols(verbose):
	global atotal
	a1 = []
	for i in range(65, 65+26):
		for j in range(65, 65+26):
			for k in range(65, 65+26):
				for l in range(65, 65+26):
					for m in range(65, 65+26):
						a1.append(chr(i)+chr(j)+chr(k)+chr(l)+chr(m))
	get_symbols(a1, atotal, verbose)

def help():
	print 'to retrieve all 1-character symbols:'
	print '\tpython get_yahoo_stock_symbols.py -v -c 1'
	print '\tyahoo_stock_symbols_1.txt = symbols, yahoo_stock_symbols_1.csv = symbols w/names'
	print 'to retrieve all 1 and 2-character symbols:'
	print '\tpython get_yahoo_stock_symbols.py -v -c 2'
	print '\tyahoo_stock_symbols_2.txt = symbols, yahoo_stock_symbols_2.csv = symbols w/names'
	print
	print '(likewise for 3 and 4)'
	print
	print 'to retrieve all 1, 2, 3, 4, and 5-character symbols (takes 2 hours w/broadband):'
	print '\tpython get_yahoo_stock_symbols.py -v -c 5'
	print '\tyahoo_stock_symbols_5.txt = symbols, yahoo_stock_symbols_5.csv = symbols w/names'
	print

def usage():
	print 'usage: python get_yahoo_stock_symbols.py "vhc:", ["help", "characters="]'

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "vhc:", ["help", "characters="])
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
	verbose = False
	characters = None
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			help()
			sys.exit()
		elif o in ("-c", "--characters"):
			characters = a
		else:
			assert False, "unhandled option"
	if verbose:
		print time.strftime("%m/%d/%Y %I:%M"),
		sys.stdout.flush()
	if characters == None:
		help()
		sys.exit()
	elif characters == '1':
		get_1_character_symbols(verbose)
	elif characters == '2':
		get_1_character_symbols(verbose)
		get_2_character_symbols(verbose)
	elif characters == '3':
		get_1_character_symbols(verbose)
		get_2_character_symbols(verbose)
		get_3_character_symbols(verbose)
	elif characters == '4':
		get_1_character_symbols(verbose)
		get_2_character_symbols(verbose)
		get_3_character_symbols(verbose)
		get_4_character_symbols(verbose)
	elif characters == '5':
		get_1_character_symbols(verbose)
		get_2_character_symbols(verbose)
		get_3_character_symbols(verbose)
		get_4_character_symbols(verbose)
		get_5_character_symbols(verbose)
	csv = 'yahoo_stock_symbols_%s.csv' % characters
	txt = 'yahoo_stock_symbols_%s.txt' % characters
	fcsv = open(csv, 'w')
	ftxt = open(txt, 'w')
	for s in atotal:
		fcsv.write(s+'\n')
		sym = s.split(',')[0]
		ftxt.write(sym+'\n')
	fcsv.close()
	ftxt.close()
	if verbose:
		print time.strftime("%m/%d/%Y %I:%M")
		sys.stdout.flush()

if __name__ == "__main__":
	main()

