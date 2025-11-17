import pandas as pd
import kagglehub
import shutil 

def get_asl_data():

  # Download latest version
  path = kagglehub.dataset_download("grassknoted/asl-alphabet")

  print("Path to dataset files:", path)

  os.makedirs("data", exist_ok=True)

  #files needed (R, J, M, T, )
  folders_needed = {"R":"Action", "J":"Journal", "M":"Map", "T":"Toolbar"}

  for asl_folders in os.listdir(f"{path}/asl_alphabet_train/asl_alphabet_train"):
    if asl_folders in folders_needed.keys():
      print(f"\033[95mMoving images in {asl_folders} to {folders_needed[asl_folders]}.\033[0m")

      src_path = f"{path}/asl_alphabet_train/asl_alphabet_train/{asl_folders}/"
      dst_path = f"data/{folders_needed[asl_folders]}"

      os.makedirs(dst_path, exist_ok=True)
      
      # Move every file in src_path
      for file in os.listdir(src_path):
          src_file = os.path.join(src_path, file)
          dst_file = os.path.join(dst_path, file)
          shutil.move(src_file, dst_file)


if __name__ == "__main__":
  get_asl_data()