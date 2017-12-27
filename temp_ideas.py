import os
import time
from pyfiglet import figlet_format
gd_string = figlet_format('Gone Driver', font='starwars')
gd_matrix = [[c for c in l] for l in gd_string.splitlines()]

chars = lambda c_list: set([c for l in gd_matrix for c in l if c.strip()])

trans = [ord(c) for c in gd_string]

while chars(gd_matrix):
    os.system('clear')
    print('\n'.join(''.join(c for c in l) for l in gd_matrix))
    gd_matrix = [[chr(trans[trans.index(ord(c))+1]) if c.strip() else c for c in l] for l in gd_matrix]
    time.sleep(0.5)
