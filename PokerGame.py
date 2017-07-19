"""
Created on Thu Jul  6 13:44:49 2017


"""
import pygame
import os, sys
import PokerRules

#Gloabal constant definition
HEIGHT = 720
WIDTH = 1280

BLACK = (0,0,0)
GREY = (192,192,192)
RED = (207,0,0)
REDLight= (247,0,0)
BLUE = (0,0,255)
YELLOW = (217,212,77)
GREEN = (7,132,37)
GREENLight= (11,201,56)
WHITE = (255,255,255)

class Control:
    def __init__(self):
        deck = PokerRules.Deck()
        self.images = {}
        self.scale = 1.0        
        self.cardSize = (WIDTH / 14, WIDTH / 10)
        self.buffer = 50
        self.buffer2 = 5
        self.background =pygame.image.load('img/pokerbackground.jpg').convert_alpha()
        self.cardBack = pygame.image.load('img/card_back.png').convert_alpha()
        self.cardBack = pygame.transform.scale(self.cardBack,(int(self.scale * self.cardSize[0]), int(self.scale * self.cardSize[1])))
        
        font = pygame.font.Font('font/CoffeeTin.ttf', 50)
        loadText = font.render("Loading...", 1, BLACK)
        loadSize = font.size("Loading...")
        loadLoc = (WIDTH/2 - loadSize[0]/2, HEIGHT/2 - loadSize[1]/2)
        
        self.tokens = [1000, 1000, 1000]
        self.rounds = 0
        
        SCREEN.blit(self.background, (-300, -100))
        
        SCREEN.blit(loadText, loadLoc)
        
        pygame.display.flip()
        
        for card in deck:
            self.images[str(card)] = pygame.image.load(card.image_path).convert_alpha()
            self.images[str(card)] = pygame.transform.scale(self.images[str(card)], (int(self.scale * self.cardSize[0]), int(self.scale * self.cardSize[1])))
        
        self.start_up_init()
    
    def main(self):
        if self.state == 0:
            self.start_up()
        elif self.state == 1:
            self.play()
        elif self.state == 2:
            self.play_round()
        elif self.state == 3:
            self.show_result()       
    
    def start_up_init(self):        
        
        self.font = pygame.font.Font('font/CoffeeTin.ttf', 75)
        self.font2 = pygame.font.Font('font/CoffeeTin.ttf', 45)
        
        self.startTextSurf, self.startTextRect = self.text_objects("Five Card Draw Poker", self.font, BLACK)
        self.startTextRect.center = (WIDTH/2, HEIGHT/2)
               
        self.playButtonSize = self.font2.size(" Play ")
        self.playButtonLoc = (WIDTH/3, 2 * HEIGHT/3)
        
        self.quitButtonSize = self.font2.size(" Quit ")
        self.quitButtonLoc = (2* WIDTH/3, 2 * HEIGHT/3)
                
        self.state = 0        
    
    def start_up(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        
        #draw background
        SCREEN.blit(self.background, (-300,-100))
        
        #draw welcome text
        SCREEN.blit(self.startTextSurf, self.startTextRect)
        
        #draw play and quit button
        self.button("Play", self.playButtonLoc, self.playButtonSize, GREEN, GREENLight, self.font2, WHITE, self.play_init)
        self.button("Quit", self.quitButtonLoc, self.quitButtonSize, RED, REDLight, self.font2, WHITE, self.quitgame)         
        
        pygame.display.flip()
       # pygame.display.update()  
        
                    
    def play_init(self):         
        self.rounds += 1
        self.poker = PokerRules.Poker(self.tokens)
        
        self.cardLoc = {}
        self.round = 0
        self.comp1AIaction = 0
        self.comp2AIaction = 0
        
        #initialize the states
        self.poker.foldState = [0, 0, 0]
        self.poker.winState = [0, 0, 0]
                
        #set totalTokens to zero for new round
        self.totalTokens = 0  
        
        
        self.replaceClick = False
        self.standClick = False
        self.betClick = False
        self.callClick = False
        self.foldClick = False
        
        print(self.standClick)
        
        self.playerNeedClick = False # set to False, so computer AI player can start a round before the player clicks
          
        
        #setup the locations for each card in the your hand
        x = (WIDTH - len(self.poker.playerHand) * self.scale * self.cardSize[0])/2
                
        for index in range(len(self.poker.playerHand)):
            self.cardLoc[index] = (x, int(2 * HEIGHT /3))
            x += int(self.scale * self.cardSize[0])
            
        #setup the font information shown on the screen
        self.font3 = pygame.font.Font('font/HappyMonkey.ttf', 25)
        self.font4 = pygame.font.Font('font/HappyMonkey.ttf', 35)
        self.font5 = pygame.font.Font('font/HappyMonkey.ttf', 50)
        self.font6 = pygame.font.Font('font/HappyMonkey.ttf', 20)
        self.font3.set_bold(True)         
              
        self.replaceButtonSize = self.font3.size("replace")
        self.replaceButtonLoc = (self.cardLoc[0][0] + int(len(self.poker.playerHand) * self.cardSize[0]) + 3 * self.buffer, self.cardLoc[0][1] + int(1 * self.cardSize[1]/4))
        
        self.standPatButtonSize = self.font3.size("stand pat")
        self.standPatButtonLoc = (self.cardLoc[0][0] + int(len(self.poker.playerHand) * self.cardSize[0]) + 3 * self.buffer, self.cardLoc[0][1] + int(3 * self.cardSize[1]/4))
        
        self.betButtonSize = self.font4.size("bet")
        self.betButtonLoc = (WIDTH/2 - int(len(self.poker.playerHand) * self.cardSize[0]/2) , self.cardLoc[0][1] + self.cardSize[1] + 12 *self.buffer2)
        
        self.callButtonSize = self.font4.size("bet")
        self.callButtonLoc = (WIDTH/2 , self.cardLoc[0][1] + self.cardSize[1] + 12 * self.buffer2)
        
        self.foldButtonSize = self.font4.size("bet")
        self.foldButtonLoc = (WIDTH/2 + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.cardLoc[0][1] + self.cardSize[1] + 12 * self.buffer2) 
        
        self.newGameButtonSize = self.font4.size("New Game")
        self.newGameButtonLoc = (WIDTH - 3 * self.buffer, HEIGHT/ 2 + self.buffer)
        
        #setup the location for other two players "Jason" and "Dwayne"
        self.comp1Loc = (self.buffer, 2 * self.buffer)
        self.comp2Loc = (WIDTH - int(self.buffer + len(self.poker.playerHand) * self.cardSize[0]), 2 * self.buffer)
        
        self.state = 1     
       
        
    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()
                
            #when the user click 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #create an area for the mouse click and check for intersection of either card
                    mouseRect = pygame.Rect(event.pos, (1,1))
                    for index in range(len(self.poker.playerHand)):
                        cardRect = pygame.Rect(self.cardLoc[index], (int(self.scale * self.cardSize[0]), int(self.scale * self.cardSize[1])))
                        if cardRect.colliderect(mouseRect):
                            self.poker.playerHand[index].selected = not self.poker.playerHand[index].selected
                            break
            
            #display background
            SCREEN.blit(self.background, (-300, -200))
            
            #display player name and tokens
            self.display_tokens()
            
            #dispaly the player's hand
            self.display_hand(self.poker.playerHand, self.cardLoc[0][0], self.cardLoc[0][1])
            
            for index in range(len(self.poker.comp1Hand)):
                SCREEN.blit(self.cardBack, (self.comp1Loc[0] + int(index * self.scale * self.cardSize[0]), self.comp1Loc[1]))
                SCREEN.blit(self.cardBack, (self.comp2Loc[0] + int(index * self.scale * self.cardSize[0]), self.comp2Loc[1]))
          
            #draw buttons
            self.replaceClick = self.button("replace", self.replaceButtonLoc, self.replaceButtonSize, GREEN, GREENLight, self.font6, WHITE, self.poker.replace, self.poker.playerHand)
            self.standClick = self.button("stand pat", self.standPatButtonLoc, self.standPatButtonSize, GREEN, GREENLight, self.font6, WHITE, self.poker.stand_pat, self.poker.playerHand)
            
            #when user click 'replace' or 'stand pat', move to the bet/call stage
            if self.replaceClick == True or self.standClick == True:             
                for i in range(3):
                    self.poker.tokens[i] -= 2
                    self.poker.totalTokens += 2 
                              
                self.state = 2                                 
                            
            #bet call fold buttons are inactive at this stage
            self.button("bet", self.betButtonLoc, self.betButtonSize, GREY, GREY, self.font3, WHITE, )
            self.button("call", self.callButtonLoc, self.callButtonSize, GREY, GREY, self.font3, WHITE, )
            self.button("fold", self.foldButtonLoc, self.foldButtonSize, GREY, GREY, self.font3, WHITE, )
            
            
            pygame.display.update()    
    
    def play_round(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()          
            
            #show the total token accumulated in one round
            self.tokenTextSurf, self.tokenTextRect = self.text_objects("$" + str(self.poker.totalTokens), self.font5, WHITE)
            self.tokenTextRect.center = (WIDTH/2, HEIGHT/2)  
       
            #display background
            SCREEN.blit(self.background, (-300, -200))
            
            #display player name and tokens
            self.display_tokens()
            
            #dispaly the player's hand
            self.display_hand(self.poker.playerHand, self.cardLoc[0][0], self.cardLoc[0][1])
            
            for index in range(len(self.poker.comp1Hand)):
                SCREEN.blit(self.cardBack, (self.comp1Loc[0] + int(index * self.scale * self.cardSize[0]), self.comp1Loc[1]))
                SCREEN.blit(self.cardBack, (self.comp2Loc[0] + int(index * self.scale * self.cardSize[0]), self.comp2Loc[1]))
        
            
            #draw buttons, 'replace' and 'standpat' become inactive
            self.button("replace", self.replaceButtonLoc, self.replaceButtonSize, GREY, GREY, self.font6, WHITE, )
            self.button("stand pat", self.standPatButtonLoc, self.standPatButtonSize, GREY, GREY, self.font6, WHITE, )
            
            #bet call fold buttons are active now
            self.betClick = self.button("bet", self.betButtonLoc, self.betButtonSize, GREEN, GREENLight, self.font3, WHITE, self.poker.bet, self.poker.playerHand )
            self.callClick = self.button("call", self.callButtonLoc, self.callButtonSize, GREEN, GREENLight, self.font3, WHITE, self.poker.call, self.poker.playerHand )
            self.foldClick = self.button("fold", self.foldButtonLoc, self.foldButtonSize, GREEN, GREENLight, self.font3, WHITE, self.poker.fold, self.poker.playerHand )

            # set the extra computer action before the player click the button, so each player including AI can take a lead
            if self.rounds % 3 == 2 and self.playerNeedClick == False:
                self.poker.AI_action(self.poker.comp1Hand)
                self.comp1AIaction = self.poker.AIaction
                
                # comp1hand call ,jump to the show_result
                if self.poker.AIaction == 2 or self.poker.foldState.count(1) == 2:
                    self.state = 3   
                    
                else:
                    self.poker.AI_action(self.poker.comp2Hand)
                    self.comp2AIaction = self.poker.AIaction
                    #comp2hand call or both comp1 and comp2 choose to fold, jump to show result
                    if self.poker.AIaction == 2 or self.poker.foldState.count(1) == 2:
                        self.state = 3
                
                self.playerNeedClick = True
                        
            elif self.rounds % 3 == 0 and self.playerNeedClick == False:
                 self.poker.AI_action(self.poker.comp2Hand)
                 self.comp2AIaction = self.poker.AIaction
                
                 if self.poker.AIaction == 2 or self.poker.foldState.count(1) == 2:
                     self.state = 3 
                
                 self.playerNeedClick = True

            if self.callClick == True or self.poker.foldState.count(1) == 2:
                self.state = 3         
                     
            elif self.betClick == True or self.foldClick == True:
                self.poker.AI_action(self.poker.comp1Hand)
                self.comp1AIaction = self.poker.AIaction
                
                    #comp1hand call, jump to show result stage
                if self.poker.AIaction == 2 or self.poker.foldState.count(1) == 2:
                    self.state = 3
                else:
                    self.poker.AI_action(self.poker.comp2Hand)
                    self.comp2AIaction = self.poker.AIaction
                        #comp2hand call, or both comp1 and comp2 choose to fold, jump to show result stage
                    if self.poker.AIaction == 2 or self.poker.foldState.count(1) == 2:
                        self.state = 3           
          
            self.display_AIaction(self.comp1AIaction, self.comp1Loc[0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.comp1Loc[1] + self.cardSize[1] + 10 * self.buffer2)
            self.display_AIaction(self.comp2AIaction, self.comp2Loc[0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.comp2Loc[1] + self.cardSize[1] + 10 * self.buffer2)
  
            pygame.display.update()
            
    def show_result(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit() 
                
            self.poker.result()    
            
            #display background
            SCREEN.blit(self.background, (-300, -200)) 
            
            #display player name and tokens
            self.display_tokens()
            self.display_winner()
            
            #dispaly the player's hand
            self.display_hand(self.poker.playerHand, self.cardLoc[0][0], self.cardLoc[0][1])
            self.display_hand(self.poker.comp1Hand, self.comp1Loc[0] , self.comp1Loc[1])
            self.display_hand(self.poker.comp2Hand, self.comp2Loc[0] , self.comp2Loc[1])
          
            #draw buttons, 'replace' and 'standpat' become inactive
            self.button("replace", self.replaceButtonLoc, self.replaceButtonSize, GREY, GREY, self.font6, WHITE, )
            self.button("stand pat", self.standPatButtonLoc, self.standPatButtonSize, GREY, GREY, self.font6, WHITE, )
            
            #bet call fold buttons are inactive at this stage
            self.button("bet", self.betButtonLoc, self.betButtonSize, GREY, GREY, self.font3, WHITE, )
            self.button("call", self.callButtonLoc, self.callButtonSize, GREY, GREY, self.font3, WHITE, )
            self.button("fold", self.foldButtonLoc, self.foldButtonSize, GREY, GREY, self.font3, WHITE, )
            
            self.button("New Game", self.newGameButtonLoc, self.newGameButtonSize, GREEN, GREENLight, self.font3, WHITE, self.play_init)
            
            self.display_AIaction(self.comp1AIaction, self.comp1Loc[0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.comp1Loc[1] + self.cardSize[1] + 10 * self.buffer2) 
            self.display_AIaction(self.comp2AIaction, self.comp2Loc[0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.comp2Loc[1] + self.cardSize[1] + 10 * self.buffer2)
                      
            self.display_handResult(self.poker.playerHand, self.cardLoc[0][0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.cardLoc[0][1] - 10 * self.buffer2)
            self.display_handResult(self.poker.comp1Hand, self.comp1Loc[0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.comp1Loc[1] + self.cardSize[1] + 15 * self.buffer2)
            self.display_handResult(self.poker.comp2Hand, self.comp2Loc[0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.comp2Loc[1] + self.cardSize[1] + 15 * self.buffer2)
                        
            
            pygame.display.update()            
 
            
    def text_objects(self, text, font, color):
        self.textSurface = font.render(text, True, color)
        return self.textSurface, self.textSurface.get_rect()        
 
    
    def button(self, msg, buttonLoc, buttonSize, buttonColor1, buttonColor2, font, textcolor, action = None, actionInput = None):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.buttonVertexLoc = (buttonLoc[0] - buttonSize[0]/2, buttonLoc[1] - buttonSize[1]/2)
                      
        #draw a button in active state and take an action if clicked
        if buttonLoc[0] + buttonSize[0]/2 > self.mouse[0] > buttonLoc[0] - buttonSize[0]/2 and buttonLoc[1] + buttonSize[1]/2 > self.mouse[1] > buttonLoc[1] - buttonSize[1]/2:
            pygame.draw.rect(SCREEN, buttonColor2, (self.buttonVertexLoc, buttonSize))
            if self.click[0] == 1 and action != None:
                if actionInput == None:
                    action()
                else:
                    action(actionInput) 
                #return whether replace button is clicked
                return self.click[0]
   
        #draw a buttion in inactive state             
        else:
            pygame.draw.rect(SCREEN, buttonColor1, (self.buttonVertexLoc, buttonSize))
            
        #draw button outline
        pygame.draw.rect(SCREEN, BLACK, (self.buttonVertexLoc, buttonSize), 2)
        #smallText = pygame.font.SysFont("comicsansms",20)
        self.textSurf, self.textRect = self.text_objects(msg, font, textcolor)
        self.textRect.center = buttonLoc
        SCREEN.blit(self.textSurf, self.textRect)         
        
            
    def quitgame(self):
        pygame.quit(); sys.exit()
        quit()           
    
               
    def display_hand(self, hand, x, y):
        for index in range(len(hand)):
            if not hand[index].selected:
                SCREEN.blit(self.images[str(hand[index])], (x, y))
            else:
                SCREEN.blit(self.cardBack, (x, y))            
            x += int(self.scale *self.cardSize[0])  
            
    def display_tokens(self):
        # show the start player of each round in YELLOW color
        color1, color2, color3 = WHITE, WHITE, WHITE
        if self.rounds % 3 == 1:
            color1 = YELLOW
        elif self.rounds % 3 == 2:
            color2 = YELLOW
        else:
            color3 = YELLOW
        #show your information 
        youTextSurf, youTextRect = self.text_objects("You:  $" + str(self.poker.tokens[0]), self.font3, color1)
        youTextRect.center = (WIDTH/2, self.cardLoc[0][1] - 4 * self.buffer2)   
        #show the other two players' information     
        comp1TextSurf, comp1TextRect = self.text_objects("Jason:  $" + str(self.poker.tokens[1]), self.font3, color2)
        comp1TextRect.center = (self.comp1Loc[0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.comp1Loc[1] + self.cardSize[1] + 4 * self.buffer2)
        
        comp2TextSurf, comp2TextRect = self.text_objects("Dwayne:  $" + str(self.poker.tokens[2]), self.font3, color3)
        comp2TextRect.center = (self.comp2Loc[0] + int(len(self.poker.playerHand) * self.cardSize[0]/2), self.comp2Loc[1] + self.cardSize[1] + 4 * self.buffer2)
        #show the total token accumulated in one round
        tokenTextSurf, tokenTextRect = self.text_objects("$" + str(self.poker.totalTokens), self.font5, WHITE)
        tokenTextRect.center = (WIDTH/2, HEIGHT/2) 
  
        #display the text
        SCREEN.blit(youTextSurf, youTextRect)
        SCREEN.blit(comp1TextSurf, comp1TextRect)
        SCREEN.blit(comp2TextSurf, comp2TextRect)
        SCREEN.blit(tokenTextSurf, tokenTextRect)  
        
    def display_AIaction(self, AIaction, x, y):
        # if AI takes an action, show the last action 
        if AIaction == 1:
            action = 'bet'
        elif AIaction == 2:
            action = 'call'
        elif AIaction == 3:
            action = 'fold'
        else:
            action = 'waiting for other players'
            
        AItextSurf, AItextRect = self.text_objects(str(action), self.font6, WHITE)
        AItextRect.center = (x, y)
        
        SCREEN.blit(AItextSurf, AItextRect)
    
    def display_handResult(self, hand, x, y):
        #each hand information
        scoreText = self.poker.convert_score(hand)
        
        scoreTextSurf, scoreTextRect = self.text_objects(str(scoreText), self.font3, WHITE)
        scoreTextRect.center = (x, y)
        
        SCREEN.blit(scoreTextSurf, scoreTextRect)  
        
    def display_winner(self):
        winner = []
        # display the winner under the total tokens
        if self.poker.winState[0] == 1:
            winner.append("You")
        if self.poker.winState[1] == 1:
            winner.append("Jason")
        if self.poker.winState[2] == 1:
            winner.append("Dwayne")
            
        if len(winner) == 1:
            winnerTextSurf, winnerTextRect = self.text_objects(" Winner:  " + winner[0] , self.font3, YELLOW)
        elif len(winner) == 2:
            winnerTextSurf, winnerTextRect = self.text_objects(winner[0] + " and " + winner[1] + " win !", self.font3, YELLOW)
        elif len(winner) == 3:
            winnerTextSurf, winnerTextRect = self.text_objects(winner[0] + " and " + winner[1] + " and " + winner[2] + " win !", self.font3, YELLOW)            
        
        winnerTextRect.center = (int(WIDTH/4), HEIGHT/2 + self.buffer) 
        SCREEN.blit(winnerTextSurf, winnerTextRect)       
          
            
            
#############################################################
if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_caption("5 Card Draw Poker")
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    
    Runit = Control()
    Myclock = pygame.time.Clock()
    
    while 1:
        Runit.main()
        Myclock.tick(30)

