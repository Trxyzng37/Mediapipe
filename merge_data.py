import os
import numpy as np
import csv

folder_name = str(input("Enter folder type: train/val/test\n"))
folder_path = f"data_set/data/{folder_name}"

if os.path.exists(folder_path):
    pass
else:
    print("Folder not exist.......\n")
    exit

f = open(f"{folder_path}/{folder_name}.csv", 'w')

# loop through each CSV file in the folder_path
for item in os.listdir(folder_path):
    if item.endswith('.csv') and item != f"{folder_name}.csv":
        with open(f"{folder_path}/{item}", 'r') as f:
            reader = csv.reader(f)
            with open(f"{folder_path}/{folder_name}.csv", 'a', newline='') as g:
                writer = csv.writer(g)
                for row in reader:
                    writer.writerow(row)
print(f"Write data to {folder_name}.csv")
print("Finished...")