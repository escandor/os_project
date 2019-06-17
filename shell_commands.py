# Student name: Alexandra Escandor
# ID: 17418156

from cmd import Cmd
from subprocess import *
from threading import Thread
import os

class MyShell(Cmd):

	def default(self, args):
		pid = os.fork()
		if pid > 0: # checks to see if process is given the pid of the parent process.
			wpid = os.waitpid(pid, 0)
		else:
			try:
				if args[-1] == "&": # checks to see if program should be executed in the background.
					Thread(target=self.default, args=(args[:-1],)).start() # a thread is created and runs in the background. Targets the default function again but removes &.
				elif ">" in args or ">>" in args:
					self.io_redir(args.split()) # program is passed into the io_redir if > or >> is present.
					raise SystemExit
				else:
					call(args.split()) # otherwise the command is executed simply as a child process of the shell.
					raise SystemExit # exits the child process
			except FileNotFoundError:
				print("Please enter a valid command")

	def io_redir(self, args): # redirection for non-built-in commands. Args is a list.
		func = "w"
		if ">>" in args: # if >> is in args, the variable will change to 'a' which appends to the file instead of overwriting it.
			func = "a"

		myoutput = open(args[-1], func)
		p = Popen(args[:-2], stdout=myoutput, close_fds=True)
		out, err = p.communicate()

	def io_redir_commands(self, output, args): # redirection for built-in commands. Args is a string.
		args = args.split()
		if ">" in args: # if > is present, output will be written into the given file.
			with open(args[-1], 'w') as f:
				f.write(output)
		elif ">>" in args: # if >> is present, output will be appended to the end of the given file.
			with open(args[-1], 'a') as f:
				f.write(output)
		else: # otherwise print output into the shell as normal.
			print(output)

	def do_cd(self, args):
		if len(args) > 0: # if argument is present.
			try:
				os.chdir(args) # directory is changed to argument.
				os.environ["PWD"] = os.getcwd()
			except FileNotFoundError:
				print("File or directory \"{}\" does not exist".format(args))
		else: # otherwise simply print the current directory.
			print("Current directory:", os.getcwd())
		self.myprompt()

	def do_clr(self, args):
		if len(args) > 0: # command shouldn't work if arguments are present.
			print("Incorrect use of command")
		else:
			os.system("clear")

	def do_dir(self, args):
		try:
			directory = os.listdir() # contents of current directory is set to a variable first.
			if len(args) > 0 and args[0] != ">": # if argument is present, variable is replaced to contents of argument.
				directory = os.listdir(args.split()[0])

			output = ""
			for file in directory: # adds each file/directory to a string
				if file[0] != ".":
					if os.path.isdir(file):
						output += self.color_blue("(d) " + file + "\n") # directories are blue.
					else:
						output += "(f) " + file + "\n"
			self.io_redir_commands(output.strip(), args) # string is passed to io_redir_commands function to check if redirection is needed.

		except FileNotFoundError as e:
			print("No such directory: " + "".join(args))

	def do_environ(self, args):
		if len(args) == 0 or ">" == args[0] or ">>" == args[0]: # if command has no arguments or if argument specifies redirection, then do the following.
			output = ""
			for k, v in os.environ.items():
				output += self.color_red(k + ": \n") + v + "\n\n" # keys of the os.environ are red.
			self.io_redir_commands(output.strip(), args) # output is passed into the io_redir_commands function to check is redirection is needed.
		else: # command shouldn't work if arguments are present.
			print("Incorrect use of command")

	def do_echo(self, args):
		args_lst = args.split()
		output = " ".join(args_lst)
		if ">" in args_lst or ">>" in args_lst:
			self.io_redir_commands(" ".join(output.split()[:-2]), args) # ouput passed into io_redir_commands if > or >> is present.
		else:
			print(output)

	def do_help(self, args):
		with open("readme", "r") as f: # opens the user manual and adds each line into a list.
			contents = f.readlines()
			lines = [line for line in contents]

		if len(args) == 0: # command shouldn't work if arguments are present.
			for idx, line in enumerate(lines): # indexing added to lines to ensure only 20 lines are displayed each time.
				if idx % 20 == 0 and idx != 0: # limits to 20 lines each time.
					input("Press ENTER for more...")
				print(line.rstrip())
		elif args[0] == ">":
				self.io_redir_commands("".join(contents), args)
		else: # unless the argument contains output redirection, the command shouldn't work.
			print("Incorrect use of command")

	def do_pause(self, args):
		if len(args) > 0: # command shouldn't work if arguments are present.
			print("Incorrect use of command")
		else:
			input("Paused. Press ENTER to continue\n")

	def do_quit(self, args):
		if len(args) > 0: # command shouldn't work if arguments are present.
			print("Incorrect use of command")
		else:
			print("Bye!\n")
			raise SystemExit # exits the shell.

	def emptyline(self): # fixes issue that arises when an empty line is passed into the prompt and executes the previous non-empty command.
		self.myprompt()

	def myprompt(self): # sets the shell command prompt to the current directory
		self.prompt = self.color_purple(os.getcwd()) + "~$ " # command prompt is also purple.

	def color_blue(self, word):
		return "\033[34;01m" + word + "\033[0m"

	def color_red(self, word):
		return "\033[31;01m" + word + "\033[0m"

	def color_purple(self, word):
		return "\033[95;01m" + word + "\033[0m"
