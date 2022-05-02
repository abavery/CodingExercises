from typing import List

import pandas as pd
import os
import sys


def get_files(searchdir=None) -> List[str]:
    allfiles = []

    if searchdir is None:
        searchdir = os.getcwd()

    for root, dirs, files in os.walk(searchdir):
        for file in files:
            allfiles.append(os.path.join(root, file))

    return allfiles


def create_frame(filepath) -> pd.DataFrame:
    extension = get_extension(filepath)

    if extension == '.csv':
        return pd.read_csv(filepath)

    if extension == '.dat':
        return pd.read_csv(filepath)

    if extension == '.json':
        return pd.read_json(filepath)

    if extension == '.xml':
        return pd.read_xml(filepath)


def get_extension(filepath) -> str:
    return os.path.splitext(filepath)[1]


def generate_report(searchdir=None, simplefilter=None) -> pd.DataFrame:
    filenames = get_files(searchdir)

    df = None
    for file in filenames:
        tempframe = create_frame(file)
        if tempframe is None:
            print('Error reading file: ' + file)
            continue

        tempframe['source'] = file

        if df is None:
            df = tempframe
        else:
            df = pd.concat([df, tempframe], ignore_index=True)

    if df is None:
        return

    if simplefilter is not None:
        df = simple_filter(simplefilter, df)

    outputdir = './Output/'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    df.to_csv('Output/consolidated_output.1.csv')

    return df


# TODO finish this function to parse a simple statement with a column name, operand, and a comparison value
def simple_filter(filterstatement: str, df: pd.DataFrame) -> pd.DataFrame:
    values = filterstatement.split()

    if len(values) != 3:
        return

    if values[0] not in df.columns:
        return

    if values[1] not in ['=', '>', '<', '>=', '<=']:
        return

    if not values[2].isdecimal():
        return

    compnumber = float(values[2])

    if values[1] == '=':
        return df.loc[df[values[0]] == compnumber]

    if values[1] == '>':
        return df.loc[df[values[0]] > compnumber]

    if values[1] == '<':
        return df.loc[df[values[0]] < compnumber]

    if values[1] == '>=':
        return df.loc[df[values[0]] >= compnumber]

    if values[1] == '<=':
        return df.loc[df[values[0]] <= compnumber]

    # TODO validate column name somehow

    return values


if __name__ == '__main__':
    # I don't love this method of finding the number of args passed, but I don't have a better solution yet
    # TODO research *argv. This may be a clean solution to iterate args including allowing multiple filters
    if len(sys.argv) == 1:
        generate_report()

    if len(sys.argv) == 2:
        generate_report(sys.argv[1])
    else:
        generate_report(sys.argv[1], sys.argv[2])
