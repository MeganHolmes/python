# Megan Holmes Python Code

This repo is a collection of all python code I have written or used. The idea is to maximize how much code I can reuse across projects. Main functions for all projects are contained one per file in the highest directory in src/. If there is project specific code it is in a directory under src/ with the same name as the project. All code in other directories inside src/ is intended to be shared and reusable code across projects.

## Individual projects:
### Pathfinding
This is a project that creates a 2D map with collision, and multiple entities that can navigate the environment. This project is still a work-in-progress.
Start command: ```py .\src\pathfinding.py```

### Flashcards
This is a small project intended to aid in learning. It is flashcards as everyone is familar with but presents them in a random order and uses a scoring system to determine how often a flashcard is given. At the start a flashcard has a score of zero. If the user gets the question right then the score is increased and removed from the session. The next time the user runs the flashcard program the chance that question will be asked will be decreased as their knowledge has likely improved. As the score increases the chance of the question being asked decreases as well. If the user gets the question wrong, the opposite happens.
Start command: ```py .\src\flashcards.py [PATH/TO/CSV/FILE]```

### File Synchronization
This project is my replacement for Google Drive/ Dropbox / OneDrive etc. I want to sync files across all my computers so that if any of them have a hard drive failure, or is lost / stolen I don't lose my files. This project will only function on LAN so I won't have to worry about more advanced security methods associated with external access. This program will be able to indentify other copies of itself on the local network, will perform a basic check to determine if the user profile is the same, then perform a periodic file sync.
Start command ```py .\src\file_sync.py```
