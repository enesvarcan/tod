import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime
import subprocess
from sys import platform

WINDOWS_COMMANDS = [["shutdown", "/s", "/t", "00"], ["shutdown", "/r", "/t", "00"]]
LINUX_COMMANDS = [["shutdown", "-h", "now"], ["shutdown", "-r", "now"]]

WINDOW_HEIGHT = 200
WINDOW_WIDTH = 400
DARK_ORANGE = "#FF8C00"

ABOUT = """"""
HELP = """"""


class GUI:

    def __init__(self, master):
        self.master = master
        self.master.title('Tod')
        self.master.call('wm', 'iconphoto', self.master._w, tk.PhotoImage(file='icon.png'))
        master.resizable(width=False, height=False)

        canvas = tk.Canvas(master, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
        canvas.pack()

        menu_bar = tk.Menu(master)
        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label='Help', command=lambda: messagebox.showinfo(title='Help', message=HELP))
        menu_help.add_separator()
        menu_help.add_command(label='About', command=lambda: messagebox.showinfo(title='About', message=ABOUT))
        menu_bar.add_cascade(label='Help', menu=menu_help)
        master.config(menu=menu_bar)

        self.main_frame = tk.Frame(master, bg=DARK_ORANGE)
        self.main_frame.place(relheight=1, relwidth=1)

        self.radiobutton_var_operation = tk.StringVar()
        self.radiobutton_var_operation.set('shutdown')
        self.radiobutton_restart = tk.Radiobutton(self.main_frame, variable=self.radiobutton_var_operation, value='restart',
                                                  text='Restart', bg=DARK_ORANGE)
        self.radiobutton_restart.place(relx=0.1, rely=0.2, anchor='w')

        self.radiobutton_shutdown = tk.Radiobutton(self.main_frame, variable=self.radiobutton_var_operation, value='shutdown',
                                                   text='Shutdown', bg=DARK_ORANGE)
        self.radiobutton_shutdown.place(relx=0.1, rely=0.3, anchor='w')

        self.spinbox_time = tk.Spinbox(self.main_frame, from_=1, to=10000)
        self.spinbox_time.place(relx=0.7, rely=0.25, anchor='e', relheight=0.1, relwidth=0.1)

        self.radiobutton_var_time = tk.StringVar()
        self.radiobutton_var_time.set('minutes')
        self.radiobutton_minutes = tk.Radiobutton(self.main_frame, variable=self.radiobutton_var_time, value='minutes',
                                                  text='minutes', bg=DARK_ORANGE)
        self.radiobutton_minutes.place(relx=0.73, rely=0.2, anchor='w')

        self.radiobutton_hours = tk.Radiobutton(self.main_frame, variable=self.radiobutton_var_time, value='hours',
                                                text='hours', bg=DARK_ORANGE)
        self.radiobutton_hours.place(relx=0.73, rely=0.35, anchor='w')

        self.button_start = tk.Button(self.main_frame, text='Start', command=self.start_button_pressed)
        self.button_start.place(relx=0.1, rely=0.5, anchor='w', relwidth=0.35)

        self.button_stop = tk.Button(self.main_frame, text='Stop', command=self.stop_button_pressed)
        self.button_stop.place(relx=0.5, rely=0.5, anchor='w', relwidth=0.35)

        self.time_remaining_text = tk.StringVar()
        self.time_remaining_text.set("")
        self.label_time_remaining = tk.Label(self.main_frame, text=self.time_remaining_text.get(), bg=DARK_ORANGE)
        self.label_time_remaining.place(relx=0.5, rely=0.7, anchor='n')

        self.time_estimated_text = tk.StringVar()
        self.time_estimated_text.set("")
        self.label_estimated_time_minutes = tk.Label(self.main_frame, text=self.time_estimated_text.get(),
                                                     bg=DARK_ORANGE)
        self.label_estimated_time_minutes.place(relx=0.5, rely=0.8, anchor='n')

        self.START_FLAG = False

    def get_time_mode(self):
        if self.radiobutton_var_time.get() == 'minutes':
            return 60
        return 3600

    def start_button_pressed(self):
        seconds = int(self.spinbox_time.get()) * self.get_time_mode()
        self.START_FLAG = True
        self.count(seconds)
        self.disable_widgets()
        date_time = datetime.fromtimestamp(time.time()+seconds)
        self.update_label(label=self.label_estimated_time_minutes,
                          text="Your computer will " + self.radiobutton_var_operation.get() + " at " + str(date_time.strftime('%X')))

    def stop_button_pressed(self):
        self.START_FLAG = False
        self.enable_widgets()
        self.update_label(label=self.label_time_remaining, text="Countdown stopped!")
        self.update_label(label=self.label_estimated_time_minutes, text="")

    def update_label(self, label, text):
        label.config(text=text)

    def display_error_message(self):
        self.update_label(label=self.label_time_remaining, text="Error!")
        self.update_label(label=self.label_estimated_time_minutes, text=self.radiobutton_var_operation.get().title() +
                          " terminated due to an unknown error.")

    def disable_widgets(self):
        self.button_start.config(state='disabled')
        self.radiobutton_shutdown.config(state='disabled')
        self.radiobutton_restart.config(state='disabled')
        self.spinbox_time.config(state='disabled')
        self.radiobutton_minutes.config(state='disabled')
        self.radiobutton_hours.config(state='disabled')

    def enable_widgets(self):
        self.button_start.config(state='normal')
        self.radiobutton_shutdown.config(state='normal')
        self.radiobutton_restart.config(state='normal')
        self.spinbox_time.config(state='normal')
        self.radiobutton_minutes.config(state='normal')
        self.radiobutton_hours.config(state='normal')

    def display_time(self, seconds):
        if self.radiobutton_var_time.get() == 'minutes':
            self.update_label(label=self.label_time_remaining,
                              text=self.radiobutton_var_operation.get().title() + " countdown started! " +
                              str(seconds // self.get_time_mode()) + " " + self.radiobutton_var_time.get() + " " +
                              str(seconds % self.get_time_mode()) + " seconds left.")
        else:
            self.update_label(label=self.label_time_remaining,
                              text=self.radiobutton_var_operation.get().title() + " countdown started! " +
                              str(seconds // self.get_time_mode()) + " " + self.radiobutton_var_time.get() + " " +
                              str(seconds % self.get_time_mode() // 60) + " minutes left.")

    def count(self, seconds):
        if self.START_FLAG:
            seconds -= 1
            self.master.after(1000, lambda: self.count(seconds))
            self.display_time(seconds)
        if seconds <= 0:
            self.START_FLAG = False
            self.execute()
            self.main_frame.quit()

    def find_os(self):
        if platform.startswith('win'):
            return WINDOWS_COMMANDS
        elif platform.startswith('linux'):
            return LINUX_COMMANDS
        else:
            return -1

    def execute(self):
        commands = self.find_os()
        command = ['shutdown', 'restart'].index(self.radiobutton_var_operation.get())
        if command in range(len(commands)) and commands != -1:
            subprocess.call(commands[command], shell=True)
        else:
            self.display_error_message()


root = tk.Tk()
gui = GUI(root)
root.mainloop()
