"""
Get and organize images needed from the Hagrid dataset.

Organize like rock, paper, scissors dataset.

folder_name/
-menu/ (peace inverted)
-three/ (three)
-four/ (four)
-five/ (palm)
"""

import os
import shutil
import kagglehub

def get_hagrid_data():
    # Download latest version
    path = kagglehub.dataset_download("innominate817/hagrid-sample-30k-384p")

    print("Path to dataset files:", path)

    home_path = os.path.expanduser("~")
    data_folder = f"{home_path}/jester_data"
    os.makedirs(data_folder, exist_ok=True)

    folders_needed = {
        "train_val_peace_inverted": "menu", 
        "train_val_three": "three", 
        "train_val_four": "four", 
        "train_val_palm": "five",
        "train_val_fist": "move",
        "train_val_stop": "run",
        "train_val_peace": "two",
        "train_val_one": "one",
    }

    for hagrid_folder in os.listdir(f"{path}/hagrid-sample-30k-384p/hagrid_30k"):
        if hagrid_folder in folders_needed.keys():
            print(f"\033[95mMoving images in {hagrid_folder} to {folders_needed[hagrid_folder]}.\033[0m")

            src_path = f"{path}/hagrid-sample-30k-384p/hagrid_30k/{hagrid_folder}/"
            dst_path = f"{data_folder}/{folders_needed[hagrid_folder]}"

            os.makedirs(dst_path, exist_ok=True)
            
            # Move every file in src_path
            for file in os.listdir(src_path):
                src_file = os.path.join(src_path, file)
                dst_file = os.path.join(dst_path, file)
                shutil.move(src_file, dst_file)




if __name__ == "__main__":
    get_hagrid_data()