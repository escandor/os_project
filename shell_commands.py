from cmd import Cmd
from subprocess import *
import os

class MyShell(Cmd):

	shell = os.getcwd() + "/myshell"

	def default(self, args):
		# invalid_commands = ["clear", "ls"]

		# if args not in invalid_commands:
		pid = os.fork()
		if pid > 0:
			wpid = os.waitpid(pid, 0)
		else:
			if args.split()[-1] == "&":
				p = Popen(args[:-2], shell=True, stderr=PIPE)
				return p.communicate()
			else:
				tokens = args.split()
				call(tokens)
		# else:
		# 	print("Command does not exist: " + args)
		# 	print("Type \"help\" to see valid commands")

	def do_cd(self, args):
		if len(args) > 0:
			try:
				os.chdir(args)
				os.environ["PWD"] = os.getcwd()
			except FileNotFoundError:
				print("File or directory \"{}\" does not exist".format(args))
		self.myprompt()

	def do_clr(self, args):
		os.system("clear")

	def do_dir(self, args):
		try:
			directory = os.listdir()
			if len(args) > 0:
				directory = os.listdir(args)
			for file in directory:
				if file[0] != ".":
					if os.path.isdir(file):
						print(self.color_blue("(d) " + file))
					else:
						print("(f) " + file)
		except FileNotFoundError as e:
			print("No such directory: " + "".join(args))

	def do_environ(self, args):
		if len(args) > 0:
			print("Incorrect use of command")
			return
		else:
			for k, v in os.environ.items():
				print("\033[01m" + k + ":\033[0m")
				print(v + "\n")

	def do_echo(self, args):
		print(" ".join(args.split()))

	# def do_help(self, arg):
	# 	pass

	def do_pause(self, args):
		if len(args) > 0:
			print("Incorrect use of command")
			return

		input("Paused. Press ENTER to continue\n")

	def do_quit(self, args):
		if len(args) > 0:
			print("Incorrect use of command")
		else:
			print("Bye!\n")
			raise SystemExit

	def do_EOF(self, args):
		return True

	def myprompt(self):
		self.prompt = self.color_yellow(os.getcwd()) + "~$ "

	def color_blue(self, word):
		return "\033[34;01m" + word + "\033[0m"

	def color_yellow(self, word):
		return "\033[93;01m" + word + "\033[0m"