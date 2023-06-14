import os
import time
from datetime import datetime
import tkinter as tk
import logging

import PIL
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ImageChangeHandler(FileSystemEventHandler):
    def __init__(self, image_handler):
        super().__init__()
        self.image_handler = image_handler

    def on_modified(self, event):
        if event.src_path in self.image_handler.img_path_to_label:
            self.image_handler.update_image(event.src_path)

    def on_created(self, event):
        if event.src_path.endswith(('.jpg', '.png')):
            self.image_handler.add_image(event.src_path)

class ImageHandler:
    def __init__(self, root, dir_path):
        self.root = root
        self.dir_path = dir_path
        self.img_path_to_label = {}

        self.image_labels = []
        self.canvas = tk.Canvas(root)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.row = 0
        self.col = 0
        self.load_images()
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

        self.observer = Observer()
        event_handler = ImageChangeHandler(self)
        self.observer.schedule(event_handler, self.dir_path, recursive=True)
        self.observer.start()


    def add_image(self, path):
        logging.info(f"add img: {path}")
        for _ in range(5):  # try to open the file 5 times
            print("===")
            try:
                img = Image.open(path)
                break  # if the file was opened successfully, break the loop
            except IOError:
                time.sleep(1)  # wait for 1 second before trying again
        else:  # if the file could not be opened after 5 tries, return
            return

        tk_img = ImageTk.PhotoImage(img)
        img.close()
        image_label = tk.Label(self.frame, image=tk_img)
        image_label.image = tk_img

        image_label.grid(row=self.row, column=self.col)
        self.col += 1
        if self.col == 3:
            self.col = 0
            self.row += 1

        self.img_path_to_label[path] = image_label

    def update_image(self, path):
        logging.info(f"update img: {path}")
        time.sleep(1)
        try:
            img = Image.open(path)
        except PIL.UnidentifiedImageError:
            logging.error(f'Could not open image {path}')

        # img = img.resize((200, 200))  # resize for demonstration purposes
        tk_img = ImageTk.PhotoImage(img)
        img.close()  # important to close the image to free up resources
        if path in self.img_path_to_label:  # if the image label already exists
            logging.info("real update img")
            image_label = self.img_path_to_label[path]
            image_label.config(image=tk_img)
            image_label.image = tk_img  # keep a reference to the image to prevent it from being garbage collected
        else:  # if the image label does not exist, create a new one
            logging.info("add one img")
            image_label = tk.Label(self.frame, image=tk_img)
            image_label.image = tk_img
            self.img_path_to_label[path] = image_label
        return image_label

    def load_images(self):
        for file in os.listdir(self.dir_path):
            if file.endswith('.jpg') or file.endswith('.png'):
                img_path = os.path.join(self.dir_path, file)
                image_label = self.update_image(img_path)
                self.img_path_to_label[img_path] = image_label
                self.image_labels.append(image_label)
                image_label.grid(row=self.row, column=self.col)
                self.col += 1
                if self.col > 2:
                    self.col = 0
                    self.row += 1

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


logging.basicConfig(filename='monitor.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('PIL').setLevel(logging.INFO)

root = tk.Tk()
root.geometry("800x600")

cur_date = datetime.now()
date_str = cur_date.strftime('%Y-%m-%d')
# image_dir = os.path.join('..', 'images', date_str)
image_dir = 'C:\\Users\\WeiHuang\\Desktop\\test\\images\\2023-06-15'
os.makedirs(image_dir, exist_ok=True)
image_handler = ImageHandler(root, image_dir)

root.mainloop()