"""
Program for learning commands and words
You need a questions.txt file in the format:
definition###answer
first line empty and no ending lines
"""
from time import time
from datetime import date, timedelta, datetime
from os import listdir
from random import randint
from sys import exit

# Flytte getquestions til etter hovedloopen
# Lage save funksjon som kjoerer etter hovedloopen og etter oenske# Lage save
# funksjon som kjoerer etter hovedloopen og etter oenske# Lage save funksjon
# ogsom kjoerer etter hovedloopen og etter oenske
# Open the question file and read the lines into txt list
questionfile = 'nyquestion.txt'
txt = open(questionfile).readlines()

# read the first line for stats, if empty make it, make it list
stats = txt[0]
if stats == '\n':
    stats = 'MemScore: 0 average_cpm: 100 Answered: 0'
print(stats)
stats = stats.split()

# make the stats items workable
totalscore = int(stats[1])  # Total score
averagecpm = int(stats[3])  # Average Characters per minute
totalanswered = int(stats[5])  # Total answered right

qcounter = 0  # for counting questions in a session


def getnewquestion():
    xfiles = listdir('lists')  # readlines of files into list
    xfile = xfiles[randint(0, len(xfiles)-1)]
    print('Reading expression file: lists/' + xfile)
    expression = open('lists/' + xfile, encoding='utf-8', errors='ignore').readlines()
    global txt
    txt.append(expression[0])
    if '###' in expression[0]:
        split = expression[0].split('###')
        print('New expression is: ', split[0])
        print('Definition is: ', split[1])
    else:
        print('New expression is: ', expression[0])
    input('Make it stick to memory, then kick enter')
    writefile = open('lists/' + xfile, 'w')
    writefile.writelines(expression[1:])


def save():
    # Write line to file
    writefile = open(questionfile, 'w')
    writefile.writelines(txt)


def goodanswer():
    global timer, score, totalscore, averagecpm, totalanswered
    # Calcultate characters per minute
    cpm = int(len(answer)/(time()-timer)*60)
    print('Good: %s characters per minute' % cpm)
    # Scorebonus dependent on speed
    scorebonus = int(cpm/averagecpm)
    score = score + scorebonus + 1
    print('Speed bonus: %s ' % scorebonus)
    totalanswered = totalanswered + 1
    # calculate new average cpm
    averagecpm = int((averagecpm*(totalanswered-1)+cpm)/totalanswered)
    # Update score
    totalscore += scorebonus


numquestions = 5
newexpressions = 0


# Go through the lines in txt, bar the first stats line
for i in range(1, len(txt)):
    if numquestions == 0:
        break
    # split the line and make a line list
    line = txt[i].strip().split('###')
    expression = line[0]
    if len(line) < 2:
        print(expression)
        definition = ''
        while definition == '':
            definition = input('Please define %s :' % expression)
            confirmation = input('confirm with "ja"')
            if confirmation != 'ja':
                definition = ''
        line.append(definition)
    # if missing, append date and score for question
    if len(line) < 3:
        line.append(str(date.today()))
        line.append('0')
    # Make the line items workable
    definition = line[1]
    qdate = datetime.strptime(line[2], '%Y-%m-%d').date()  # make date object
    score = int(line[3])

    # Ask question if date says so
    if qdate <= date.today():
        qcounter += 1
        print('Definition is: ')
        print(definition)
        print('Give the expression: ')
        timer = time()
        answer = input()
        if answer == 'save':
            save()
            exit(0)

        if answer.lower().replace(' ', '') == expression.lower().replace(' ', ''):
            goodanswer()
        else:
            score = score - 1
            print(expression)
            input("Maybe some practice will help? ")
        line[2] = str(date.today() + timedelta(days=score))
        line[3] = str(score)
        txt[i] = '###'.join(line) + '\n'
    # make the relevant elements of stats string
    stats[1] = str(totalscore)
    stats[3] = str(averagecpm)
    stats[5] = str(totalanswered)
    txt[0] = ' '.join(stats) + '\n'


if numquestions - qcounter > 0:
    newexpressions = numquestions - qcounter
    print('New expressions: ', newexpressions)

while newexpressions > 0:
    try:
        getnewquestion()
        newexpressions -= 1
    except:
        print('This expression file is probably empty')
        input()
save()

# print the stats
print(txt[0])
print("You are good!")
'''
Todo:
 - make it possible to have different answers
'''
