"""
Program for learning commands and words
You need a questions.txt file in the format:
question###answer
"""
from time import time
from datetime import date, timedelta, datetime

# Open the question file and read the lines
questionfile = 'questions.txt'
txt = open(questionfile).readlines()
stats = txt[0]
if stats == '\n':
    stats = 'MemScore: 0 average_cpm: 100 Answered: 0'
print(stats)
stats = stats.split()

# Iterate through the lines in txt, bar the first stats line
for i in range(1, len(txt)):
    stats[1] = int(stats[1])  # Total score
    stats[3] = int(stats[3])  # Average Characters per minute
    stats[5] = int(stats[5])  # Total answered right
    line = txt[i].strip().split('###')
    # if missing, append date and score for question
    if len(line) < 3:
        line.append(str(date.today()))
        line.append('0')
    linedate = datetime.strptime(line[2], '%Y-%m-%d').date()
    if linedate <= date.today():
        print(line[0])
        timer = time()
        answer = input()
        if answer.lower() == line[1].lower():  # check anser, no matter caps
            # Calcultate characters per minute
            cpm = int(len(line[1])/(time()-timer)*60)
            print('Good: %s characters per minute' % cpm)
            # Scorebonus dependent on speed
            scorebonus = int(cpm/stats[3])
            score = int(int(line[3]) + scorebonus + 1)
            print('Speed bonus: %s ' % scorebonus)
            stats[5] = stats[5] + 1
            # calkulate new average cpm
            stats[3] = int((stats[3]*(stats[5]-1)+cpm)/stats[5])
            # Update score
            stats[1] += scorebonus
        else:
            score = int(line[3]) - 1
            print("Better: " + line[1])
            input("Kikkaki")
        line[2] = str(date.today() + timedelta(days=score))
        line[3] = str(score)
        txt[i] = '###'.join(line) + '\n'
    # make the relevant elements of stats string
    stats[1] = str(stats[1])
    stats[3] = str(stats[3])
    stats[5] = str(stats[5])
    txt[0] = ' '.join(stats) + '\n'
    # Write to file
    writefile = open(questionfile, 'w')
    writefile.writelines(txt)

# print the stats
print(txt[0])
print("You are good!")
'''
Todo:
 - make it possible to have different answers
 make a question creator
'''
