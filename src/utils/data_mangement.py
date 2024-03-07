import os
import glob

def get_most_recent_file(directory, prefix):
    files = glob.glob(os.path.join(directory, prefix + '*'))
    if not files:
        return None, None
    
    file_number = [i.split('_')[1].replace('ciclo', '') for i in files]
    return directory+prefix + str(max(file_number)), max(file_number).split('.')[0]

def get_available_files(directory, prefix):
    files = glob.glob(os.path.join(directory, prefix + '*'))
    return files

