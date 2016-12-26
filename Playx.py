from subprocess import call
import os
import re

class Playx:
	def __init__(self, configFile, args):
		vardic = {}
		exec(open(configFile).read(), vardic)

		self.playerArgs = []

		args2 = []
		for a in args:
			if a[0] == '-': self.playerArgs += [a]
			else: args2 += [a]

		req = " ".join(args2)

		self.player = vardic['player']
		dirList = vardic['dirList']
		self.dirList = dirList
		self.fname = ""
		self.request = req

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
					if self.isShortName(req, fp):
						cand += [fp]
				
		if len(cand) == 0:
			fname = ""
		elif len(cand) == 1:
			fname = cand[0]
		else:
			flgMatched = False
			errMsg = ""
			while True:
				for i in range(len(cand)):
					print("%-4d%s" % (i, cand[i]))

				if errMsg: print("*** %s" % errMsg)
				print("\nwhich file do you want to apply `%s' to?" % self.player)
				try:
					s = input("> ")
					i = int(s)
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


	def isShortName(self, sh, fname):
		# return True iff string sh is a short name of file fname

		sh = re.sub(r'[\s_]+', r' ', sh)
		f = re.sub(r'[\s_]+', r' ', fname)
		
		sh = sh.lower().strip()
		f = f.lower().strip()

		if os.path.isfile(fname) and re.search(r'[.]', f):
			ext = re.sub(r'^.*[.]([a-z0-9]+)$', r'\1', f)
			if ext not in self.extensions:
				return False

		if sh in f:
			return True
		else:
			return False
