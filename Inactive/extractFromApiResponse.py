# Import extractTitle from processApiResponse
from sharedMethods.processApiResponse import prepText, extractDetails

# Open and read the file content
with open("Inactive/outputMD/apiResponse.md", "r") as file:
    fileContent = file.read()

rawText = prepText(fileContent)

extractResults = extractDetails(rawText, fileContent)

with open("Inactive/outputMD/apiResults.md", "w") as results:
    for each in extractResults:
        if "error with this link:" not in each:
            results.write(str(each) + "\n")

#### Uncomment this to send proposals to obsidian as a single file
#
#with open("Obsidian_TC39_Proposals/Proposals/Inactive.md", "w") as results:
#    results.write("#InactiveTag\n")
#    for each in extractResults:
#        if "error with this link:" not in each:
#            results.write(str(each) + "\n")
