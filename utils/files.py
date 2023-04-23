import tkinter.filedialog as filedialog

def gui_save_as_path():
    return filedialog.asksaveasfilename(
            filetypes=(("INI", "*.ini"), ("All files", "*.*")),
            defaultextension=".ini")