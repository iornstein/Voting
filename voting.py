import copy
import sys #just so I can abort when I was doing bug-testing
import random #for the coinflip

#text Example will be 0 if running the program. if 1 or 2 then it will run a test example.
testExample = 0

if len(sys.argv) >2:
    print "TOO MANY COMMAND LINE ARGUMENTS."
    print "type this into your terminal: "
    print "\t  \t python voting.py"
    print "or if you want to instead see a test example, type: "
    print "\t \t python voting.py 1"
    print "or type a 2 instead of the 1"
    sys.exit()
if len(sys.argv) == 2:
    testExample = str(sys.argv[1])


print "Running text example "
print testExample

inputIncorrect = 1
 
voteName = None 
twoWinners = None
secondVote = 0 #when we are finding two winners, the second vote gets activitated (set to 1). This is to allow us to pass the original borda count to figure out the second vote.
previousWinner = None #if we are doing two votes, we set the previous winner here and eliminate the candidate on the second vote.
candidate = None
candidates = None


def getTheElectionInfo():
    """this method gets user input for the election and returns it [position name, two winners or not, candidates, number voters]
    
    This method asks for user input for the election information: the name of the position we are voting on,
    whether we want to determine two winners (like for improv director), the candidates running for the election
    the number of voters it  returns as a list in that order"""
    voteName = raw_input("please enter what you are voting on (for example, improv director1): ")
    multWin = raw_input("if you want there to be two winners (for example, two improv directors), type the word YES in all capitals. Otherwise, type NO in all capitals  :   ")
    twoWinners = False
    if multWin == "YES":
        twoWinners = True
    elif multWin == "NO":
        twoWinners = False
    else:
        raw_input("You did not type YES or NO. Please push enter and try again")
        return getTheElectionInfo()
    candidates = []
    candidate = raw_input("enter the name of the first candidate: ")
    while not candidate == "0":
        candidates.append(candidate)
        candidate = raw_input("enter the name of the next candidate. Enter 0 if no more candidates to add: ")
    numberOfVoters = int(float(raw_input("please enter the number of people voting with digits. For example, 10 or 13. Don't enter \"ten\" or \"thirteen\": ")))
    return [voteName, twoWinners, candidates, numberOfVoters] 



#procedure that returns the key whose value is the minimum in the map AS A LIST. So, could return ['Marty'] but not 'Marty'
#If there is no ONE minimum (ie two tied minimums), return [False, list of keys with the minimum value]. [False, ['Marty', 'Ash']]
def minimumInMap(map):
    keyForMin = min(map, key=map.get) #gets the key of the minimum value in map (dictionary)
    minimum = map[keyForMin]
    if map.values().count(minimum) == 1:
        #if the min value occurs only once
        return [keyForMin]
    else:
        minKeys = []
        for key in map:
            if map[key] == minimum:
                minKeys.append(key)
        return [False, minKeys]



def getTheBallots(candidates, numberOfVoters):
    print "Make sure you don't do any spelling errors!"
    numberCandidates = len(candidates)
    ballots = []
    for voter in range(numberOfVoters):
        print ("Please enter the next ballot for the position: " + voteName)
        voterChoices = []
        i = 0
        while i < numberCandidates:
            choice = raw_input("The choice " + str(i+1) + " is: ")
            if choice not in candidates:
                print "YOU MADE A SPELLING ERROR PLEASE TYPE AGAIN"
            elif choice in voterChoices:
                print ("THIS BALLOT ALREADY VOTED FOR " + choice + " PLEASE VOTE PROPERLY") 
            else:
                voterChoices.append(choice)
                i = i+1
        ballots.append(voterChoices)
    return ballots


if testExample == 0:
    voteName, twoWinners, candidates, numberOfVoters = getTheElectionInfo()

elif testExample == "1":
    voteName = "A Position"
    twoWinners = False
    candidates = ['brit/bon', 'brit/red', 'brit/dek', 'bon/red', 'bon/dek', 'red/dek']
    numberOfVoters = 13

elif testExample == "2":
    voteName = "The Best Letter"
    twoWinners = True
    candidates = ['A', 'B', 'C', 'D']
    numberOfVoters = 2

else:
    print "testExample is set to the wrong value"
    print "testExample is"
    print testExample
    sys.exit()




voteString = "you are voting for " + str(voteName) + " and the candidates are " + str(candidates) + ". There are " + str(numberOfVoters) + " voters."
if twoWinners:
    voteString += " We are trying to select TWO winners"
else:
    voteString += " We are only trying to select ONE winner"

print voteString
correct = raw_input("If that is all correct, please type yes:  ")

if not correct == "yes":
    print "RUN THE PROGRAM AGAIN AND DON'T MESS UP THIS TIME ;)"

if testExample == 0:
    ballots = getTheBallots(candidates, numberOfVoters)
elif testExample == "1":
    ballots = [['bon/dek', 'bon/red', 'red/dek', 'brit/bon', 'brit/dek', 'brit/red'], ['brit/bon', 'brit/dek', 'bon/dek', 'brit/red', 'bon/red', 'red/dek'], ['brit/bon', 'brit/dek', 'bon/dek', 'brit/red', 'bon/red', 'red/dek'], ['bon/red', 'brit/bon', 'bon/dek', 'brit/red', 'brit/dek', 'red/dek'], ['bon/dek', 'brit/dek', 'brit/bon', 'bon/red', 'brit/red', 'red/dek'], ['brit/bon', 'bon/red', 'bon/dek', 'red/dek', 'brit/red', 'brit/dek'], ['bon/red', 'brit/dek', 'brit/bon', 'bon/dek', 'red/dek', 'brit/red'], ['brit/dek', 'red/dek', 'brit/red', 'brit/bon', 'bon/dek', 'bon/red'], ['bon/dek', 'bon/red', 'red/dek', 'brit/dek', 'brit/bon', 'brit/red'], ['bon/red', 'brit/red', 'red/dek', 'brit/bon', 'bon/dek', 'brit/dek'], ['brit/bon', 'bon/dek', 'brit/dek', 'bon/red', 'brit/red', 'red/dek'], ['brit/dek', 'brit/bon', 'bon/red', 'red/dek', 'brit/red', 'bon/dek'], ['bon/dek', 'red/dek', 'bon/red', 'brit/bon', 'brit/dek', 'brit/red']]
elif testExample == "2":
    ballots = [['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A']]
else:
    sys.exit()

print ballots


#In case of tie! The Following method returns a dictionary of lists
#Keys are the names of candidates.
#Values are lists. Each item in the list represents the number of that place votes. The first entry is the number of 1st place votes, second entry is 2nd place votes. . .
#this could be used to calculate Borda Voting pretty easily. I will use it for a method of tie breaking.
def returnMapOfVotes(ballots, candidates):    
    toReturn = {}
    for candidate in candidates:
        toReturn[candidate] = [0]*len(candidates)
    #initialize a list of length number of candidates for each candidate of zeroes (represents votes for each place)
    for ballot in ballots:
        for vote in range (len(candidates)):
            currentVote = ballot[vote]
            toReturn[currentVote][vote] += 1
    return toReturn

#Returns the list  of people who could do worst in the IRV of the potential losers. The list could be a size of one
#Essentially this does a modified borda count scaled geometrically. So, first place votes would count as 80000 each, second place votes 400, third place 20, fourth place 1.
#This is not exactly what is done, but it works the same, automatically selecting the proper geometric basis
def possibleLoserOfIRV(ballots, candidates, potentialLosers):
    """Returns the list of candidates who would possibly do the worst in the IRV of the potential losers
    
    May be a list of length 1"""
    voteMap = returnMapOfVotes(ballots, candidates)
    #get rid of people who aren't potential losers
    for candidate in candidates:
        if candidate not in potentialLosers:
            del voteMap[candidate]
    loserVotes = {} #this represents the total votes each potential loser has during run off
    for potentialLoser in potentialLosers:
        loserVotes[potentialLoser] = 0 #initialize everyone to 0 votes
    
    numberOfVotes = len(ballots[0])
    for i in range (numberOfVotes):
        #update the total votes for each candidate
        for potentialLoser in potentialLosers:
            loserVotes[potentialLoser] += voteMap[potentialLoser][i]
        minFinder = minimumInMap(loserVotes)
        if minFinder[0]: #if at this point we have found one person to eliminate
            return [minFinder[0]]
        #otherwise we run the next iteration of loop
    #if we reach here, we couldn't find one loser based on the irv. Then we return everyone who has little votes
    return minFinder[1]

#returns a map that is keyed on the name of the candidate, and the value is the borda count of that candidate  according to old election procedures:
#A first place vote counts as 1, a second place vote counts as 2, a third place vote counts as 3, sum each candidate's total.
#note that the borda count of a candidate is "better" if it is SMALL. 
#Someone with a borda count vote of 8 should win over someone with a borda count total of 15
def returnBordaMap(ballots, candidates):
    bordaMap = {}
    for candidate in candidates:
        bordaMap[candidate] = 0
    for ballot in ballots:
        voteStrength = 1
        for vote in ballot:
            if vote in candidates:
                bordaMap[vote] += voteStrength
            voteStrength+=1
    return bordaMap

#takes in a bordaMap, a map generated by returnBordaMap, returns the possible candidates (or candidate) to eliminate
def breakTiesWithBordaMap(bordaMap):
    peopleToEliminate = []
    personToEliminate = "none"
    runningMaximum = -1

    for candidate in bordaMap:
        if bordaMap[candidate] == runningMaximum:
            peopleToEliminate.append(candidate)
        #high is bad for the borda map. Higher borda count means lower approval rate
        if bordaMap[candidate] > runningMaximum:
            runningMaximum = bordaMap[candidate]
            personToEliminate = candidate
            peopleToEliminate = []
            peopleToEliminate.append(candidate)
    return peopleToEliminate


def megaTie(ballots, candidates):
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "T I E   B R E A K I N G    S C E N A R I O"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    print "All of the following candidates are tied"
    print candidates

    print "Unfortunately we have a mega-tie, a tie in both the bordavote and the instant run off with no way to choose who to eliminate. This is the rarest of all ties and all tie-breaking methods fail to work here. here are the recommended actions:"
    print ""
    print "1) do a recount of votes"
    print ""
    print "2) look at the remaining candidates and give people a chance to vote again for the remaining candidates"
    print ""
    print "3) let the computer \"flip a coin\" to randomly choose one person to eliminate among the tied candidates"
    print ""
    print ""
    flip = raw_input( "if you wish to break the tie randomly, please type FLIP in all capitals now: ")
    if flip == ("FLIP"):
        flip = random.randint(0, len(candidates)-1)
        choice = candidates[flip]
        print ("flip is:", flip)
        print ("choice to remove is:", choice)
        return choice

    print ("\n \n \n Best of luck determining a winner... ")
    sys.exit()




def mainProgram(ballots, candidates, numberVoters):

    print "running MAIN PROGRAM NOW"
    print ("BALLOTS: " + str(ballots))
    print ("CANDIDATES: " + str(candidates))
    print ("numberVoters: " + str(numberVoters))
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("   B E G I N      E L E C T I O N     P R O C E D U R E")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    bordaMap = returnBordaMap(ballots, candidates)


    return instantRunOff(copy.deepcopy(ballots), copy.deepcopy(candidates), numberOfVoters, 0, copy.deepcopy(ballots))


#destructively removes person from ballots and candidates
def removeFromBallot(ballots, candidates, person):
    print ("Unfortunately, " + person + " will not be the new " + str(voteName))
    for ballot in ballots:
        ballot.remove(person)
        #if ballot[0] == person:
         #   del ballot[0]
    candidates.remove(person)
    
    #Now we run the instant run-off

    #Method, for each ballot, add it's top choice to that candidate's running total.
    #If we don't have a majority, look at the candidates with the least votes, and remove that candidate from all of the ballots.
    #continue until we have a majority.

def instantRunOff(ballots, candidates,numberOfVoters, numberOfRunOffs, originalBallots):
    #if we are on the second vote we want to remove the previous winner. We only want to do it once, thus we check to see if we are in the first runoff.
    #in other words, this if statement gets triggered ONLY IF we are are trying to determine two winners AND it only gets triggered once
    if secondVote == 1 and numberOfRunOffs == 0:
        print "removing the previous winner from the second vote"
        removeFromBallot(ballots, candidates, previousWinner)
    print ""
    print ("remaining candidates: " + str(candidates))
    #firstPlaceVotes is a map keyed on the name of candidates. Value is the number of first place votes recieved.
    firstPlaceVotes = {}

    for candidate in candidates:
        firstPlaceVotes[candidate] = 0

    for ballot in ballots:
        #if we eliminated someone we don't want to count that ballot)
        if ballot[0] in firstPlaceVotes:
            #increase the total of the first choice of that ballot
            firstPlaceVotes[ballot[0]] += 1
        else:
            #something majorly went wrong, in our ballots we have a first place vote for someone who should be removed
            print "Invariant Violation X1"
            print ballot
            print firstPlaceVotes
            sys.exit()
    
    print "The Current Votes Are:"
    print firstPlaceVotes
    print

    #check if we have a winner!
    for candidate in firstPlaceVotes:
        if firstPlaceVotes[candidate] > numberOfVoters/2 :
            print "~~~~~~WE HAVE A WINNER!!!~~~~~~~"
            print ("after " + str(numberOfRunOffs) + " run offs, the new " + str(voteName) + " is. . .")
            for i in range(10):
                print " . . ."
            print candidate + "!!!"
            return candidate

    changedBallots = 0

    #we don't have one person with a majority of first-place votes. We now have to remove a candidate. 
    #we first attempt to find the person with the minimum number of first place votes and eliminate her or him.
    
    foundToEliminate = minimumInMap(firstPlaceVotes)
    oneMinimum = foundToEliminate[0]
             
    #the easy case: there is one minimum
    if oneMinimum:
        minPerson = oneMinimum
        print "eliminating the person according to irv rules (has the least number of first-place votes)..."
        removeFromBallot(ballots, candidates, minPerson)
        return instantRunOff(ballots, candidates, numberOfVoters, numberOfRunOffs + 1, originalBallots)
    #the hard case: multiple people tied for the least amount of first place votes
    minPeople = foundToEliminate[1]    
    #we attempt to eliminate one candidate from minPeople by using the borda count (jericho's all method)
    bordaMap = returnBordaMap(originalBallots, minPeople)

    print "we are deciding to eliminate some people. Here are their scores based on borda count (jericho's old voting method) lower score means higher approval rate:"
    print bordaMap

    #generate people with the worst borda count.
    peopleToEliminate = breakTiesWithBordaMap(bordaMap)
    #if we found one person to eliminate, do so!
    if len(peopleToEliminate) == 1:
        print "irv had an unbreakable tie, now eliminating based on the borda count (the old jericho voting method)"
        removeFromBallot(ballots, candidates, peopleToEliminate[0])
        return instantRunOff(ballots, candidates, numberOfVoters, numberOfRunOffs + 1, originalBallots)

    #otherwise we make sure that not every candidate is tied. If not everyone is tied, we do a tiebreaker
    if len(candidates) > len(minPeople):
        print "irv had an unbreakable tie, now eliminating based on two borda counts, first the old jericho voting method, and secondly one that predicts losers of irv"
        #peopleToEliminate are people tied for the highest borda count with the old method of adding (first place is 1 point, second place 2 points).
        losers = possibleLoserOfIRV(ballots, candidates, peopleToEliminate)
        #possibleLoserOfIRV returns losers who are predicted to do worst in the IRV (meaning they have less second place votes, if tie, check third place votes, etc...)
        for person in losers:
            removeFromBallot(ballots, candidates, person)
        return instantRunOff(ballots, candidates, numberOfVoters, numberOfRunOffs + 1, originalBallots)

    #Otherwise we are stuck with a megatie, we ask user if we want to randomly select someone to eliminate, otherwise we exit program
    loser = megaTie(ballots, candidates) 
    removeFromBallot(ballots, candidates, loser)
    return instantRunOff(ballots, candidates, numberOfVoters, numberOfRunOffs + 1, originalBallots)

            
EndResult = mainProgram(ballots, candidates, numberOfVoters)


if twoWinners and not EndResult[0] == 0:
    #cross out the endResult
    previousWinner = EndResult
    secondVote = 1
    raw_input(" Please note that the person above is the first winner. Push Enter to run the program to determine who the second winner is")
    secondResult = mainProgram(ballots, candidates, numberOfVoters)
    if secondResult == 0:
        print "also consider the bordaVote puts the numbers like this (less points is better): "
        for candidate in bordaMap:
            print (str(candidate) + " recieved a score of " + str(bordaMap[candidate]))
