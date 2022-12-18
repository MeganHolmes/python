"""Main function for the flashcards program."""

# --- Imports ------------------------------------------------------------------
# System imports
from __future__ import absolute_import
from logging import error
import sys
from dataclasses import dataclass
import time
import os

# Project imports

import comms.file
import app.random

# --- Constants ----------------------------------------------------------------
SLEEP_TIME = 5

# --- Structs ------------------------------------------------------------------
@dataclass
class Flashcard:
    """Dataclass for flashcards."""
    question: str
    answer: str
    score: int = 0
    fileIdx: int = 0

@dataclass
class FlashcardData:
    """Dataclass for data to use in this program."""
    path: str
    hardMode: bool = False
    totalQuestions: int = 0
    remainingQuestions: int = 0
    correct: int = 0
    incorrect: int = 0

# --- Helper Functions ---------------------------------------------------------

def init(path):
    """Prepares the flashcards program."""
    raw_list = comms.file.getListFromCSV(path)

    if raw_list == None:
        return

    examMode = input("Exam mode? (y/n): ")
    if examMode == "y":
        examMode = True

    flashcard_list = []
    for idx, raw_flashcard in enumerate(raw_list):
        card = translateListToFlashcard(raw_flashcard, idx)
        if examMode:
            flashcard_list.append(card)
        else:
            if (app.random.checkLogisticRemoval(card.score) == False):
                flashcard_list.append(card)

    return flashcard_list

def translateListToFlashcard(raw_list, idx):
    """Translates a list to a flashcard object."""
    length = len(raw_list)
    card = Flashcard(raw_list[0], raw_list[1], 0, idx)

    if length == 3:
        card.score = int(raw_list[2])

    return card

def flashcardsRun(flashcard, flashcard_list, data):
    """Runs the main loop of flashcards program."""
    os.system('cls')
    print("Questions to go: "
        + str(data.remainingQuestions)
        + "/"
        + str(data.totalQuestions)
        + ". Correct: "
        + str(data.correct)
        + " Wrong: "
        + str(data.incorrect))

    print("Question: " + flashcard.question)
    input()
    print("Answer: " + flashcard.answer)

    answer = input("Did you get it right? y/n: ")

    if answer == "y":
        data.correct += 1
        flashcard.score += 1
        flashcard_list.remove(flashcard)
        data.remainingQuestions -= 1
    elif answer == "n":
        data.incorrect += 1
        if data.hardMode:
            flashcard.score = 0
        else:
            if flashcard.score > 0:
                flashcard.score -= 1
            else: # Technically not needed but just in case a score is negative
                flashcard.score = 0
    else:
        error("Error: Invalid input")

    comms.file.updateCellInCSV(data.path, flashcard.fileIdx, 2, flashcard.score)

# --- Main ---------------------------------------------------------------------

def main():
    """Main function for the flashcards program."""
    data = FlashcardData(sys.argv[1])

    flashcard_list = init(data.path)

    if flashcard_list == None:
        return -1

    data.totalQuestions = len(flashcard_list)
    data.remainingQuestions = data.totalQuestions

    if data.totalQuestions == 0:
        print("Lucky day, all flashcards randomly removed, try again later!")
        time.sleep(SLEEP_TIME)
        return

    hardMode = input("Hard mode? (y/n): ")
    if hardMode == "y":
        data.hardMode = True
    elif hardMode == "n":
        data.hardMode = False
    else:
        error("Error: Invalid input")

    while data.remainingQuestions > 0:
        app.random.randomizeList(flashcard_list)

        for flashcard in flashcard_list:
            flashcardsRun(flashcard, flashcard_list, data)

    print("All questions answered, good job!")
    time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
