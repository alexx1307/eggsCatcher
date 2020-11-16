def addScore(score):
    try:
        mylist = __load()
    except FileNotFoundError:
        open('highscore.txt', 'x')
        mylist = __load()
    mylist.append(score)
    mylist.sort(reverse=True)
    __save(mylist)

def getBestScores(n):
    mylist = __load()
    return [mylist[i] for i in range(len(mylist)) if i < n]

def __load():
    with open('highscore.txt') as f:
        mylist = list(map(int, f.read().split()))
        return mylist

def __save(mylist):
    with open('highscore.txt', 'w') as f:
        f.write(' '.join(list(map(str, mylist))))
