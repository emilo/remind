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

# read the first line for stats, if empty make it, make it list
stats = txt[0]
if stats == '\n':
    stats = 'MemScore: 0 average_cpm: 100 Answered: 0'
print(stats)
stats = stats.split()

# make the stats items workable
totalscore    = int(stats[1])  # Total score
averagecpm    = int(stats[3])  # Average Characters per minute
totalanswered = int(stats[5])  # Total answered right

# Iterate through the lines in txt, bar the first stats line
for i in range(1, len(txt)):
    line = txt[i].strip().split('###')
    # if missing, append date and score for question
    if len(line) < 3:
        line.append(str(date.today()))
        line.append('0')
    # Make the line items workable
    question    = line[0]
    rightanswer = line[1]
    date        = datetime.strptime(line[2], '%Y-%m-%d').date()
    score       = int(line[3])

    # Ask question if date says so
    if date <= date.today():
        print(question)
        timer = time()
        answer = input()
        if answer.lower() == rightanswer.lower():  # check anser, no matter caps
            # Calcultate characters per minute
            cpm = int(len(answer)/(time()-timer)*60)
            print('Good: %s characters per minute' % cpm)
            # Scorebonus dependent on speed
            scorebonus = int(cpm/averagecpm)
            score = score + scorebonus + 1
            print('Speed bonus: %s ' % scorebonus)
            totalanswered = totalanswered + 1
            # calkulate new average cpm
            averagecpm = int((averagecpm*(totalanswered-1)+cpm)/totalanswered)
            # Update score
            totalscore += scorebonus
        else:
            score = score - 1
            print("Better: " + rightanswer)
            input("Kikkaki ")
        line[2] = str(date.today() + timedelta(days=score))
        line[3] = str(score)
        txt[i] = '###'.join(line) + '\n'
    # make the relevant elements of stats string
    stats[1] = str(totalscore)
    stats[3] = str(averagecpm)
    stats[5] = str(totalanswered)
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
