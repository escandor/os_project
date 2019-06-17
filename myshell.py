import sys, os
from shell_commands import MyShell

def main():
	prompt = MyShell()

	if len(sys.argv) == 1:	# if there is no batchfile
		prompt.myprompt()
	else:
		batchfile = sys.argv[1]
		with open(batchfile, "r") as file:
			prompt.cmdqueue = [line.strip() for line in file]
			prompt.cmdqueue.append("quit")
	prompt.cmdloop()

if __name__ == '__main__':
	main()
