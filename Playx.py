from subprocess import call
import os
import re

class Playx:
	def __init__(self, configFile, args):
		vardic = {}
		exec(open(configFile).read(), vardic)

		req = " ".join(args)

		self.player = vardic['player']
		self.dirList = vardic['dirList']
		self.fname = ""
		self.request = req

		if 'extensions' in vardic.keys():
			self.extensions = vardic['extensions']
		else:
			self.extensions = []


		fname = ""
		dirList = self.dirList
		while True:
			files = []
			for d in dirList:
				lst = os.listdir(d)
				for f in lst:
					fp = d + "/" + f
					if self.isShortName(req, fp):
						files += [fp]


			if len(files) == 0:
				fname = ""
				break
			elif len(files) == 1:
				if os.path.isdir(files[0]):
					dirList = [files[0]]
					req = ""
					continue
				fname = files[0]
				break

			flgMatched = False
			errMsg = ""
			while True:
				for i in range(0, len(files)):
					print("%-4d%s" % (i, files[i]))

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
					if os.path.isdir(files[i]):
						flgMatched = False
						dirList = [files[i]]
						req = ""
					else:
						fname = files[i]

					break

			if flgMatched: break

		self.fname = fname


	def play(self):
		cid = os.fork()
		fname = self.fname

		if not fname: raise Exception("no file matches `%s'" % self.request)

		if not cid:
			rc = call([self.player, fname])


	def isShortName(self, sh, fname):
		# return True iff string sh is a short name of file fname

		sh = re.sub(r'[\s_]+', r' ', sh)
		f = re.sub(r'[\s_]+', r' ', fname)
		
		sh = sh.lower()
		f = f.lower()

		if os.path.isfile(fname) and re.search(r'[.]', f):
			ext = re.sub(r'^.*[.]([a-z0-9]+)$', r'\1', f)
			if ext not in self.extensions:
				return False

		if sh in f:
			return True
		else:
			return False
