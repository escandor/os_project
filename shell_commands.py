# Student name: Alexandra Escandor
# ID: 17418156

from cmd import Cmd
from subprocess import *
import os
from threading import Thread

class MyShell(Cmd):

	shell = os.getcwd() + "/myshell"

	def default(self, args):
		# pid = os.fork()
		# if pid > 0:
		# 	wpid = os.waitpid(pid, 0)
		# else:
		try:
			args = args.split()
			if args[-1] == "&":
				Thread(target=self.multiprocess, args=(args[:-1],)).start()
			elif ">" in args or ">>" in args:
				self.io_redir2(args)
			else:
				call(args)
		except:
			print("Please enter a valid command")

	def multiprocess(self, args):
		call(args)

	def io_redir2(self, args):
		func = "w"
		if ">>" in args:
			func = "a"

		myoutput = open(args[-1], func)
		p = Popen(args[:2], stdout=myoutput, close_fds=True)
		out, err = p.communicate()

		if len(args) > 2:
			if os.path.isfile(args[1]) and os.path.isfile(args[2]):
				myoutput = open(args[-1], "a")
				p = Popen(args[:1] + args[2:-1], stdout=myoutput, close_fds=True)
				out, err = p.communicate()
		raise SystemExit

	def io_redir(self, output, args):
		args = args.split()
		func = "w"
		if ">>" in args:
			func = "a"

		if ">" in args or ">>" in args:
			with open(args[-1], func) as f:
				f.write(output)
		else:
			print(output)

	def do_cd(self, args):
		if len(args) > 0:
			try:
				os.chdir(args)
				os.environ["PWD"] = os.getcwd()
			except FileNotFoundError:
				print("File or directory \"{}\" does not exist".format(args))
		else:
			print("Current directory:", os.getcwd())
		self.myprompt()

	def do_clr(self, args):
		if len(args) > 0:
			print("Incorrect use of command")
		else:
			os.system("clear")

	def do_dir(self, args):
		try:
			directory = os.listdir()
			if len(args) > 0 and args[0] != ">":
				directory = os.listdir(args.split()[0])

			output = ""
			for file in directory:
				if file[0] != ".":
					if os.path.isdir(file):
						output += self.color_blue("(d) " + file + "\n")
					else:
						output += "(f) " + file + "\n"
			self.io_redir(output.strip(), args)

		except FileNotFoundError as e:
			print("No such directory: " + "".join(args))

	def do_environ(self, args):
		if len(args) == 0 or ">" == args[0]:
			output = ""
			for k, v in os.environ.items():
				output += self.color_red(k + ": \n") + v + "\n\n"
			self.io_redir(output.strip(), args)
		else:
			print("Incorrect use of command")

	def do_echo(self, args):
		output = " ".join(args.split())
		if ">" in args.split() or ">>" in args.split():
			self.io_redir(" ".join(output.split()[:-2]), args)
		else:
			print(output)

	def do_help(self, args):
		with open("readme", "r") as f:
			lines = [line for line in f.readlines()]

		for idx, line in enumerate(lines):
			if len(args) > 0:
				if line != "\n" and args == line.split()[0]:
			 		print(line.strip())
			else:
				if idx % 20 == 0 and idx != 0:
					input("Press ENTER for more...")
				print(line.strip())

	def do_pause(self, args):
		if len(args) > 0:
			print("Incorrect use of command")
		else:
			input("Paused. Press ENTER to continue\n")

	def do_quit(self, args):
		if len(args) > 0:
			print("Incorrect use of command")
		else:
			print("Bye!\n")
			raise SystemExit

	def do_EOF(self):
		return True

	def emptyline(self):
		self.myprompt()

	def myprompt(self):
		self.prompt = self.color_purple(os.getcwd()) + "~$ "

	def color_blue(self, word):
		return "\033[34;01m" + word + "\033[0m"

	def color_red(self, word):
		return "\033[31;01m" + word + "\033[0m"

	def color_purple(self, word):
		return "\033[95;01m" + word + "\033[0m"
