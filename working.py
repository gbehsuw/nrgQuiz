##########################################
#imports
import pygame
import random
import requests
import html
import time
import questions 
import os
realSub = questions.realSubjects()
subjectCat = questions.subjectCategories()

pygame.init()

##########################################
#CONSTANTS
WIDTH = 400
HEIGHT = 300
WHITE = (255, 255, 255)
font = pygame.font.SysFont("Century Gothic", 25)
background = pygame.image.load("blackboard.jpg")
logo = pygame.image.load("logo.png")
button = pygame.image.load("button.png")
##########################################
#API STUFF
#takes data into a dictionary of the questions
def getQuestionPool(amount, category):
  apiUrl = f"https://opentdb.com/api.php?amount={amount}&category={category}"

  response = requests.get(apiUrl)
  responseJson = response.json()

  return responseJson["results"]

#take correct and incorrect choices and mix them up
def shuffleChoices(choices):
  random.shuffle(choices)
  return choices

#print out the different choices
def printChoices(choices):
  for choice_index, choice in enumerate(choices):
    #html escape turn weird html jargin into characters
    print(f"{choice_index+1}. {html.unescape(choice)}")

#get and validate the users choices for the questions
def getUserChoice(type):
  while True:
    userChoice = ""
    choiceValid = False
    while not choiceValid:
      userChoice = input("Enter the number of your choice: ")
      for char in userChoice:
        if char in "0123456789":
          choiceValid = True
        else:
          choiceValid = False
          break

    userChoice = int(userChoice)

    #correct number range for multiple choice and T/F
    if (type == "multiple" and userChoice in range(1,5)) or (type == "boolean" and userChoice in range(1,3)):
      return userChoice - 1
    else:
      print("Invalid input, enter the number of your choice.")

#play the trivia
def playTrivia(amount, category):
  questionPool = getQuestionPool(amount, category)

  numCorrect = 0
  timeStart = time.time()
  questionTime = [timeStart]

  #loop through the questions
  for question in questionPool:
    #get question string
    questionText = html.unescape(question["question"])
    print(questionText)

    #turns the answers into a list of shuffled choices
    choices = question["incorrect_answers"]
    choices.extend([question["correct_answer"]])
    shuffledChoices = shuffleChoices(choices)
    printChoices(shuffledChoices)
    userChoiceIndex = getUserChoice(question["type"])
    userChoiceText = shuffledChoices[userChoiceIndex]
    correctChoiceText = html.unescape(question["correct_answer"])

    #check if answer is right
    if userChoiceText == correctChoiceText:
      print(f"Correct! You answered: {correctChoiceText}\n")
      numCorrect += 1
    else:
      print(f"Incorrect! The correct answer is: {correctChoiceText}\n")
    questionTime.append(time.time())
  timeEnd = time.time()
  calculateStats(amount, numCorrect, timeStart, timeEnd, questionTime)

##########################################
#FUNCTIONS
def renderText(text):
  letterX=0
  letterY=0
  alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!.“()1234567890:;$#/%^[]+-= ")
  words=list(text)
  num=0
  while num<len(words):
    for i in range(len(alphabet)-1,-1,-1):
      if alphabet[i] in words[0]:
        letterX=letterX + 12
        text = font.render((alphabet[i]), 1, WHITE)
        gameWindow.blit(text, (letterX, letterY))
        words.insert(-1,words[len(words)-1])
        words.pop(0)
        num=num+1
  pygame.display.update()

def render(text, letterX, letterY):
  text = font.render((text), 1, WHITE)
  gameWindow.blit(text, (letterX, letterY))

# Subject mode
def playSubject(subject, questionNum, subjectCat, realSub):

  numCorrectS = 0
  timeStartS = time.time()
  questionTimeS = [timeStartS]

  for forLoopCounter in range(questionNum):
    # Random question
    randomQNum = random.randint(0,len(subjectCat[0])-1)
    # Print question
    print(subjectCat[realSub.index(subject.upper())][randomQNum][0]["question"])
    guess = input("Type your answer here: ")
    if guess == subjectCat[realSub.index(subject.upper())][randomQNum][0]["answer"]:
      print("Correct!")
      numCorrectS += 1
    else:
      print("Incorrect! The answer is", subjectCat[realSub.index(subject.upper())][randomQNum][0]["answer"])
    questionTimeS.append(time.time())
  timeEndS = time.time()
  calculateStats(questionNum, numCorrectS, timeStartS, timeEndS, questionTimeS)

def calculateStats (numQuestions: int, numCorrect: int, timeStart: float, timeEnd: float, sinceStart):
  #numCorrect is numCorrect
  correctPercent = numCorrect/numQuestions*100
  timeTotal = round(timeEnd - timeStart) #in seconds
  averageTime = round((timeEnd-timeStart))/numQuestions #per Question
  #####################################################################
  # Calculating time per question
  trueTimePer = []
  for i in (1,numQuestions):
    trueTimePer.append(int(round(sinceStart[i] - sinceStart[i-1])))
  # True time now contains the amount of time spent on each question to the nearest second

##########################################
# PYGAME SETUP
pygame.display.set_caption("Wizzy Quizzy")
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

##########################################
#main function
os.system('clear')
running = True
while running:
  gameWindow.fill(WHITE)
  gameWindow.blit(background, (0,0))
  gameWindow.blit(button, (WIDTH/2+100, HEIGHT))
  gameWindow.blit(button, (WIDTH/2+100, HEIGHT+50))
  render(("Trivia"), WIDTH/2+120, HEIGHT+100)
  render(("Subjects"), WIDTH/2+120, HEIGHT+180)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()


  # Main menu 
  mainMenu = int(input("1) Triva \n2) Subject \n\nOption here: "))
  # Trivia option
  if mainMenu == 1:
    subjectValid = False
    subject = 1
    while not subjectValid:
      subject = int(input("\nEnter the subject number: "))
      if subject in range(1,25):
          subjectValid = True
    subject = subject + 8    

    questionNum = 10
    questionValid = False
    while not questionValid:
      questionNum = int(input("\nPlease input the number of questions: "))
      if questionNum in range(1,51):
        questionValid = True

    playTrivia(questionNum, subject)

  # Subject option
  elif mainMenu == 2:
    subject = input("Please input the subject of the questions: ")
    questionNum = int(input("Please input the number of questions: "))

    playSubject(subject, questionNum, subjectCat, realSub)
  # Menu option unnable to process
  else:
    print("An error has occured and your answer could not be processed \n")

  pygame.display.update()