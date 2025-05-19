import re

stage3Extract = []
stage2_7Extract = []
stage2Extract = []


def delegateDetails(fileContent):

    stage3Title = fileContent.index("### Stage 3\n")
    stage2_7Title = fileContent.index("### Stage 2.7\n")
    stage2Title = fileContent.index("### Stage 2\n")
    nextTitle = fileContent.index("## Contributing to proposals\n")

    links = fileContent[nextTitle:]

    stage3 = fileContent[stage3Title:stage2_7Title]
    stage3Extract.append(stage3)
    stage3Extract.append(links)

    stage2_7 = fileContent[stage2_7Title:stage2Title]
    stage2_7Extract.append(stage2_7)
    stage2_7Extract.append(links)

    stage2 = fileContent[stage2Title:nextTitle]
    stage2Extract.append(stage2)
    stage2Extract.append(links)

    with open("Stage_2_2_7_3/Stage_3/outputMD/delegatedApiResponse.md", "w") as results:
        for each in stage3Extract:
            if "error with this link:" not in each:
                results.write(str(each) + "\n")

    with open("Stage_2_2_7_3/Stage_2_7/outputMD/delegatedApiResponse.md", "w") as results:
        for each in stage2_7Extract:
            if "error with this link:" not in each:
                results.write(str(each) + "\n")

    with open("Stage_2_2_7_3/Stage_2/outputMD/delegatedApiResponse.md", "w") as results:
        for each in stage2Extract:
            if "error with this link:" not in each:
                results.write(str(each) + "\n")


#--------------------------Extraction--------------------------------#

# Open and read the file content
with open("Stage_2_2_7_3/outputMD/apiResponse.md", "r") as file:
    fileContent = file.read()

# Use the extractTitle function

delegateDetails(fileContent)

