# PRI - One Piece Search Engine

## Preparations

Start environment
```
prienv/Scripts/activate
```
Run requirements.txt

## M1. Data Preparation

We will use the data from episodes stored at the [wiki](https://onepiece.fandom.com/wiki/Episode_1). From this we will collect:

- Title
- Episode Number
- Season Number
- Arc
- Saga
- Air Date
- Opening
- Ending
- Long Summary

From this, we will have, at least:
- 1120 episodes (therefore the same amount of unique values such as title or long summary)
- 21 seasons
- 53 arcs
- 11 sagas
- 26 openings
- 20 endings