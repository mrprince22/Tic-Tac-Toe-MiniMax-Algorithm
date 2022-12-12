import numpy as np
import random
import time
from playsound import playsound
from tkinter import *
from tkinter import ttk,messagebox

class Main:
    board = np.zeros([3,3], dtype = int)
    root = Tk(className =  " X-O Game")
    root.configure(bg = "#303030")
    root.minsize(350,350)
    title = Label(root,font = ("Cairo",20), bg = '#303030', fg = "White")
    title.grid(row = 0, column = 2)
    title.config(text = "X-O Game")
    available = []
    def __init__ (self,num,root):
        self.num = num
        self.row = int((num - 1 )/3)
        self.col = int((num - 1) % 3)
        self.button = Button(root,text = "")
        self.button.grid(row = self.row +1 , column = self.col+1, sticky = 'snew', ipadx = 40, ipady = 40)
        __class__.available.append(self)
        self.button.config(command = self.press)

    def X_win():
        c1 = any(sum(Main.board[i,:]) == 3 for i in range(3))
        c2 = any(sum(Main.board[:,j]) == 3 for j in range(3))
        c3 = sum(np.fliplr(Main.board).diagonal()) == 3 or sum(Main.board.diagonal()) == 3
        return c1 or c2 or c3

    def O_win():
        c1 = any(sum(Main.board[i,:]) == -3 for i in range(3))
        c2 = any(sum(Main.board[:,j]) == -3 for j in range(3))
        c3 = sum(np.fliplr(Main.board).diagonal()) == -3 or sum(Main.board.diagonal()) == -3
        return c1 or c2 or c3

    def tie():
        x_win = Main.X_win()
        o_win = Main.O_win()
        if not np.count_nonzero(Main.board == 0) and not (x_win or o_win) :
            return True
        else:
            return False
    
    def disable(self):    
        Main.root.destroy()

    def minimax(board, ismaxing):
        lost = Main.X_win() 
        win = Main.O_win() 
        tie = Main.tie() 
        if lost:
            return -1
        elif win:
            return 1
        elif tie:
            return 0
        
        if ismaxing: #O to play -- Maximizing
            bestscore = -1000
            for index in range(len(Main.available)):
                pos = Main.available[index]
                Main.board[pos.row][pos.col] = -1
                Main.available.remove(pos)
                score = Main.minimax(board, False)
                Main.board[pos.row][pos.col] = 0
                Main.available.insert(index,pos)
                bestscore = max(bestscore,score)
            return bestscore

        else: # X to play -- Minimizing
            bestscore = 1000
            for index in range(len(Main.available)):
                pos = Main.available[index]
                Main.board[pos.row][pos.col] = 1
                Main.available.remove(pos)
                score = Main.minimax(board, True)
                Main.board[pos.row][pos.col] = 0
                Main.available.insert(index,pos)
                bestscore = min(bestscore,score)
            return bestscore


    def O_play():
        bestscore = -1000
        bestmove = Main.available[0] 
        for index in range(len( Main.available)):
            pos = Main.available[index]
            Main.board[pos.row][pos.col] = -1
            Main.available.remove(pos)
            score = Main.minimax(Main.board,False) # We are chossing from our opponent's move => Minimizing
            Main.board[pos.row][pos.col] = 0
            Main.available.insert(index,pos)

            if score > bestscore:   
                bestscore = score
                bestmove = pos
        Main.board[bestmove.row][bestmove.col] = -1
        Main.available.remove(bestmove)
        bestmove.button.config(text = "O", font = ("Cairo",20))
        if bestscore == 1:
            print(f"Best Possible Score: O winning")
        elif bestscore == -1:
            print(f"Best Possible Score: X winning")
        elif bestscore == 0:
            print(f"Best Possible Score: Draw")







    # def O_play():
    #     pos = random.choice(Main.available)
    #     pos.button.config(text = "O", font = ("Cairo",20))
    #     Main.board[pos.row][pos.col] = -1
    #     Main.available.remove(pos)


    def press(self):
        if Main.X_win() or Main.O_win() or Main.tie():
            self.disable()
        else:
            self.turn()
            
    def turn(self):
        if self in Main.available: # if square is empty
            #Human to Play
            self.button.config(text = "X", font = ("Cairo",20))
            Main.board[self.row][self.col] = 1
            Main.available.remove(self)



            # Check if X won
            if Main.X_win(): # if X won
                    playsound("bravo.mp3")
                    # print("Playing Sound..")
                    messagebox.showinfo("Congrats!", "X wins!")
                    self.button.config(command = self.disable) 
                    Main.title.config(text = "Press Any Button to exit")             
                    
            elif Main.tie(): # if tie
                    playsound("bravo.mp3")
                    messagebox.showinfo("Tie!", "Tie!")
                    Main.title.config(text = "Press Any Button to exit")             
                    self.button.config(command = self.disable)              
            
                # Now Computer to Play:
            else:
                Main.O_play()

                if Main.O_win(): # if Computer won
                        playsound("sh.mp3")
                        messagebox.showinfo("Loser :)", "Computer wins!")
                        Main.title.config(text = "Press Any Button to exit")             
                        self.button.config(command = self.disable)

                elif Main.tie(): # if tie
                        messagebox.showinfo("Tie!", "Tie!")
                        Main.title.config(text = "Press Any Button to exit")             
                        self.button.config(command = self.disable)

        else: # if square is not empty
            messagebox.showwarning("Warning!", "Button is not empty")



def create_button(root = Main.root):
    b1 = Main(1,root)
    b2 = Main(2,root)
    b3 = Main(3,root)
    b4 = Main(4,root)
    b5 = Main(5,root)
    b6 = Main(6,root)
    b7 = Main(7,root)
    b8 = Main(8,root)
    b9 = Main(9,root)