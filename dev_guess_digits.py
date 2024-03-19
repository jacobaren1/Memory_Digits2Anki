from DigitPalace import PAO_palace, create_palace
import tkinter as tk
from tkinter import messagebox as mb
from random import randint
"""
    This code doesn't work properly, the result_frame and continue_frame are shown as expected
    after first submission, but only a few of the objects show after second submission and after that
    only submission window is shown.
"""
class SubmissionWindow:
    def __init__(self, MP):
        self.root = tk.Tk()
        self.root.title("Guess the number sequens!")
        self.MP = MP
        self.initialize_ui()
        self.state = 0

    def initialize_guess_values(self):
        guess_next = bool(randint(0, 2))
        shift = guess_next - (guess_next == 0)

        int_ref = randint(0, self.MP.n_loci + 1)
        int_guess = int_ref + shift

        if int_guess == self.MP.n_loci:
            int_ref = 1
            int_guess = 0
            guess_next = False
        elif int_guess == -1:
            int_ref = self.MP.n_loci - 2
            int_guess = self.MP.n_loci - 1
            guess_next = True

        self.before_after = ["before", "after"][guess_next]
        self.ref_value = self.MP.get_sequens(int_ref)
        self.correct_value = self.MP.get_sequens(int_guess)
        self.question_entry = f"What decimals comes {self.before_after} {self.ref_value}?"

    def initialize_ui(self):
        self.root.geometry('500x300')

        self.question_label = tk.Label(self.root, text="")
        self.question_label.pack()

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack()

        self.entry_label = tk.Label(self.entry_frame, text="")
        self.entry_label.pack(side=tk.TOP)

        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(side=tk.BOTTOM)
        self.entry.focus_set()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_guess)
        self.submit_button.pack()

        #result frame
        self.result_frame = tk.Frame(self.root, bg='lightgreen', width= 300, height=50)
        
        self.result_label = tk.Label(self.result_frame, text="")

        #continue frame
        self.continue_frame = tk.Frame(self.root,bg='lightgreen', width=300, height=50)
        self.continue_label = tk.Label(self.continue_frame, text="Do you want to continue?")
        self.continue_button_yes = tk.Button(self.continue_frame, text="Yes", command=self.back_to_start)
        self.continue_button_no = tk.Button(self.continue_frame, text="No", command=self.quit)
        self.root.bind("<Return>", self.submit_guess)

        self.initialize_guess_values()
        self.update_question_label()

    def update_question_label(self):
        self.entry_label.config(text=self.question_entry)

    def submit_guess(self, event=None):
        if self.state != 1:
            self.state = 1

            self.evaluate(self.entry.get())


            print("result_frame.pack()")
            self.result_frame.pack(side=tk.TOP, fill='both', expand=True)
            print("result_label.pack()")
            self.result_label.pack(side=tk.TOP, expand=True)

            print(".continue_frame.pack")
            self.continue_frame.pack(side=tk.TOP,fill='both', expand=True)
            print(".continue_label.pack")
            self.continue_label.pack(side=tk.TOP)
            print(".center_button(continue_button_yes,continue_frame)")
            self.center_button(self.continue_button_yes,self.continue_frame)
            print(".center_button(continue_button_no,continue_frame\n")
            self.center_button(self.continue_button_no,self.continue_frame)
            

            self.root.bind("<Return>", self.back_to_start)
            self.entry.config(state="disabled")
            self.root.bind("<Key>", self.key_pressed)



    def evaluate(self, ans):
        if ans == self.correct_value:
            display_text = f"Nice work! {ans} comes {self.before_after} {self.ref_value}"
            bg_col = 'lightgreen'
        else:
            display_text = f"NOOB, You guessed wrong! Correct answer is {self.correct_value}!"
            bg_col = 'pink'

        self.result_label.config(text=display_text, bg=bg_col)
        self.continue_label.config(bg=bg_col)
        self.result_frame.config(bg=bg_col)
        self.continue_frame.config(bg=bg_col)

    def key_pressed(self, event):
        if event.char.upper() == 'Y':
            self.continue_button_yes.invoke()
        elif event.char.upper() == 'N':
            self.continue_button_no.invoke()

    def back_to_start(self, event=None):

        self.state = 0

        print("result.frame.pack_forget()")
        self.result_frame.pack_forget()
        print("result.label.pack_forget()")
        self.result_label.pack_forget()
        print("continue_frame.pack_forget()")
        self.continue_frame.pack_forget()
        print("continue_label.pack_forget()")
        self.continue_label.pack_forget()
        print("continue_button_yes.pack_forget()")
        self.continue_button_yes.pack_forget()
        print("continue_button_no.pack_forget()\n")
        self.continue_button_no.pack_forget()


        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.root.bind("<Return>", self.submit_guess)

        self.initialize_guess_values()
        self.update_question_label()


    def center_button(self, button, frame):
        pady = max((frame.winfo_height() - button.winfo_reqheight()) / 2, 0)
        button.pack_configure(pady=pady)

    def quit(self, event=None):
        res = mb.askquestion('Exit Application', 'Do you really want to exit?')
        if res == 'yes':
            self.root.destroy()
        else:
            mb.showinfo('Return', 'Returning to main application')



if __name__ == "__main__":
    Cyber_Egypt = create_palace("./input_files/Cyber_Egypt.xml")
    Cyber_Egypt.generate_decimals('pi', skip_first=2)

    game = SubmissionWindow(Cyber_Egypt)
    game.root.mainloop()
