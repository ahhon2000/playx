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


		fname = ""
		dirList = self.dirList
		while True:
			files = []
			for d in dirList:
				lst = os.listdir(d)
				for f in lst:
					if self.isShortName(req, f):
						files += [d + "/" + f]


			if len(files) == 0:
				fname = ""
				break
			elif len(files) == 1:
				if os.path.isdir(fname):
					dirList = [fname]
					req = ""
					continue
				fname = files[0]

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


	def isShortName(self, sh, f):
		# return True iff string sh is a short name of file f

		sh = re.sub(r'[\s_]+', r' ', sh)
		f = re.sub(r'[\s_]+', r' ', f)

		sh = sh.lower()
		f = f.lower()

		if sh in f:
			return True
		else:
			return False
