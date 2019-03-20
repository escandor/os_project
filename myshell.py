from cmd import Cmd
import os, sys

class MyShell(Cmd):

	def do_cd(self, path):
		try:
			if os.path.exists:
				os.chdir(path)
			os.environ["PWD"] = os.getcwd()
			print("{}{}{}".format("\033[34;01m", os.getcwd(), "\033[0m"))
		except FileNotFoundError:
			print("\"{}\" does not exist.".format(path))

	def do_clr(self, args):
		os.system("clear")
		print("{}Cleared!{}".format("\033[93;01m", "\033[0m"))

	def do_dir(self, args):
		contents = sorted([elem for elem in os.listdir() if elem[0] != "."])
		for file in contents:
			if os.path.isdir(file):
				print("\033[34;01m" + file + "\033[0m")
			else:
				print(file)

	def do_environ(self, args):
		if len(args) > 0:
			print(os.environ[args])
		else:
			for k, v in os.environ.items():
				print("\033[31;01m" + k + ":" + "\033[0m")
				print(v + "\n")

	def do_echo(self, args):
		print(args)

	# def do_help(self, arg):
	# 	pass

	def do_pause(self, args):
		pass

	def do_quit(self, args):
		print("{}Bye!\n{}".format("\033[93;01m", "\033[0m"))
		raise SystemExit

if __name__ == '__main__':
	prompt = MyShell()
	prompt.prompt = "\033[90m" + "> " + "\033[0m"
	prompt.cmdloop("{}\nWelcome to your Shell!\n{}".format("\033[93;01m", "\033[0m"))