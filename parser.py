import argparse
import json

from pathlib import Path
from os import path

def __init__(self) -> None:
    pass

def readCommands(file):
    with open(file , "r+") as f:
        data = json.load(f)
        return data

def findCommands(data):
    commandlist = dict()
    with open('scripts/Invoke-AppLocker.ps1', encoding="utf8") as f:
        read_data = f.read()
        for x in data:
            for r in read_data.split():
                if x['Name'] == r:
                    if x['Name'] in commandlist:
                        commandlist[x['Name']] += 1
                    else:
                        commandlist[x['Name']] = 1    
    
    return commandlist

def main():
    parser = argparse.ArgumentParser(description="Parses selected PowerShell scripts for cmdlets, functions, and aliases")
    parser.add_argument("-s", "--single", type=Path, help="Process single file only", action="store_true") 

    args = parser.parse_args()
    pathf = "commands.json"
    file = Path(pathf)

    if not(path.exists("commands.json")):
        print("Missing commands.json file!")
        exit()

    data = readCommands(file) 

    commandlist = findCommands(data)
    print(commandlist)
    
    with open("output.json", 'w') as outfile:
        json.dump(commandlist, outfile)

if __name__ == "__main__":
    main()