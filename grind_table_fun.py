import csv
import os
import sys
import time
import random
import platform

from pyfiglet import Figlet
f = Figlet(font='slant')

def say(text):
    if platform.system() == 'Darwin':
        os.system('say ' + text)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_scores(limit):
    highest = 0
    lowest = 10000
    scores = []
    try:
        with open('score' + str(limit) + '.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                current_value = int(row[1])
                if current_value > highest:
                    highest = current_value
                if current_value < lowest:
                    lowest = current_value
                scores.append((row[0], current_value))

            return highest, lowest, scores
    except FileNotFoundError:
        return 0, 0, []

def write_scores(scores, highscores_length, limit): 
    scores = sorted(scores, key=lambda score: -score[1])[:highscores_length]

    f = open('score' + str(limit) + '.csv', 'w')

    writer = csv.writer(f)

    for s in scores:
        writer.writerow(s)

    f.close()

    return scores


def game():
    cls()
    
    tafels = []

    for i in range(1,10):
        for j in range(1,10):
            tafels.append((str(i), 'x', str(j), str(i * j)))
            tafels.append((str(i * j), ':', str(i), str(j)))

    random.shuffle(tafels)

    limit = 200
    
    try:
        limit = int(sys.argv[1])
        tafels = tafels[:limit]
    except Exception:
        limit = 200

    highest, lowest, scores = get_scores(limit)

    points = 0
    highscores_length = 10


    print(f.renderText('Maaltafelfun!'))
    print('')
    print('- Een fout antwoord: -1 punt')
    print('- Een juist antwoord: 1 punt.')
    print('- Geantwoord binnen de 5 seconden?')
    print('  Des te sneller, des te meer extra punten!')
    print('')
    input('Druk ENTER om verder te gaan.')
    cls()

    for t in tafels:
        starttime = time.time()
        response = ''
        
        while True:
            response = input(t[0] + ' ' + t[1] + ' ' + t[2] + ' = ')
            if response != t[3]:
                points -= 1
                print('\033[91mFOUT!!!\033[0m')
                say("FOUT!")
            else:
                break

        points += 1
        
        difference = time.time() - starttime

        if difference < 1:
            print('\033[92mULTRAMEGASPEEDMONSTER!!!!!!\033[0m')    
            say("ultraspeedmonster!")
            points += 5
        elif difference < 2:
            print('\033[94mMEGASPEEDMONSTER!!!!!!\033[0m')    
            say("mega speed monster!")
            points += 4
        elif difference < 3:
            print('\033[96mSUPERSPEEDMONSTER!!!!!!\033[0m')    
            say("super speed monster!")
            points += 3
        elif difference < 4:
            print('\033[93mSPEEDMONSTER!!!!!!\033[0m')    
            say("speed monster!")
            points += 2
        elif difference < 5:
            print('\033[95mLITTLE SPEEDMONSTER!!!!!!\033[0m')    
            say("little speed monster!")
            points += 1

    print('')
    print('Je hebt ' + str(points) + ' punten.')
    say('You have ' + str(points) + ' points.')
    print('')

    name = None

    if points > lowest or len(scores) < highscores_length:
        if points > highest:
            print('TOPSCORE!!!')
            say('Topscore!')
        else:
            print('Highscore!')
            say('Highscore!')
        
        print('')
        
        while True:
            name = input('Geef je naam: ').strip()
            if name != '':
                break

        scores.append((name, points))
    
    cls()
    scores = write_scores(scores, highscores_length, limit)

    print(f.renderText('HIGHSCORES!'))

    for i in range(len(scores)): 
        if scores[i][1] == points and scores[i][0] == name:
            print(str(i + 1) + '. ' + '\033[92m' + scores[i][0] + ': ' + str(scores[i][1]) + '\033[0m')
        else:
            print(str(i + 1) + '. ' + scores[i][0] + ': ' + str(scores[i][1]))
        

    print('')
    input('Druk ENTER om het volgende spel te starten gaan.')
    game()

game()