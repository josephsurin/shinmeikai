import json
import difflib

def init_dict():
	smk_dict = []
	for i in range(1, 10):
		f = open(f'./shinmeikai/term_bank_{i}.json')
		smk_dict += json.load(f)
		f.close()
	return smk_dict

def main():
	smk_dict = init_dict()
	while True:
		cmdargs = input('command:  ')
		cmd = cmdargs.split()[0]
		if cmd == 'exit':
			break
		if cmd in ['s', 'search']:
			search_q = cmdargs.split()[1]
			match = [w for w in smk_dict if difflib.SequenceMatcher(a = w[0], b = search_q).ratio() > 0.60 or difflib.SequenceMatcher(a = w[1], b = search_q).ratio() > 0.60]
			print(match)

if __name__ == '__main__':
	main()
