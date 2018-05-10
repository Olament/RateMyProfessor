import os
import time

schoolList = [['Williams_College', 1209], ['Amherst_College', 33], ['Bowdoin_College', 125],
            ['Swarthmore_College', 990], ['Wellesley_College', 1156], ['Middlebury_College', 605],
            ['Pomona_College', 774], ['Carleton_College', 179], ['Claremont_McKenna_College', 234],
            ['Davidson_College', 3965], ['Washington_and_Lee_University', 1139], ['Colby_College', 250],
            ['Colgate_University', 252], ['Harvey_Mudd_College', 400], ['Smith_College', 910],
            ['Vassar_College', 4070], ['Grinnell_College', 383], ['Hamilton_College', 389],
            ['Haverford_College', 402]]

for school in schoolList:
    command = 'python3 scrape.py ' + school[0] + ' ' + str(school[1])
    print(command)
    os.system(command)