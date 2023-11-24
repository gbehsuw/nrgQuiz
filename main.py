##########################################
#imports
import pygame
import random
import requests
import html
import time

pygame.init()

##########################################
#CONSTANTS
WIDTH = 400
HEIGHT = 300
WHITE = (255, 255, 255)
font = pygame.font.SysFont("Century Gothic", 25)
background = pygame.image.load("blackboard.jpg")
logo = pygame.image.load("New Piskel.png")
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
  timeEnd = time.time()
  calculateStats(numCorrect, amount, timeStart, timeEnd)

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

def playSubject(subject, questionNum):

  # running the code for questions and answers of subject questions
  with open('questions.txt', 'r') as subjectCode:    # opens text file
    exec(subjectCode.read())                          # executes the text as code
    randomQNum = random.randint(0,len(subjectCategories[0]-1))
    print(subjectCategories[realSubject[subject.upper()]][randomQNum]["question"])
    subjectCode.close()                       # closes the file
  
def calculateStats (numQuestions: int, numCorrect: int, timeStart: float, timeEnd: float):
  #numCorrect is numCorrect
  correctPercent = numCorrect/numQuestions * 100
  timeTotal = round(timeEnd) - round(timeStart) #in seconds
  averageTime = timeTotal/numQuestions #per Question

##########################################
# PYGAME SETUP
pygame.display.set_caption("Wowiezowie!")
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

##########################################
#main function
running = True
while running:
  gameWindow.fill(WHITE)
  gameWindow.blit(background, (0,0))
  gameWindow.blit(button, (WIDTH/2-50, HEIGHT))
  gameWindow.blit(button, (WIDTH/2-50, HEIGHT+50))
  render("Trivia", WIDTH/2-50, HEIGHT+100)
  render("Subjects", WIDTH/2-50, HEIGHT+180)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()


  # Main menu 
  mainMenu = int(input("1) Triva \n2) Subject \nAnswer here: "))
  # Trivia option
  if mainMenu == 1:
    subjectValid = False
    subject = 1
    while not subjectValid:
      subject = int(input("Enter the subject number: "))
      if subject in range(1,25):
          subjectValid = True
    subject = subject + 8    

    questionNum = 10
    questionValid = False
    while not questionValid:
      questionNum = int(input("Please input the number of questions: "))
      if questionNum in range(1,51):
        questionValid = True

    playTrivia(questionNum, subject)
  
  # Subject option
  elif mainMenu == 2:
    subject = input("Please input the subject of the questions: ")
    questionNum = int(input("Please input the number of questions: "))
    difficulty = int(input("Please input the difficulty of the questions: "))
    playSubject(subject, questionNum)
  # Menu option unnable to process
  else:
    print("An error has occured and your answer could not be processed \n")

  pygame.display.update()