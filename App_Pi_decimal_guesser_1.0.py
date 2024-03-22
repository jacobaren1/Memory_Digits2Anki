from DigitPalace import PAO_palace, create_palace
import tkinter as tk
from tkinter import messagebox
from random import randint


class Master(object):

    def __init__(self,MP=None):
        self.root = tk.Tk()
        self.root.title('Test decimals of π!')
        self.root.geometry('400x400')
        self.root.configure(background='')
        self.MP = MP
        self.player = Player()
        self.correct_value = None
        self.init_frame()

    def init_frame(self):

        self.main_frame = tk.Frame(self.root,bg='')
        self.main_frame.pack(pady=20,expand=True)

        self.main_label =  tk.Label(self.main_frame,text=str(self.player))
        self.main_label.grid(row=0,column=0,columnspan=2)


        #create subframes
        self.question_frame = QuestionFrame(self)
        self.entry_frame = EntryFrame(self)
        self.bottom_frame = BottomFrame(self)

        self.root.bind('<KeyPress>',self.on_key_press)

    def play_game(self):

        """
            Initializes game for guessing `evaluate` is also part of the game but called
            from EntryFrame after submitting a guess
        """
        def scramble(N):
            """Randomly pics (the index of) a locus given the total number of loci"""
            
            i_ref = randint(0,N-1)
            shift = 1 - 2*randint(0,1)

            # fix if guess is outside boundary
            if i_ref == 0 and shift == -1: 
                i_ref = N-2
                shift = 1
            elif i_ref == N-1 and shift == 1:
                i_ref = 1
                shift = -1

            i_corr = i_ref + shift
            before_after = 'after' if shift == 1 else 'before'

            return i_ref, i_corr, before_after

        def get_sequenses(MP,i_ref,i_corr):
            """Gets a the information from two loci ajacent to eachother in a MindPalace"""

            ref_value = MP.get_sequens(i_ref)
            corr_value = MP.get_sequens(i_corr)
            return ref_value, corr_value

        #initiate game with randomized values
        i_ref, i_corr, before_after = scramble(self.MP.n_loci)
        ref_value, corr_value = get_sequenses(self.MP,i_ref,i_corr)

        #store correct value in master
        self.correct_value = str(corr_value)
        
        #print question for player
        self.question_frame.update_text(before_after,ref_value)

        #Make sure submit frame is enabled
        self.entry_frame.enable()

    def evaluate(self,ans):

        player_was_right = (str(ans) == self.correct_value)
        if player_was_right:
            s = f'Nice job! {ans} is correct!'
        else:
            s = f'Too bad! You guessed {ans},\ncorrect answer was {self.correct_value}'

        #Update player scores and texts in the frame
        self.player.update_score( player_was_right )
        self.main_label.config(text=str(self.player))
        self.entry_frame.result_label.config(text=s)
    

    def on_key_press(self,event=None):

        if event.keysym == 'Escape':
                self.quit()

        elif self.entry_frame.isEnabled() and event.keysym == 'Return':
                #Only when submission possible
                self.entry_frame.submit_button.invoke()    
        
        elif self.bottom_frame.isVisible():
            #Only after results are shown
            if event.keysym in ['Return','y']:
                self.bottom_frame.do_continue_button.invoke()
            elif  event.keysym == 'n':
                self.bottom_frame.dont_continue_button.invoke()

    def quit(self):
        #Better check :)
        player_is_sure = messagebox.askyesno('','Are you sure you want to quit?')
        
        if player_is_sure:    
            messagebox.showinfo('Session ended!',self.player.str_final_score())
            self.root.destroy()
        else:
            messagebox.showinfo('Back to game','Returning back to game!')

class QuestionFrame(object):
    """
        The frame where the question is stated
        update_text() makes sure a new question is asked
        in each game
    """

    def __init__(self,master):
        self.init_frame(master)

    def init_frame(self,master):
        self.frame = tk.LabelFrame(master.main_frame,text='',bd=0)
        self.frame.grid(row=1,column=0,padx=20,ipadx=20)
        
        self.label = tk.Label(self.frame,text='This is the top frame')
        self.label.pack(pady=20,expand=True)

    def update_text(self,before_after,digits):
        self.label.config(text=f'Which {len(digits)} digits comes {before_after} {digits}?')

class EntryFrame(object):

    """
        The frame where the player submits its answers
        Contains an EntryFrame and a submission buttom
        Methods for more compact calls outside the class:
            enable, disable, isEnabled
        The submit method triggers evaluation of results and shows the BottomFrame
    """

    def __init__(self,master):
        self.master = master
        self.init_frame(master)

    def init_frame(self,master):
        self.frame = tk.Frame(master.main_frame,bd=0)
        self.frame.grid(row=2,column=0,padx=20,ipadx=20)

        self.submit_button = tk.Button(self.frame,text='Submit',command=self.submit)
        self.submit_button.grid(row=0,column=0,padx=10,ipadx=10)

        self.entry = tk.Entry(self.frame)
        self.entry.grid(row=0,column=1,padx=10,ipadx=10)

        self.result_label = tk.Label(self.frame)
        self.result_label.grid(row=1,column=0,columnspan=2,padx=10,ipadx=10)

    def submit(self,event=None):
        self.master.evaluate(self.entry.get())
        self.disable()
        self.master.bottom_frame.show()

    def enable(self):
        """Reenables all the widgets in the frame when a new game is played"""
        self.entry.config(state='normal')
        self.submit_button.config(state='normal')
        
        self.entry.delete(0, tk.END)
        self.result_label.config(text='')
        self.entry.focus_set()

    def disable(self):
        """Disables all the widgets after submission"""
        self.entry.config(state='disabled')
        self.submit_button.config(state='disabled')

    def isEnabled(self):
        return (self.entry['state'] == 'normal')

class BottomFrame(object):

    """
        This frame is hidden at start and shown after the player
        has submitted their answer.
        Methods for more compact calls outside the class:
            show, hide, isVisible
    """

    def __init__(self,master):
        self.master = master
        self.frame=None
        self.label=None
        self.do_continue_button = None
        self.dont_continue_button = None    

    def show_frame(self):
        """Initiates the frame if it's not already shown"""
        if not self.isVisible():
            self.frame = tk.LabelFrame(self.master.main_frame,text='',bd=0)
            self.frame.grid(row=3,column=0,padx=20,ipadx=20)
            
            self.label = tk.Label(self.frame,text='Do you want to continue?')
            self.label.grid(row=0,column=0,columnspan=2)

    def show_buttons(self):
        """Initiates bottoms for whether or not the user wnats to continue playing"""
        self.dont_continue_button = tk.Button(self.frame,text='No!',command = self.master.quit)
        self.do_continue_button = tk.Button(self.frame,text='Yes!',command = self.new_game)

        self.dont_continue_button.grid(row=1,column=0)
        self.do_continue_button.grid(row=1,column=1)

    def new_game(self):
        self.hide()
        self.master.play_game()

    def show(self):
        self.show_frame()
        self.show_buttons()

    def hide(self):
        if self.isVisible():
            self.frame.grid_forget()
        
    def isVisible(self):
        try:
            return len(self.frame.grid_info()) > 0
        except AttributeError:
            return False

class Player(object):
    """
        Player class to keep track of the players score
        Help functions for resultprinting:
            __str__, str_final_score
    """

    def __init__(self,name = 'Player π'):
        self.name = name
        self.score = 0
        self.games_played = 0
        self.ratio = 0

    def __str__(self):
        s = f'{self.name} - '
        s += f'Games played: {self.games_played} '
        s += f'Score: {self.score} ( {self.ratio_str()} )'
        return s


    def update_score(self,result):
        self.games_played += 1
        self.score += result
        self.ratio = self.score/self.games_played

    def ratio_str(self):
        if self.ratio in [0,1]:
            #No decimals if all or none correct guesses
            return f'{self.ratio:.0%}'
        else:
            #Two decimals otherwise
            return f'{self.ratio:.2%}'

    def str_final_score(self):
        ratio = self.score/self.games_played

        if self.score == 0:
            line0 = f'''Well fought, {self.name}!'''
        elif ratio == 1:
            line0 = f'''Brilliant, {self.name}, you're crushing it!'''
        else:
            line0 = f'''Well done, {self.name}!'''

        line1 = f'''You played {self.games_played} and made {self.score} correct guesses'''
        line2 = f'''You guessed right in {self.ratio_str()} of the games!'''
        
        return f'''{line0}\n\t{line1}\n\t{line2}'''



if __name__ == '__main__':

    Cyber_Egypt = create_palace("./input_files/Cyber_Egypt.xml")
    Cyber_Egypt.generate_decimals('pi', skip_first=2)

    game = Master(Cyber_Egypt)
    game.play_game()
    game.root.mainloop()

