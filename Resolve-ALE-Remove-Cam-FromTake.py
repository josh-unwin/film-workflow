#!/usr/local/bin/python3

__programName__ = "Resolve ALE - Remove Cam from Take"
__description__ = "Removes the cam letter from the Take column if present"
__author__ = "Josh Unwin"
__version__ = "0.3"

import csv
import sys
import os
import argparse
import re

# Method for processing the ALEs.
def ale_parser(inputAle):
    with open(inputAle, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        outputFilePath = os.path.dirname(inputAle) + "/_" + os.path.basename(inputAle).split(".")[0] + '_take-cam-removed.ale'

        with open(outputFilePath, 'w') as new_file:
            csv_writer = csv.writer(new_file, delimiter='\t')

            past_data_row = False
            take_column = None
            for line in csv_reader:
              if "Take" in line:
                  take_column = line.index("Take")
              if past_data_row == False:
                csv_writer.writerow(line)
              else:
                  new_take_column = re.sub(r"[a-z]", "", line[take_column])
                  line[take_column] = new_take_column
                  csv_writer.writerow(line)
              try:
                if line[0] == "Data":
                  past_data_row = True
              except:
                pass
    return outputFilePath


# Args Parse Method, allows user input and provides feedback.
def args_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('resolveAles', nargs='+', help="A list of paths to Resolve ALE's you wish to modify.")
    return parser.parse_args()


# Main Method. Runs both methods.
def main():
    args = args_parse()
    listOfAles = args.resolveAles

    for ale in listOfAles:
        outputAle = ale_parser(ale)
        print("Exported file: " + os.path.basename(outputAle))

    print("\nFinished! " + __programName__ + " - Version "+ __version__+ ", written by "+__author__)

# Runs when opened from command line
if __name__ == '__main__':
    main()
