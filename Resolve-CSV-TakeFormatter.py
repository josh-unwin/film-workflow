#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

__programName__ = "Resolve-CSV-TakeFormatter"
__description__ = "Takes a Resolve metadata CSV and converts take from default sound format to commonly used editorial format. Eg: A Cam take 01 becomes 1a"
__author__ = "Josh Unwin"
__version__ = "0.1"

import csv
import sys
import os
import argparse

# Method for processing the ALEs.
def csv_parser(inputCsv):
    with open(inputCsv, 'r', encoding='utf-16') as csv_file:
        csv_reader = csv.reader(csv_file)
        outputFilePath = os.path.dirname(inputCsv) + "/_" + os.path.basename(inputCsv).split(".")[0] + '_take-formatted.csv'

        with open(outputFilePath, 'w', newline='', encoding='utf-16') as new_file:
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

                if take[0] == "0":
                    take = take[1:]
                new_take = take + cam_letter
                line[take_column] = new_take
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