
from datetime import datetime, timedelta
import shutil
import os
pname = "smaato"






# Get the current date
current_date = datetime.today()
current_date_formatted = current_date.strftime("%Y%m%d")

# Calculate the previous date by subtracting one day
previous_date = current_date - timedelta(days=1)

# Format the previous date as desired (e.g., YYYYMMDD)
previous_date_formatted = previous_date.strftime("%Y%m%d")

print(current_date_formatted)
print(previous_date_formatted)



ink_file_name = pname + "_" + previous_date_formatted +".csv"
if pname == "loopme":
    ink_file_name = pname + "_" + previous_date_formatted +".csv"



# Specify the source and destination directories
source_directory = os.path.dirname(__file__) + "/attachment"
destination_directory = os.path.dirname(__file__) + "/attachment/" + previous_date_formatted


# Check if the directory exists
if not os.path.exists(destination_directory):
    # Create the directory
    os.makedirs(destination_directory)
    print(f"Directory '{destination_directory}' created successfully")
else:
    print(f"Directory '{destination_directory}' already exists")



# Get a list of files in the source directory
files = os.listdir(source_directory)

#Sensedigital_dealid_statistics_2024-04-14-2024-05-13.csv.zip

not_in_use_substring = "Sensedigital_Amazon_dealids"
in_use_substring = ".csv"
# Iterate over each file in the source directory
for file_name in files:

    if not_in_use_substring in file_name:
        source_file_path = os.path.join(source_directory, file_name)
        os.remove(source_file_path)
        print("Not need to use this. Deleting this file .... ")
    else:
        if in_use_substring in file_name:
            print(file_name)
            # Get the full path of the file
            source_file_path = os.path.join(source_directory, file_name)
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(source_file_path):
                # Move the file to the destination directory
                destination_directory = os.path.join(destination_directory, ink_file_name)
                shutil.move(source_file_path, destination_directory)
