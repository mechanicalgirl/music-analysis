import os
import sys

deletes = []

for d in deletes:
    print(d)
    try:
        os.remove(d)
    except Exception as e:
        print(e)
    try:
        folder_path = d.rpartition('/')[0]
        if len(os.listdir(folder_path)) == 0:
            print(f"Directory is empty, delete {d}")
            os.rmdir(folder_path)
    except Exception as e:
        print(e)

