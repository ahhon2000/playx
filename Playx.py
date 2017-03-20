from subprocess import call
import os
import re
from os.path import samefile

def hasFile(cand, f):
	"""Return True iff file f is on list cand

	Absolute path is used for comparison, while f may be relative or abs.
	"""

	for ff in cand:
		if samefile(f, ff): return True

	return False

class Playx:
	def __init__(self, configFile, args):
		vardic = {}
		exec(open(configFile).read(), vardic)

		self.playerArgs = []

		args2 = []
		for a in args:
			if a[0] == '-': self.playerArgs += [a]
			else: args2 += [a]

		self.player = vardic['player']
		dirList = vardic['dirList']
		self.dirList = dirList
		self.fname = ""
		self.request = args2

		if 'extensions' in vardic.keys():
			self.extensions = vardic['extensions']
		else:
			self.extensions = []

		cand = []  # file candidates
		home = os.path.abspath(os.getenv("HOME"))
		for d0 in dirList:
			if os.path.abspath(d0) == home: continue

			for p, ds, fs in os.walk(d0):
				for f in fs:
					fp = "%s/%s" % (p, f)
					if self.isShortName(fp)  and\
					not hasFile(cand, fp):
						cand += [fp]
				
		if len(cand) == 0:
			fname = ""
		elif len(cand) == 1:
			fname = cand[0]
		else:
			cand.sort()
			flgMatched = False
			errMsg = ""
			while True:
				for i in range(len(cand)):
					print("%-4d%s" % (i+1, cand[i]))

				if errMsg: print("*** %s" % errMsg)
				print("\nwhich file do you want to apply `%s' to?" % self.player)
				try:
					s = input("> ")
					i = int(s) - 1
					flgMatched = True
				except EOFError:
					raise Exception("user aborted")
					break
				except:
					flgMatched = False
					errMsg = "wrong index"

				if flgMatched:
					fname = cand[i]
					break

		self.fname = fname


	def play(self):
		#cid = os.fork()
		fname = self.fname

		if not fname: raise Exception("no file matches `%s'" % self.request)

		#if not cid:
		cmd = [self.player] + self.playerArgs + [fname]
		rc = call(cmd)


	def isShortName(self, fname):
		# return True iff request is a short name of file fname
		
		f = fname.lower().strip()
		if os.path.isfile(fname)  and  '.' in f:
			ext = re.sub(r'^.*[.]([a-z0-9]+)$', r'\1', f)
			if ext not in self.extensions:
				return False

		req = self.request
		for s in req:
			s = s.strip().lower()
			if s not in f: return False

			i0 = f.index(s) + len(s)
			f = f[i0:]

		return True
