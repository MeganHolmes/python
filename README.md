# Megan Holmes Python Code

This repo is a collection of all python code I have written or used. The idea is to maximize how much code I can reuse across projects. Main functions for all projects are contained one per file in the highest directory in src/. If there is project specific code it is in a directory under src/ with the same name as the project. All code in other directories inside src/ is intended to be shared and reusable code across projects.

## Individual projects:
### Flashcards
This is a small project intended to aid in learning. It is flashcards as everyone is familar with but presents them in a random order and uses a scoring system to determine how often a flashcard is given. At the start a flashcard has a score of zero. If the user gets the question right then the score is increased and removed from the session. The next time the user runs the flashcard program the chance that question will be asked will be decreased as their knowledge has likely improved. As the score increases the chance of the question being asked decreases as well. If the user gets the question wrong, the opposite happens.
Start command: ```py .\src\flashcards.py [PATH/TO/CSV/FILE]```
