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
  text = titleFont.render((text), 1, WHITE)
  gameWindow.blit(text, (letterX, letterY))

def renderNormal(text, letterX, letterY):
  text = font.render((text), 1, WHITE)
  gameWindow.blit(text, (letterX, letterY))

def start():
  while starting:
    gameWindow.fill(WHITE)
    gameWindow.blit(background, (-47,0))
    gameWindow.blit(button, (WIDTH/2-140, HEIGHT-450))
    render(("Trivia (1)"), WIDTH/2-120, HEIGHT-420)
    gameWindow.blit(button, (WIDTH/2-140, HEIGHT-250))
    render(("Subjs (2)"), WIDTH/2-120, HEIGHT-215)
    render(("Welcome to AvoQuiz!"), WIDTH/2-300, HEIGHT-555)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
      return True
    if keys[pygame.K_2]:
      return False
    pygame.display.update()
    pygame.event.clear()

def trivia():
    while triviaing:
      print("e")
      gameWindow.fill(WHITE)
      gameWindow.blit(background, (-47,0))
      render(("Select your category"), WIDTH/2-300, HEIGHT-575)
      renderNormal(("a - General Knowledge"), WIDTH/2-390, HEIGHT-485)
      renderNormal(("b - Books"), WIDTH/2-390, HEIGHT-460)
      renderNormal(("c - Film"), WIDTH/2-390, HEIGHT-435)
      renderNormal(("d - Music"), WIDTH/2-390, HEIGHT-410)
      renderNormal(("e - Musicals and Theatres"), WIDTH/2-390, HEIGHT-385)
      renderNormal(("f - Television"), WIDTH/2-390, HEIGHT-360)
      renderNormal(("g - Video Games"), WIDTH/2-390, HEIGHT-335)
      renderNormal(("h - Board Games"), WIDTH/2-390, HEIGHT-310)
      renderNormal(("i - Science and Nature"), WIDTH/2-390, HEIGHT-285)
      renderNormal(("j - Computers"), WIDTH/2-390, HEIGHT-260)
      renderNormal(("k - Mathematics"), WIDTH/2-390, HEIGHT-235)
      renderNormal(("l - Mythology"), WIDTH/2-390, HEIGHT-210)
      renderNormal(("m - Sports"), WIDTH/2-390, HEIGHT-185)
      renderNormal(("n - Geography"), WIDTH/2-390, HEIGHT-160)
      renderNormal(("o - History"), WIDTH/2-390, HEIGHT-135)
      renderNormal(("p - Politics"), WIDTH/2-390, HEIGHT-110)
      renderNormal(("q - Art"), WIDTH/2-390, HEIGHT-85)
      renderNormal(("r - Celebreties"), WIDTH/2-390, HEIGHT-60)
      renderNormal(("s - Animals"), WIDTH/2-390, HEIGHT-35)
      renderNormal(("t - Vehicles"), WIDTH/2-100, HEIGHT-485)
      renderNormal(("u - Comics"), WIDTH/2-100, HEIGHT-460)
      renderNormal(("v - Gadgets"), WIDTH/2-100, HEIGHT-435)
      renderNormal(("w - Japanese Anime and Manga"), WIDTH/2-100, HEIGHT-410)
      renderNormal(("x - Cartoon and Animations"), WIDTH/2-100, HEIGHT-385)
      keys = pygame.key.get_pressed()
      if keys[pygame.K_a]:
        return 1
      if keys[pygame.K_b]:
        return 2
      if keys[pygame.K_c]:
        return 3
      if keys[pygame.K_d]:
        return 4
      if keys[pygame.K_e]:
        return 5
      if keys[pygame.K_f]:
        return 6
      if keys[pygame.K_g]:
        return 7
      if keys[pygame.K_h]:
        return 8
      if keys[pygame.K_i]:
        return 9
      if keys[pygame.K_j]:
        return 10
      if keys[pygame.K_k]:
        return 11
      if keys[pygame.K_l]:
        return 12
      if keys[pygame.K_m]:
        return 13
      if keys[pygame.K_n]:
        return 14
      if keys[pygame.K_o]:
        return 15
      if keys[pygame.K_p]:
        return 16
      if keys[pygame.K_q]:
        return 17
      if keys[pygame.K_r]:
        return 18
      if keys[pygame.K_s]:
        return 19
      if keys[pygame.K_t]:
        return 20
      if keys[pygame.K_u]:
        return 21
      if keys[pygame.K_v]:
        return 22
      if keys[pygame.K_w]:
        return 23
      if keys[pygame.K_x]:
        return 24
      pygame.display.update()

def triviaQuestion():
    gameWindow.fill(WHITE)
    gameWindow.blit(background, (-47,0))
    render((questionText), WIDTH/2-300, HEIGHT-575)
    renderNormal(("1.",choices[0]), WIDTH/2-300, HEIGHT-575)
    renderNormal(("2.",choices[1]), WIDTH/2-300, HEIGHT-540)
    renderNormal(("3.",choices[2]), WIDTH/2-300, HEIGHT-505)
    renderNormal(("4.",choices[3]), WIDTH/2-300, HEIGHT-470)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
      return 1
    if keys[pygame.K_2]:
      return 2
    if keys[pygame.K_3]:
      return 3
    if keys[pygame.K_4]:
      return 4
    pygame.display.update()

###### SUBJECT QUIZ ######
def playSubject(subject, questionNum, subjectCat, realSub):

  numCorrectS = 0
  timeStartS = time.time()
  questionTimeS = [timeStartS]

  # Looping for number of questions user specified
  for forLoopCounter in range(questionNum):
    # Random question
    randomQNum = random.randint(0,len(subjectCat[realSub.index(subject.upper())])-1)
    # Print question
    print(subjectCat[realSub.index(subject.upper())][randomQNum][0]["question"])
    # Asking for guess and checking with answer
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
  if (numQuestions != 0):
    correctPercent = numCorrect/numQuestions*100
    averageTime = round((timeEnd-timeStart))/numQuestions #per Question
  else:
    correctPercent = 0
    averageTime = 0
  timeTotal = round(timeEnd - timeStart) #in seconds
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
starting = True
triviaing = False

##########################################
#main function
os.system('clear')

running = True
start()
triviaing = (start())
trivia()
for i in range(questionNum):
  triviaQuestion()
while running:
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
      subject = trivia()
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
    if questionNum <= len(subjectCat[realSub.index(subject.upper())]):
      playSubject(subject, questionNum, subjectCat, realSub)
    else:
      print("Not enough questions in that category. Please choose less questions!")
  # Menu option unnable to process
  else:
    print("An error has occured and your answer could not be processed \n")

  pygame.display.update()
