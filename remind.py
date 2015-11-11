"""
Program for learning commands and words
You need a questions.txt file in the format:
definition###answer
first line empty and no ending lines
"""
from gettext import translation
nb = translation('local', localedir='locale', languages=['nb'])
nb.install()

from time import time
from datetime import date, timedelta, datetime
from os import listdir
from random import randint
from sys import exit

# mulighet til forandre definisjon
# mulighet til legge til avgitt svar som riktig uttrykk til definisjonen
# mulighet til slette definisjon og uttrykk


# Open the question file and read the lines into txt list
questionfile = 'nyquestion.txt'
txt = open(questionfile).readlines()

# read the first line for stats, if empty make it, make it list
stats = txt[0]
if stats == '\n':
    stats = _('MemScore: 0 average_cpm: 100 Answered: 0')
print(stats)
stats = stats.split()

# make the stats items workable
totalscore = int(stats[1])  # Total score
averagecpm = int(stats[3])  # Average Characters per minute
totalanswered = int(stats[5])  # Total answered right

qcounter = 1  # for counting questions in a session


def getnewquestion():
    xfiles = listdir('lists')  # readlines of files into list
    xfile = xfiles[randint(0, len(xfiles)-1)]
    print(_('Reading expression file: lists/') + xfile)
    expression = open('lists/' +
                      xfile, encoding='utf-8', errors='ignore').readlines()
    global txt
    txt.append(expression[0])
    if '###' in expression[0]:
        split = expression[0].split('###')
        print(_('New expression is: '), split[0])
        print(_('Definition is: '), split[1])
    else:
        print(_('New expression is: '), expression[0])
    input(_('Make it stick to memory, then kick enter'))
    writefile = open('lists/' + xfile, 'w')
    writefile.writelines(expression[1:])


def save():
    # Write line to file
    writefile = open(questionfile, 'w')
    writefile.writelines(txt)
#    print(_('wrote file'))


def goodanswer():
    global qcounter, timer, score, totalscore, averagecpm, totalanswered
    # Calcultate characters per minute
    cpm = int(len(answer)/(time()-timer)*60)
    print(_('Good: %s characters per minute') % cpm)
    # Scorebonus dependent on speed
    scorebonus = int(cpm/averagecpm)
    score = score + scorebonus + 1
    print(_('Speed bonus: %s ') % scorebonus)
    totalanswered = totalanswered + 1
    # calculate new average cpm
    averagecpm = int((averagecpm*(totalanswered-1)+cpm)/totalanswered)
    # Update score
    totalscore += scorebonus
    qcounter += 1


numquestions = 10
newexpressions = 0


# Go through the lines in txt, bar the first stats line
for i in range(1, len(txt)):
    if qcounter >= numquestions:
        break
    # split the line and make a line list
    line = txt[i].strip().split('###')
    expression = line[0]
    if len(line) < 2:
        print(expression)
        definition = ''
        while definition == '':
            definition = input(_('Please define %s : ') % expression)
            confirmation = input(_('confirm with "ja": '))
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
    while qdate <= date.today():
        for z in range(100):
            print('\n')
        print(_('Question number '), qcounter)
        print(definition)
        timer = time()
        for z in range(5):
            print('')
        print(_('Give the expression: '))
        answer = input()
        for z in range(3):
            print('')
        if answer == _('save'):
            save()
            exit(0)
        # make a list splittet with ';;;'
        elist = expression.split(';;;')
        blist = [x.lower().replace(' ', '') for x in elist]
        # evaluate through list of possible right expressions
        if answer.lower().replace(' ', '') in blist:
            goodanswer()
        else:
            score = score - 1
            print(elist)
            print(_('Something wrong here'))
            print(_('you can of course add your answer as synonyme'))
            errorinput = input()
            if errorinput == _('synonyme'):
                elist.append(answer)
                line[0] = ';;;'.join(elist)
        line[2] = str(date.today() + timedelta(days=score))
        qdate = datetime.strptime(line[2], '%Y-%m-%d').date()
        print(_('Next repetition: '), line[2])
        line[3] = str(score)
        txt[i] = '###'.join(line) + '\n'
        save()
        input()
    # make the relevant elements of stats string
    stats[1] = str(totalscore)
    stats[3] = str(averagecpm)
    stats[5] = str(totalanswered)
    txt[0] = ' '.join(stats) + '\n'


if numquestions - qcounter > 0:
    newexpressions = numquestions - qcounter
    print(_('New expressions: '), newexpressions)

while newexpressions > 0:
    try:
        getnewquestion()
        newexpressions -= 1
    except:
        print(_('This expression file is probably empty'))
        input()
save()

# print the stats
print(txt[0])
print(_("You are good!"))
