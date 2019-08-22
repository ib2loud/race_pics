"""
race_pics v. 1.0
    This is a simple widget created to quickly resize, rename, and organize pictures taken of local races.
    The intention is to have it used as other pictures are being taken with a different card so photos can
    be ready for upload as the race is happening.

Created for Enmotive by Brad Remy - August 2019
"""

from natsort import natsorted
from tkinter import Button, Entry, Frame, Label, messagebox, PhotoImage, Tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from ttkthemes import ThemedTk
import tkinter.scrolledtext as tkst
import arrow
import os


class Race_pics:
    def __init__(self):
        """
        Initialize and set up variables and windows for future placement
        """
        # A few variables to be used throughout the class
        self.working_directory = ''
        self.image_list = []

        # Create main window
        self.root = ThemedTk(theme='radiance')
        self.root.geometry('640x480+640+300')
        self.root.configure(background='white')
        self.root.resizable(False, False)
        self.root.title('Race_Pics - We\'re really cookin\' now!')
        self.root.call('wm', 'iconphoto', self.root._w,
                       PhotoImage(file='assets\\favicon.ico'))
        Label(self.root, text=arrow.now().format("dddd, MMMM DD, YYYY"),
              background='white', font=('Tahoma, 8')).grid(row=3, column=0, sticky='W')
        Label(self.root, text='Race_Pics v. 1.0',
              background='white', font=('Tahoma', 8)).grid(row=3, column=1, sticky='E')

        # Create initial logo and directory selection visuals
        self.main_logo = PhotoImage(file='assets\\enmotive_logo.png')
        self. main_logo_window = Label(
            self.root, image=self.main_logo, borderwidth=0, highlightthickness=0, width=640, background='white')
        self.select_directory_button = Button(self.root, width=13, text='Select Directory', font=(
            'Tahoma', 20, 'bold'), command=self.select_working_directory)
        self.main_logo_window.grid(
            row=0, column=0, columnspan=2, pady=25, sticky='NESW')
        self.select_directory_button.grid(
            row=1, column=0, columnspan=2, padx=100, pady=25, sticky='NESW')

        # Run main tkinter loop
        self.root.mainloop()

    def __repr__(self):
        return f'We\'re really cookin\' now!'

    def select_working_directory(self):
        """
        This selects the image directory and creates a list of the images to be iterated through.
        After creating the list it continues the program and clears out the start up logos
        """
        # Pop up to select directory and setting up proper slashes
        self.working_directory = askdirectory()
        self.working_directory = str(self.working_directory)
        self.working_directory = self.working_directory.replace('/', '\\')
        self.working_directory += '\\'

        # Create image list and sort it naturally
        self.image_list = natsorted(os.listdir(self.working_directory))

        # Check for valid images in list and if none, start over
        for notpic in self.image_list:
            if not (notpic.lower().endswith('jpg')):
                self.image_list.remove(notpic)
        if len(self.image_list) == 0:
            messagebox.showerror(
                'No Photos', f'No Photos Were Found In {self.working_directory}')
        else:
            self.main_logo_window.destroy()
            self.select_directory_button.destroy()
            self.create_gui()
        return

    def create_gui(self):
        """
        This arranges the entry boxes, labels, and info window for the program to use
        """
        # Create frame for entry labels
        main_frame = Frame(self.root, width=640, height=50, background='white')
        main_frame.grid(row=0, column=0, columnspan=2)

        # Create entry labels
        Label(main_frame, text='Image Batch Details:', background='white', font=(
            'Tahoma', 20, 'bold underline')).grid(row=0, column=0, columnspan=2)
        Label(main_frame, text='Photographer Name: ',
              background='white', font=('Tahoma', 15)).grid(row=1, column=0, sticky='w', pady=(5, 0))
        self.name_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.name_entry.grid(row=1, column=1, pady=(5, 0), sticky='e')
        Label(main_frame, text='Race Name: ',
              background='white', font=('Tahoma', 15)).grid(row=2, column=0, sticky='w', pady=(5, 0))
        self.race_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.race_entry.grid(row=2, column=1, pady=(5, 0), sticky='e')
        Label(main_frame, text='Race Location: ',
              background='white', font=('Tahoma', 15)).grid(row=3, column=0, sticky='w', pady=(5, 0))
        self.location_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.location_entry.grid(row=3, column=1, pady=(5, 0), sticky='e')
        Label(main_frame, text='Race Date: ', background='white',
              font=('Tahoma', 15)).grid(row=4, column=0, sticky='w', pady=(5, 0))
        self.date_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.date_entry.grid(row=4, column=1, pady=(5, 0), sticky='e')
        self.date_entry.insert(1, arrow.now().format("MMMM DD, YYYY"))
        Label(main_frame, text='Resize Images To: ', background='white',
              font=('Tahoma', 15)).grid(row=5, column=0, sticky='w', pady=(5, 0))
        self.size_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.size_entry.grid(row=5, column=1, pady=(5, 0), sticky='e')
        self.size_entry.insert(1, '1200')
        self.start_button = Button(main_frame, text='START', width=12, font=(
            'Tahoma', 15, 'bold'), command=self.start_batch)
        self.start_button.grid(row=7, column=1, sticky='e')

        # Create progress bar and label
        self.progress_bar = ttk.Progressbar(
            main_frame, orient='horizontal', length=600)
        self.progress_bar.config(mode='determinate')
        self.progress_bar.grid(
            row=6, column=0, columnspan=2, pady=(12))
        self.progress_label = Label(
            main_frame, text=f'Current Progress: 0 / {len(self.image_list)}', background='white', font=('Tahoma', 12, 'bold'))
        self.progress_label.grid(row=7, column=0, columnspan=2, sticky='w')

        # Create text window
        self.info_window = tkst.ScrolledText(
            self.root, width=47, height=5, font=('Tahoma', 17), wrap='word', borderwidth=2)
        self.info_window.grid(row=1, column=0, columnspan=2,
                              sticky='s', pady=(15, 0))
        self.info_window.insert(
            1.0, f'Found {len(self.image_list)} images in {self.working_directory}\n')
        self.info_window.config(state='disabled')

        return

    def start_batch(self):
        """
        This is where the images will be manipulated and looped through
        """
        # Set up initial variables for index and progress bar
        self.start_button.config(state='disabled', text='RUNNING...')
        img_idx = 0
        progress = 0
        progress_bar_increment = 100 / len(self.image_list)

        # Set up user entered variables
        photog_prefix = ''.join(
            c for c in self.name_entry.get() if c.isupper())
        print(photog_prefix)

        # Loop through images by index of image_list
        while img_idx < len(self.image_list):
            self.info_window.config(state='normal')
            self.info_window.insert(
                1.0, f'Processing {self.image_list[img_idx]}\n')

            # Update progress bar and label
            self.progress_bar.config(value=progress)
            progress += progress_bar_increment
            self.progress_label.config(
                text=f'Current Progress: {img_idx+1} / {len(self.image_list)}')
            self.info_window.config(state='disabled')

            # Move to next photo
            img_idx += 1
            self.root.update()

        # Pickle variables to show up next time

        # Finish batch and change button to allow new batch to be made
        self.info_window.insert(1.0, 'Batch Complete!\n')
        self.start_button.config(
            state='normal', text='NEW BATCH', command=self.select_working_directory)


# Run program
if __name__ == '__main__':
    Race_pics()
