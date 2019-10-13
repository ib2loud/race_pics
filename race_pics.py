"""
race_pics v. 1.0
    This is a simple widget created to quickly resize, rename, and organize pictures taken of local races.
    The intention is to have it used as other pictures are being taken with a different card so photos can
    be ready for upload as the race is happening.

Created for EnMotive by Brad Remy - August 2019
"""

from natsort import natsorted
from PIL import Image
from tkinter import Button, Entry, Frame, Label, messagebox, PhotoImage, Tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from ttkthemes import ThemedTk
import tkinter.scrolledtext as tkst
import arrow
import glob
import io
import os
import pickle
import piexif
import pyexiv2
import shutil


class Race_pics:
    def __init__(self):
        """
        Initialize and set up variables and windows for future placement
        """
        # Create main window
        self.root = ThemedTk(theme='radiance')
        self.root.geometry('640x500+640+300')
        self.root.configure(background='white')
        self.root.resizable(False, False)
        self.root.title('Race_Pics - We\'re really movin\' now!')
        self.root.call('wm', 'iconphoto', self.root._w,
                       PhotoImage(file='assets\\favicon.ico'))

        # Create initial logo and directory selection visuals
        self.main_logo = PhotoImage(file='assets\\enmotive_logo.png')
        self. main_logo_window = Label(
            self.root, image=self.main_logo, borderwidth=0, highlightthickness=0, width=640, background='white')
        self.select_directory_button = Button(self.root, width=13, text='Select Image Folder', font=(
            'Tahoma', 20, 'bold'), command=self.select_working_directory)
        self.main_logo_window.grid(
            row=0, column=0, columnspan=2, pady=25, sticky='NESW')
        self.select_directory_button.grid(
            row=1, column=0, columnspan=2, padx=100, pady=25, sticky='NESW')

        # Run main tkinter loop
        self.root.mainloop()

    def __repr__(self):
        return f'We\'re really movin\' now!'

    def select_working_directory(self):
        """
        This selects the image directory and creates a list of the images to be iterated through.
        After creating the list it continues the program and clears out the start up logos
        """
        # A few variables to be get us going
        self.working_directory = ''
        self.save_directory = ''
        self.image_list = []

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
            # Close opening window and create main GUI
            self.main_logo_window.destroy()
            self.select_directory_button.destroy()
            self.create_gui()
        return

    def create_gui(self):
        """
        This arranges the entry boxes, labels, and info window for the program to use
        """
        # Retrieve previously entered values
        with open('assets\\image_vars.pickle', 'rb') as pickle_file:
            pic_info = pickle.load(pickle_file)
            previous_photog_name = pic_info[0]
            previous_race_name = pic_info[1]
            previous_race_location = pic_info[2]
            previous_date = pic_info[3]

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
        self.name_entry.insert(1, previous_photog_name)
        Label(main_frame, text='Race Name: ',
              background='white', font=('Tahoma', 15)).grid(row=2, column=0, sticky='w', pady=(5, 0))
        self.race_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.race_entry.grid(row=2, column=1, pady=(5, 0), sticky='e')
        self.race_entry.insert(1, previous_race_name)
        Label(main_frame, text='Race Location: ',
              background='white', font=('Tahoma', 15)).grid(row=3, column=0, sticky='w', pady=(5, 0))
        self.location_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.location_entry.grid(row=3, column=1, pady=(5, 0), sticky='e')
        self.location_entry.insert(1, previous_race_location)
        Label(main_frame, text='Race Date: ', background='white',
              font=('Tahoma', 15)).grid(row=4, column=0, sticky='w', pady=(5, 0))
        self.date_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.date_entry.grid(row=4, column=1, pady=(5, 0), sticky='e')
        self.date_entry.insert(1, previous_date)
        Label(main_frame, text='Resize Images To: ', background='white',
              font=('Tahoma', 15)).grid(row=5, column=0, sticky='w', pady=(5, 0))
        self.size_entry = Entry(main_frame, width=30, font=(
            'Tahoma', 15, 'bold'), borderwidth=2, relief='groove')
        self.size_entry.grid(row=5, column=1, pady=(5, 0), sticky='e')
        self.size_entry.insert(1, '3000')
        self.start_button = Button(main_frame, text='START', width=10, font=(
            'Tahoma', 14, 'bold'), command=self.start_batch)
        self.start_button.grid(row=7, column=1, sticky='e')
        self.save_directory_button = Button(main_frame, text='SAVE TO...', width=10, font=(
            'Tahoma', 14, 'bold'), command=self.select_save_directory)
        self.save_directory_button.grid(row=7, column=1)

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
            self.root, width=47, height=6, font=('Tahoma', 17), wrap='word', borderwidth=2)
        self.info_window.grid(row=1, column=0, columnspan=2,
                              sticky='s', pady=(10, 0))
        self.info_window.insert(
            1.0, f'Found {len(self.image_list)} images in {self.working_directory}\n----------------------------------------------------------------------------')
        self.info_window.config(state='disabled')

        # Create small labels and reset button on bottom of window
        Button(self.root, text='RESET', font=('Tahoma', 7),
               command=self.select_working_directory).grid(row=3, column=1)
        Label(self.root, text=arrow.now().format("dddd, MMMM DD, YYYY"),
              background='white', font=('Tahoma, 8')).grid(row=3, column=0, sticky='W')
        Label(self.root, text='Race_Pics v. 1.0',
              background='white', font=('Tahoma', 8)).grid(row=3, column=1, sticky='E')

        return

    def select_save_directory(self):
        """
        This sets the local directory where images will be saved
        """
        # Pop up to select directory and setting up proper slashes
        self.save_directory = askdirectory()
        self.save_directory = str(self.save_directory)
        self.save_directory = self.save_directory.replace('/', '\\')
        self.save_directory += '\\'
        self.info_window.config(state='normal')
        self.info_window.insert(
            1.0, f'Saving images to:\n{self.save_directory}\n----------------------------------------------------------------------------')
        return

    def start_batch(self):
        """
        This is where the images will be manipulated and looped through
        """
        # Check for save directory
        if self.save_directory == '':
            messagebox.showerror(
                'Select Save Directory', 'Select save directory before starting batch')
            self.create_gui
            return

        # Set up shortened variables and make sure size is only numbers
        photog_prefix = ''.join(
            c for c in self.name_entry.get() if c.isupper())
        race_prefix = self.race_entry.get().replace(' ', '_').replace('\'', '')
        picture_size = int(
            ''.join(i for i in self.size_entry.get() if i.isdigit()))

        # Set up initial variables for index and progress bar
        self.start_button.config(state='disabled', text='RUNNING...')
        self.save_directory_button.config(state='disabled')
        img_idx = 0
        progress = 0
        current_file_name = 1
        progress_bar_increment = 100 / len(self.image_list)

        # Check for existing files witih current info so the file name is continued
        save_location_and_details = f'{photog_prefix}_{race_prefix}_'
        has_prev_pics = False
        cur_folder_files = glob.glob(f'{self.save_directory}/*')
        # Also check for any files left over from an unfinished batch and delete it to avoid naming issues
        for folder_file in cur_folder_files:
            if 'MG_' in folder_file:
                os.remove(folder_file)
                cur_folder_files.remove(folder_file)
            if save_location_and_details in folder_file:
                has_prev_pics = True
        if has_prev_pics:
            current_file_name = int(cur_folder_files[-1][-9:-4]) + 1

        # Set up EXIF data for all images
        custom_exif_dict = {
            'Exif.Image.ImageDescription': f'{self.race_entry.get()} // {self.location_entry.get()}',
            'Exif.Image.Artist': self.name_entry.get(),
            'Exif.Image.Copyright': 'EnMotive',
            'Exif.Image.Software': 'Race_Pics v.1.0'
        }

        # Loop through images by index of image_list
        while img_idx < len(self.image_list):
            img_to_process = f'{self.working_directory}{self.image_list[img_idx]}'

            # Move image to save directory and update variable
            shutil.copy2(img_to_process, self.save_directory)
            img_to_process = f'{self.save_directory}//{self.image_list[img_idx]}'
            img = Image.open(img_to_process)

            # Backup original EXIF
            exif_dict = piexif.load(img.info['exif'])
            exif_bytes = piexif.dump(exif_dict)

            # Resize if necessary and rename image
            new_img_name = f'{self.save_directory}//{save_location_and_details}{str(current_file_name).zfill(5)}.jpg'
            img_size_original = max(img.size[0], img.size[1])
            if img_size_original >= picture_size:
                img.thumbnail((picture_size, picture_size), Image.ANTIALIAS)
            img.save(img_to_process, 'JPEG', exif=exif_bytes, quality=90)
            img.close()
            os.rename(img_to_process, new_img_name)

            # # Add custom EXIF
            img_meta = pyexiv2.Image(new_img_name)
            img_meta.modify_exif(custom_exif_dict)

            # Update progress bar and label
            self.info_window.config(state='normal')
            self.info_window.insert(
                1.0, f'Processing {self.image_list[img_idx]}\n')
            self.progress_bar.config(value=progress)
            progress += progress_bar_increment
            self.progress_label.config(
                text=f'Current Progress: {img_idx+1} / {len(self.image_list)}')
            self.info_window.config(state='disabled')

            # Move to next photo
            img_idx += 1
            current_file_name += 1
            self.root.update()

        # Pickle variables to show up next time a batch is ran
        pickle_data = [self.name_entry.get(), self.race_entry.get(),
                       self.location_entry.get(), self.date_entry.get()]
        with open('assets\\image_vars.pickle', 'wb') as pickle_file:
            pickle.dump(pickle_data, pickle_file)

        # Finish batch and change button to allow new batch to be made
        self.info_window.config(state='normal')
        self.info_window.insert(1.0, 'Batch Complete!\n')
        self.info_window.config(state='disabled')
        self.start_button.config(
            state='normal', text='NEW BATCH', command=self.select_working_directory)
        self.progress_bar.config(value=100)
        return


# Run program
if __name__ == '__main__':
    Race_pics()
