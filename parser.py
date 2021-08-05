import os
import csv
import re
import json
import argparse
import pandas as pd

from pathlib import Path
from os import path

def __init__(self) -> None:
    pass

def readCommands(file: Path) -> str:
    with open(file , "r+") as f:
        data = json.load(f)
        return data

def parseAll(commands: str, folderpath: Path, commandlist: dict) -> dict:

    for filename in os.listdir(folderpath):
        if filename.endswith(".ps1"):
            scriptName = str(filename)
            filepath = os.path.join(folderpath, filename)
            with open(filepath, encoding="utf8") as f:
                read_data = f.read()
                commandlist[scriptName] = {}
                for command in commands:
                    for scriptWord in read_data.split():
                        if scriptWord == command['Name']:
                            try:
                                commandlist[scriptName][scriptWord] += 1
                            except:
                                commandlist[scriptName][scriptWord] = 1
    
    return commandlist
                

def parseSingle(commands: str, folderpath: Path, filename: Path, commandlist: dict) -> dict:

    filepath = os.path.join(folderpath, filename)

    with open(filepath, encoding="utf8") as f:
        read_data = f.read()

        scriptName = str(filename)
        commandlist[scriptName] = {}
        
        for command in commands:
            for scriptWord in read_data.split():
                if scriptWord == command['Name']:
                    try:
                        commandlist[scriptName][scriptWord] += 1
                    except:
                        commandlist[scriptName][scriptWord] = 1

    return commandlist

def findCommands(commands: str, folderpath: Path, filename: Path) -> list:
    commandlist = dict()

    if filename:
        commandlist = parseSingle(commands, folderpath, filename, commandlist) 
    else:
        commandlist = parseAll(commands, folderpath, commandlist)
    
    return commandlist

def convertToCSV():
    df = pd.read_json('output.json')
    df.to_csv('output.csv', index=None)

def main():
    parser = argparse.ArgumentParser(description="Parses PowerShell script from the selected folder")
    parser.add_argument("folderpath", type=Path, help="Select the folder path that contains the script(s)")
    parser.add_argument("-s", "--single", type=Path, help="Process single file only, specifiy the PowerShell script") 
    parser.add_argument("-c", "--csv", action="store_true", help="Outputs to CSV instead of JSON")

    args = parser.parse_args()

    pathf = "commands.json"
    file = Path(pathf)

    if not(path.exists("commands.json")):
        print("Missing commands.json file!")
        exit()

    commands = readCommands(file) 

    commandlist = findCommands(commands, args.folderpath, args.single)

    with open("output.json", 'w') as outfile:
        json.dump(commandlist, outfile)

    convertToCSV()

if __name__ == "__main__":
    main()