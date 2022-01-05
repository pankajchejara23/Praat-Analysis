import pandas as pd

# Trim white spaces from the string
def trim_white_newline(string):
    new_list = list()
    for item in string:
        if item == '' or item == '\n':
            pass
        else:
            new_list.append(item)
    return new_list

# Open Praat Transcribe File
f = open('group-2_single_channel.TextGrid')

# Read lines from the file
lines = f.readlines()

# Create a empty dataframe for storing transcribe data
df = pd.DataFrame(columns = ["start","end","user"])


line_count = 0
read_flag = False

# Iterate over all lines one by one
for line in lines:
    # read flag is true. This flag specify that the next line is the data line.
    if read_flag:

        # Increase line count
        line_count = line_count + 1

        # Condition to read only three lines. 
        # Each data transciption has three lines.
        if line_count < 4:
            # Split the line using space.
            words = line.split(" ")

            # Remove white spaces
            words = trim_white_newline(words)

            # First token as start time of the frame
            if line_count == 1:
                start = float(words[2])
            # Second token as end time of the frame
            if line_count == 2:
                end = float(words[2])
            # third token as annotatation
            if line_count == 3:
                user = words[2]
                user = user.replace('"','')
        # When all three lines are read.
        else:
            line_count=0
            read_flag = False

            # Append data to dataframe
            df = df.append({'start':start,'end':end,'user':user},ignore_index = True)

    # Condition to check if current line has 'intervals [' string
    elif line.find('intervals [')==-1:
        pass
    else:
        read_flag = True

# Computer annotated window time
df["speaking"] = df["end"] - df["start"]

# Save to csv format.
df.to_csv('annotated.csv')        
