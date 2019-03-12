import sys
import json

def init_dict():
	smk_dict = []
	for i in range(1, 10):
		f = open(f'./shinmeikai/term_bank_{i}.json')
		smk_dict += json.load(f)
		f.close()
	return smk_dict

def main():
	smk_dict = init_dict()
	search_q = sys.argv[1]
	match = next((w for w in smk_dict if w[0] == search_q), None)
	print(match)

if __name__ == '__main__':
	main()
