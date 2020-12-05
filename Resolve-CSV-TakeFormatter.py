__programName__ = "Resolve-CSV-TakeFormatter"
__description__ = "Takes a Resolve metadata CSV and converts take from default sound format to commonly used editorial format. Eg: A Cam take 01 becomes 1a"
__author__ = "Josh Unwin"
__version__ = "0.1"

import csv
import sys
import os
import argparse
import re

# Method for processing the ALEs.
def csv_parser(inputCsv):
    with open(inputCsv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        outputFilePath = os.path.dirname(inputCsv) + "/_" + os.path.basename(inputCsv).split(".")[0] + '_take-formatted.csv'

        with open(outputFilePath, 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)

            take_column = None
            file_name_column = None
            for line in csv_reader:
              if "Take" in line:
                  take_column = line.index("Take")
                  file_name_column = line.index("File Name")
                  csv_writer.writerow(line)
              else:
                cam_letter = line[file_name_column][0].lower()
                take = line[take_column]

                if take != "":
                    if re.match("\d{1,2}_\w{1,2}", take):
                        split_take = take.split("_")
                        split_take.insert(1, cam_letter + "_")
                        new_take = "".join(split_take)
                        line[take_column] = new_take
                    elif take[-1] != cam_letter:
                        new_take = take + cam_letter
                        line[take_column] = new_take
                        
                csv_writer.writerow(line)

    return outputFilePath


# Args Parse Method, allows user input and provides feedback.
def args_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('resolveCsvs', nargs='+', help="A list of paths to Resolve CSV's you wish to modify.")
    return parser.parse_args()


# Main Method. Runs both methods.
def main():
    args = args_parse()
    listOfCsvs = args.resolveCsvs

    for csv in listOfCsvs:
        outputCsv = csv_parser(csv)
        print("Exported file: " + os.path.basename(outputCsv))

    print("\nFinished! " + __programName__ + " - Version "+ __version__+ ", written by "+__author__)

# Runs when opened from command line
if __name__ == '__main__':
    main()
