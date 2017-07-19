#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 22:36:43 2017

"""
import operator
import random
import unittest

class Card:
    
    def __init__(self, rank, suit):
        
        # convert the rank to an interger, mapping A:14, K:13, Q:12, J:11, T:10
        self.rank = '--23456789TJQKA'.index(rank)
        self.suit = suit
        self.image_path = ('img/'+ str(self.rank) + str(self.suit) + '.png')
        self.selected = False  
        
    def __str__(self):
        out = ""
        # convert rank back to word for easily checking
        out += str('--23456789TJQKA'[self.rank]) 
     
        out += ' of '
        # convert suit back to word 
        mappings = {'H': 'Hearts', 'S': 'Spades', 'D': 'Diamonds', 'C': 'Clubs'}
        out += mappings[self.suit]  
        return out
        

class Hand:
    
    def __init__(self, cards):
        self.cards = cards      
    
    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        out = "" 
        for card in self.cards:
            out += str(card) +"\n"
        return out 
    
    def __getitem__(self, index):
        return self.cards[index]
    
    def card_ranks(self):
        # return a list of the ranks, sorted with higher first
        ranks = [card.rank for card in self.cards]
        ranks.sort(reverse = True)    
        return [5, 4, 3, 2, 1] if ranks == [14, 5, 4, 3, 2] else ranks 

    def straight(self, ranks):
        # return true if the ordered ranks form a 5-card straight
        return (ranks[0] - ranks[-1]) == 4 and len(set(ranks)) == 5
    
    def flush(self):
        #return true if all the cards have the same unit
        return len(set([card.suit for card in self.cards])) == 1
    
    def kind(self, n, ranks):
        #return the first rank that this hand has exactly n of or return none
        for r in ranks:
            if ranks.count(r) == n:
                return r
        return None
    
    def two_pair(self, ranks):
        # if there are two pairs, return the ranks from highest pair to lowest, or return none
        pairs = set()
        for r in ranks:
            if ranks.count(r) == 2:
                pairs.add(r)
        if len(pairs) == 2:
            return tuple(sorted(pairs, reverse = True))
        return None
    
    def hand_rank(self):
        ranks = self.card_ranks()
        
        if self.kind(5, ranks):
            return (9, self.kind(5, ranks))
        elif self.straight(ranks) and self.flush():
            return(8, max(ranks))
        elif self.kind(4, ranks):
            return(7, self.kind(4, ranks), self.kind(1,ranks))
        elif self.kind(3, ranks) and self.kind(2, ranks):
            return (6, self.kind(3, ranks), self.kind(2, ranks))
        elif self.flush():
            return (5, ranks)
        elif self.straight(ranks):
            return (4, max(ranks))
        elif self.kind(3, ranks):
            return (3, self.kind(3, ranks), ranks)
        elif self.two_pair(ranks):
            return (2, self.two_pair(ranks), ranks)
        elif self.kind(2, ranks):
            return (1, self.kind(2, ranks), ranks)
        else:
            return (0, ranks)

    
    def get_most_suit(self):
        suits = {'H':0, 'S':0, 'C':0, 'D': 0}
        for card in self.cards:
            suits[card.suit] += 1
        if max(suits.items(), key = operator.itemgetter(1))[1] > 2:
            return max(suits.items(), key = operator.itemgetter(1))[0]
        else:
        #output a random maximum suit, in order to break the sequence of 'HSCD'
            maxsuits = []
            for suit in 'HSCD':
                if suits[suit] == 2:
                    maxsuits.append(suit)                    
            return random.choice(maxsuits)

    def get_most_rank(self):
        ranks_mapping = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0}
        for card in self.cards:
            ranks_mapping[card.rank] += 1
        return max(ranks_mapping.items(), key = operator.itemgetter(1))[0]             
            
            
    
    
class Deck:
    
    def __init__(self):
        self.deck = []
        
        #suit H: Hearts, S: Spades, C: Clubs, D: Diamonds
        for suit in 'SHDC':
            for rank in '23456789TJQKA':
                self.deck.append(Card(rank, suit))
                
        random.shuffle(self.deck) 
        
    def __len__(self):
        return len(self.deck)
    
    def __str__(self):
        out = "" 
        for card in self.deck:
            out += str(card) +"\n"
        return out
    
    def __getitem__(self, index):
        return self.deck[index]
   
    def deal(self, amount):
        #shuffle is included in the __init__, no shuffle in deal
        cards = []      
                    
        # create and return a list of cards taken randomly from the deck
        for i in range(amount):
            # cards left is not enough for another round, use a new set of cards
            if len(self.deck) == 0:
                newDeck = Deck()               
                self.deck.extend(newDeck)
                
            card = self.deck.pop()
            cards.append(card)
        return cards

class Poker:
    
    def __init__(self, tokens):
        self.deck = Deck()
        self.tokens = tokens
        self.totalTokens = 0
        
        self.AIaction = 0
        self.foldState = [0, 0, 0]
        self.winState = [0, 0, 0]
        
        self.playerHand = Hand(self.deck.deal(5))
        self.comp1Hand = Hand(self.deck.deal(5))
        self.comp2Hand = Hand(self.deck.deal(5))
        
    def replace(self, hand):
               
        for index in range(len(hand)):
            if hand.cards[index].selected:
                hand.cards[index] = (self.deck.deal(1))[0]  
    
    def stand_pat(self, hand):
        # in case player clicked the cards and still wish to stand pat
        for index in range(len(hand)):
            if hand.cards[index].selected:
                hand.cards[index].selected = False
                
    def bet(self, hand):
        # each bet cost 2 tokens
        if hand == self.playerHand:
            self.tokens[0] -= 2
            self.totalTokens += 2
        elif hand == self.comp1Hand:
            self.tokens[1] -= 2
            self.totalTokens += 2
        elif hand == self.comp2Hand:
            self.tokens[2] -= 2
            self.totalTokens += 2
            
    def call(self, hand):
        # each bet cost 4 tokens
        if hand == self.playerHand:
            self.tokens[0] -= 4
            self.totalTokens += 4
        elif hand == self.comp1Hand:
            self.tokens[1] -= 4
            self.totalTokens += 4
        elif hand == self.comp2Hand:
            self.tokens[2] -= 4
            self.totalTokens += 4
            
    def fold(self, hand):           
        if hand == self.playerHand:
            self.foldState[0] = 1           
        elif hand == self.comp1Hand:
            self.foldState[1] = 1           
        elif hand == self.comp2Hand:
            self.foldState[2] = 1       
        
    def computerReplace(self):
        self.AI_replace(self.comp1Hand)
        self.AI_replace(self.comp2Hand)
        
    def replace_suit(self, hand):
        suit = hand.get_most_suit()
        
        for card in hand:
            if card.suit != suit:
                card.selected = True
        self.replace(hand)
        
    def replace_rank(self, hand):
        rank = hand.get_most_rank()
        for card in hand:
            if card.rank != rank:
                card.selected = True
        self.replace(hand)
        
    def AI_replace(self, hand):
        score = hand.hand_rank()[0]
                # High card, try for flush
        if score == 0:  
            self.replace_suit(hand)
        #one pair, two pair, three of a kind, or four of a kind
        elif score == 1 or score ==2 or score ==3 or score ==7:  
            self.replace_rank(hand)
         #all the other cases are not considered here 
    
    def AI_action(self, hand):
        score = hand.hand_rank()[0]
        self.AIaction = 0
        
        if score == 0:
            # high card or one pair only, randomly choose from bet, call, fold
            self.AIaction = random.choice([1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
        elif score == 1:
            self.AIaction = random.choice([1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3])
        elif score == 2:
            self.AIaction = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3])
        elif score == 3:           
            self.AIaction = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
        else:
            self.AIaction = random.choice([1, 1])           
        
        if self.AIaction == 1:
            self.bet(hand)
        elif self.AIaction == 2:
            self.call(hand)
        elif self.AIaction == 3:
            self.fold(hand)    
 
            
    def result(self):
        rank1 = self.playerHand.hand_rank()
        rank2 = self.comp1Hand.hand_rank()
        rank3 = self.comp2Hand.hand_rank()
             
        ranks = []
        #if player fold, set the rank of the player to be 0, lower than any possible hand
        if self.foldState[0] == 0:
            ranks.append(rank1)
        else:
            ranks.append((0,))  
            
        if self.foldState[1] == 0:
            ranks.append(rank2)
        else:
            ranks.append((0,))  
            
        if self.foldState[2] == 0:
            ranks.append(rank3)
        else:
            ranks.append((0,))
        
        ranks.sort(reverse = True) 
        
        if ranks[0] != ranks [1]:            
            if ranks[0] == rank1:
                self.tokens[0] += self.totalTokens
                self.winState[0] = 1
            elif ranks[0] == rank2:
                self.tokens[1] += self.totalTokens
                self.winState[1] = 1
            else:
                self.tokens[2] += self.totalTokens
                self.winState[2] = 1
                      
        elif ranks[0] == ranks[1] and ranks[1] != ranks[2]:
            if rank3 != ranks[0] and rank3 != ranks[1]:
                self.tokens[0] += self.totalTokens / 2
                self.tokens[1] += self.totalTokens / 2 
                self.winState[0] = 1
                self.winState[1] = 1
            elif rank2 != ranks[0] and rank2 != ranks[1]:
                self.tokens[0] += self.totalTokens / 2
                self.tokens[2] += self.totalTokens / 2
                self.winState[0] = 1
                self.winState[2] = 1
            elif rank1 != ranks[0] and rank1 != ranks[1]:
                self.tokens[1] += self.totalTokens / 2
                self.tokens[2] += self.totalTokens / 2
                self.winState[1] = 1
                self.winState[2] = 1
        
        elif ranks[0] == ranks[1] and ranks[0] == ranks[2]:
            self.tokens[0] += self.totalTokens / 3
            self.tokens[1] += self.totalTokens / 3
            self.tokens[2] += self.totalTokens / 3 
            for i in range(3):
                self.winState[i] = 1   
        
        self.totalTokens = 0                             
      
        
    def convert_score(self, hand):
        
        score = hand.hand_rank()[0]
        scoreList = ["High Card", "One Pair","Two Pair","Three of a Kind","Straight","Flush","Full Hose","Four of a Kind","Straight Flush"]
        return scoreList[score]    
   
       
class TestPoker(unittest.TestCase):
    
    def test_base(self):
        sf = Card('A','D')
        ef = Card('K','H')
       
        cards = []
        cards.append(sf)
        cards.append(ef)
        cards.append(ef) 
        cards.append(sf) 
        cards.append(Card('3','D')) 
        
       
        self.assertTrue((sf.rank, sf.suit) == (14, 'D'))
        self.hand1 = Hand(cards)
        #self.assertTrue(self.hand.card_ranks() == [14,13])
        
        self.playdeck = Deck()
        self.card = Card('A','D')
        #print(str(sf))
        #print(str(self.hand))
        #print(str(self.playdeck))
        #self.hand1 = Hand(self.playdeck.deal(5))
        #print(str(self.hand1))
       # print(len(self.playdeck))
        #self.hand1 = Hand(self.playdeck.deal(30))
       # print(str(self.hand1))
       
        #self.hand1 = Hand(self.deck.deal(30))
        #print(self.hand1.hand_str())
        #print(self.hand1.hand_rank())
        poker = Poker([1000,1000,1000])
        print(str(poker.playerHand),str(poker.comp1Hand), str(poker.comp2Hand))
       # print(str(poker.comp1Hand))
        print(poker.playerHand.hand_rank())
        print(poker.comp1Hand.hand_rank())
        print(poker.comp2Hand.hand_rank())      
        #print(poker.comp1Hand.get_most_suit())
       # print(poker.comp1Hand.get_most_rank())
        #poker.AI_replace(poker.comp1Hand)
        poker.bet(poker.playerHand)
        poker.bet(poker.comp1Hand)
        poker.bet(poker.comp2Hand)
        poker.fold(poker.comp1Hand)
        poker.call(poker.playerHand)
        print(poker.foldState)
        poker.result()
        
        print(poker.tokens)
        
        
       
   
        
def main():
    unittest.main()


if __name__ == '__main__':
    main()       
