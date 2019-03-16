from src.dict import init_dict, dict_search
import time

def main():
        smk_dict = init_dict()
        while True:
                cmdargs = input('command:  ')
                cmd = cmdargs.split()[0]
                if cmd == 'exit':
                        break
                if cmd in ['s', 'search']:
                        start = time.time()
                        search_q = cmdargs.split()[1]
                        matches = dict_search(search_q, smk_dict)
                        print(matches)
                        end = time.time()
                        dur = end - start
                        print(f'found {len(matches)} words in {dur} seconds')


if __name__ == '__main__':
        main()