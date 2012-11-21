import os, shutil

def clean_folder(folder):
    [shutil.rmtree(os.path.join(folder,item)) for item in os.listdir(folder)]

def remove_folder(folder):
    shutil.rmtree(folder)
