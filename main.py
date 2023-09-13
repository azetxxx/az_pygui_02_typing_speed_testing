import tkinter as tk
import os
import pygame
import random
from texts import text_options

# Constants
FONT_NAME = "consolas"
FONT_SIZE = 30
POSSIBLE_TEXTS = text_options

class TypeSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Type Speed Test')
        self.root.geometry('500x300')
        self.root.option_add(f"*Label.Font", f"{FONT_NAME} {FONT_SIZE}")
        self.root.option_add(f"*Button.Font", f"{FONT_NAME} {FONT_SIZE}")

        self.writeAble = False
        self.passedSeconds = 0

        self.setup_gui()
        self.reset_writing_labels()

        pygame.mixer.init()

    def setup_gui(self):
        self.label_left = tk.Label(self.root, text="", fg='grey')
        self.label_left.place(relx=0.5, rely=0.5, anchor=tk.E)

        self.label_right = tk.Label(self.root, text="", fg='black')
        self.label_right.place(relx=0.5, rely=0.5, anchor=tk.W)

        self.current_letter_label = tk.Label(self.root, text="", fg='green')
        self.current_letter_label.place(relx=0.5, rely=0.6, anchor=tk.N)

        self.time_left_label = tk.Label(self.root, text='0 Seconds', fg='grey')
        self.time_left_label.place(relx=0.5, rely=0.4, anchor=tk.S)

        self.root.bind('<Key>', self.key_press)

    def reset_writing_labels(self):
        text = random.choice(POSSIBLE_TEXTS)
        split_point = 0

        self.label_left.configure(text=text[0:split_point])
        self.label_right.configure(text=text[split_point:])
        self.current_letter_label.configure(text=text[split_point])

        self.writeAble = True
        self.root.after(60000, self.stop_test)
        self.root.after(1000, self.add_second)

    def key_press(self, event=None):
        try:
            if event.keysym == 'Escape':
                self.stop_test()
            elif event.char == self.label_right.cget('text')[0]:
                self.label_right.configure(text=self.label_right.cget('text')[1:])
                self.label_left.configure(text=self.label_left.cget('text') + event.char)
                self.current_letter_label.configure(text=self.label_right.cget('text')[0])
            # else:
                # self.play_sound('error.mp3')
        except tk.TclError:
            pass


    def play_sound(self, sound_filename):
        sound_path = os.path.join("assets", sound_filename)
        if os.path.exists(sound_path):
            pygame.mixer.Sound(sound_path).play()


    def stop_test(self):
        self.play_sound('finished.mp3')
        self.writeAble = False
        amount_words = len(self.label_left.cget('text').split(' '))

        self.time_left_label.destroy()
        self.current_letter_label.destroy()
        self.label_right.destroy()
        self.label_left.destroy()

        result_label = tk.Label(self.root, text=f'Words per Minute: {amount_words}', fg='black')
        result_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        result_button = tk.Button(self.root, text='Retry', command=self.restart)
        result_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def restart(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_gui()
        self.reset_writing_labels()

    def add_second(self):
        self.passedSeconds += 1
        self.time_left_label.configure(text=f'{self.passedSeconds} Seconds')

        if self.writeAble:
            self.root.after(1000, self.add_second)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypeSpeedTestApp(root)
    root.mainloop()
