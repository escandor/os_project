import sys, os
from shell_commands import MyShell

def main():
	prompt = MyShell()

	if len(sys.argv) == 1: # if there is no batchfile
		prompt.myprompt()
	else:
		batchfile = sys.argv[1]
		with open(batchfile, "r") as f:
			prompt.cmdqueue = [line.strip() for line in f.readlines()]
			prompt.cmdqueue.append("quit")
	print()
	prompt.cmdloop()

	#prompt.cmdloop("{}\nWelcome to your Shell!\n{}".format("\033[93;01m", "\033[0m"))

if __name__ == '__main__':
	main()
