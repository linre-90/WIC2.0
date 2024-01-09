from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os, shutil

CAPTION_FONT = ("Arial", 7)

class Settings:
    def __init__(self) -> None:
        self.quality = StringVar()
        self.quality.set("70") 
        self.overwrite = IntVar()
        self.overwrite.set(1)
        self.selected_files = []
        self.out_path = ""


def open_file_browser(settings, list_box):
    clear_file_select(settings, list_box)
    settings.selected_files = filedialog.askopenfilenames(filetypes=[("Image files", ".png .jpg .jpeg")])
    if len(settings.selected_files) == 0:
        return
    settings.out_path = os.path.dirname(settings.selected_files[0])
    for idx in range(len(settings.selected_files)):
        list_box.insert(idx, settings.selected_files[idx])


def make_out_dir(path, overwrite):
    output_path = os.path.join(path, r"converted")
    if os.path.exists(output_path):
        if overwrite == 1:
            shutil.rmtree(output_path)
            os.makedirs(output_path)
            return output_path
        else:
            return None
    else:
        os.makedirs(output_path)
        return output_path


def convert(settings):
    if len(settings.selected_files) > 0 and len(settings.out_path) > 0:
        created_path = make_out_dir(settings.out_path, settings.overwrite.get())
        if created_path is None:
            messagebox.showerror(message="Error creating file.\n\nOutput folder might already exists, check overwrite options.")
            return
        success_count = 0
        for file in settings.selected_files:
            try:
                with Image.open(file) as im:
                    output_file = os.path.splitext(os.path.basename(file))[0] + ".webp"
                    im.save(os.path.join(created_path, output_file), 'webp', optimize=True, quality=settings.quality.get())
                    success_count = success_count + 1
            except OSError:
                messagebox.showerror(message="Could not convert all files.\n\nError happened during conversion")
                return
            
        messagebox.showinfo(message=f"Images converted:  {success_count}.\n\nConverted images are located at: {created_path}")

    else:
        messagebox.showerror(message="No selected files or invalid path.")


def test_quality_val(str, fullstr):
    if len(fullstr) > 0:
        if len(fullstr) > 3:
            return False
        if not  fullstr.isdigit():
            return False
        if not str.isdigit():
            return False
        quality = int(fullstr)
        if quality <= 0 or quality > 100:
            return False
        return True
    else:
        return str.isdigit()


def clear_file_select(settings, list_box):
    settings.selected_files = []
    settings.out_path = ""
    list_box.delete(0, END)


def settings_menu(frame, settings):
    ttk.Label(frame, text="Overwrites previously exported images", font=CAPTION_FONT).pack()
    ttk.Checkbutton(frame, text="Overwrite output", variable=settings.overwrite, onvalue=1, offvalue=0).pack()
    ttk.Label(frame, text="Quality of webp image default=70", font=CAPTION_FONT).pack()
    ttk.Entry(frame, textvariable=settings.quality,  validate="key", validatecommand=(frame.register(test_quality_val), "%S", "%P")).pack()


def listing_menu(frame, settings, list_box):
    
    ttk.Button(frame, text="Select files...", command=lambda: open_file_browser(settings, list_box)).pack()
    ttk.Button(frame, text="Clear selected files...", command=lambda: clear_file_select(settings, list_box)).pack()


def init():
    root = Tk()
    root.title = "Wic 2.0 - Web image converter"
    root.geometry("800x600")

    settings = Settings()

    settings_frame = LabelFrame(root, text="Settings...", padx=20, pady=20)
    settings_frame.pack(fill=X, padx=20, pady=20)
    settings_menu(settings_frame, settings)

    filelist_frame = LabelFrame(root, text="Files...", padx=20, pady=20)
    filelist_frame.pack(fill=X, padx=20, pady=20)
    file_list = Listbox(filelist_frame, height=8)
    file_list.pack(fill=X, padx=20, pady=20)
    listing_menu(filelist_frame, settings, file_list)
    
    ttk.Button(root, text="Convert...", command=lambda: convert(settings)).pack()
    root.mainloop()


if __name__ == "__main__":
    init()