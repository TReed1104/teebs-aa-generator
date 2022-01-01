## Imports
from argparse import ArgumentParser
import os
import json

## Read the file
def readFileToString(fileName):
    parsedFile = ""
    try:
        ## Open the file, read the contents into a string keeping formatting
        fileContent = open(fileName, "r")
        for line in fileContent:
            parsedFile += line
        fileContent.close()
        return parsedFile

    ## Error Handling
    except (OSError, IOError) as error:
        print(">>> ERROR! - An error occured:", error)
        ## Returns a blank string to prevent execution halt
        return parsedFile

## Write the output AAs to file
def writeStringToFile(fileName, stringToWrite):
    try:
        ## Create a new file, write the string to the file and save it
        outputFile = open(fileName, "w")
        outputFile.write(stringToWrite)
        outputFile.close()

    ## Error Handling
    except (OSError, IOError) as error:
        print(">>> ERROR! - An error occured:", error)

## Input the raid member names
def setRaidAssignments(fileName):
    ## Program flow print - more for debugging than anything
    print(">> Parsing Template:", fileName)

    ## Read in the AA file
    fileData = readFileToString(inputDirectory + fileName)

    ## Find and replace assignment tokens e.g. <tank_0>
    for placeholderToken in configData["assignments"]:
        ## Check the placeholder has a value to set
        if placeholderToken != "":
            ## Replace the placeholder with the raider name, formatted with their class colour
            fileData = fileData.replace(f"<{placeholderToken}>", getFormattedRaidersName(placeholderToken))

    ## Save the parsed AA to an output file
    writeStringToFile(outputDirectory + fileName, fileData)

## Get the raider information to replace the placeholder token with
def getFormattedRaidersName(placeholder):
    ## Get the raider details from the config file
    raiderName = configData["assignments"][placeholder]
    raiderClass = configData["roster"][raiderName]

    ## Format the raider name with their class colour in the format WoW uses for colouring text |c<Colour><Text>|r
    formattedRaiderName = f"|c{raiderClass}{raiderName}|r"
    return formattedRaiderName

## Main thread check
if __name__ == '__main__':
    ## Setup the file directories
    inputDirectory = "templates/"
    outputDirectory = "bin/"

    ## Setup the command-line arguments
    argParser = ArgumentParser(description='A Python app for quickly generating AngryAssignment messages for WoW TBC-Classic')
    argParser.add_argument("-i", "--input", dest="config", help="The config file to use", type=str, default="config.json")

    ## Parse the arguments from the command line to be usable
    args = argParser.parse_args()

    ## Load the config json 
    configFile = open(args.config)
    configData = json.load(configFile)
    configFile.close()

    ## Entry point output, just for context in the command-line
    print("> Generating AngryAssignments")

    ## Create the output directory
    try:
        print(">> Creating the output directory")
        os.makedirs(outputDirectory)
    except FileExistsError:
        pass

    ## Iterate through the templates found in the specified directory
    for fileToParse in os.listdir(inputDirectory):
        ## Parse the files and replace the values with the assigned raiders
        setRaidAssignments(fileToParse)
