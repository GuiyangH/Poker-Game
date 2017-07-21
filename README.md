# Pocker-Game

## Files:
PokerGame.py:  Main file operating the poker play

PokerRules.py: A supportive script with all the rules of playing a '5-Card'

## How to Play:
Openup PokerGame.py and run the script directly.

Or equivantly run in cmd: python PokerGame.py

## Card Rules:
As a game of 5-Card Draw, you can check out the rules at PokerListings

http://www.pokerlistings.com/poker-rules-5-card-draw

Each player must pay a predetermined ante ($2) before being dealt any cards.

A player can "stand pat", meaning they keep all five cards, or they can throw away any amount from 1-5 cards, getting them replaced with an equal number of cards from the top of the deck.

Three players (you and two AI) will take turn to bet. Each round the one has a name in yellow color will start the bet. Each bet will cost ($2), and the call will cost $4.

## AI's action:
Two AI are playing the game. Replace is tried if AI holds high-card, one/two pairs, three/four of a kind.
AI's bet/call/fold action is randomly chosen. But the weight of each action is based on a simple estimation of the probability of the hand. See wiki for more information of each hand's probability.
https://en.wikipedia.org/wiki/Poker_probability

## Code:
The rules of comparing hands is based on Udacity's CS212 <Design of computer programs> 

## Dependency:
Interpreter: Python 2._ or Python 3._
Module: pygame (external), os, sys (internal)






