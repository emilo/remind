"""
Program for learning commands and words
You need a questions.txt file in the format:
question:::answer
"""

from datetime import date, timedelta, datetime
# from sys import argv

# script, filename = argv

today = date.today()

txt = open('questions.txt').readlines()
for i in range(len(txt)):
    line = txt[i].strip().split(':::')
    if len(line) < 3:
        line.append(str(today))
        line.append('0')
    linedate = datetime.strptime(line[2], '%Y-%m-%d').date()
    if linedate <= today:
        print(line[0])
        answer = input()
        if answer == line[1]:
            score = int(line[3]) + 1
        else:
            score = int(line[3]) - 1
            print("Better: " + line[1])
            input("Kikkaki")
        line[2] = str(today + timedelta(days=score*score/2))
        line[3] = str(score)
        txt[i] = ':::'.join(line) + '\n'
        writefile = open('questions.txt', 'w')
        writefile.writelines(txt)

'''
Todo:
 - make it possible to have different answers
 make a question creator
'''
