import os
import numpy as np
import csv

folder_name = ["train","val","test"]
folder_path = f"data_set/data/"

if os.path.exists(folder_path):
    pass
else:
    print("Folder not exist.......\n")
    exit

for h in folder_name:
    f = open(f"{folder_path}/{h}/{h}.csv", 'w')

for i in folder_name:
# loop through each CSV file in the folder_path
    for item in os.listdir(f"{folder_path}/{i}"):
        if item.endswith('.csv') and item != f"{i}.csv":
            with open(f"{folder_path}/{i}/{item}", 'r') as f:
                reader = csv.reader(f)
                with open(f"{folder_path}/{i}/{i}.csv", 'a', newline='') as g:
                    writer = csv.writer(g)
                    for row in reader:
                        writer.writerow(row)
    print(f"Write data to {i}.csv")
print("Finished...")