#!/usr/bin/env python3

__programName__ = "Resolve ALE Clip Renamer"
__description__ = "Takes a list of Resolve ALE's, exports new versions with the Name column replaced with Scene-Take"
__author__ = "Josh Unwin"
__version__ = "0.3"

import csv
import sys
import os
import argparse
from datetime import datetime
import operator
from operator import itemgetter

# Method for processing the ALEs.
def ale_parser(inputAle):
    with open(inputAle, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        currentTime = datetime.now().strftime('%Y%m%d_%H%M%S')
        outputFilePath = os.path.dirname(inputAle) + "/_" + os.path.basename(inputAle).split(".")[0] + '_scene-take.ale'

        with open(outputFilePath, 'w') as new_file:
            csv_writer = csv.writer(new_file, delimiter='\t')

            past_data_row = False
            scene_column = None
            take_column = None
            for line in csv_reader:
              if "Scene" in line and "Take" in line:
                  scene_column = line.index("Scene")
                  take_column = line.index("Take")
              if past_data_row == False:
                csv_writer.writerow(line)
              else:
                line[0] = line[scene_column] + "-" + line[take_column]
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
