#########################################################################################################
#
# Run this script like this from project root: 
# 
# For extracting stages:
# python sharedMethods/getDataForScatterplot.py stage 4
# python sharedMethods/getDataForScatterplot.py stage 3
# python sharedMethods/getDataForScatterplot.py stage Inactive
# 
#########################################################################################################

import sys
import os
import re
import csv


def extractBumpsAndCommit(title, completePath):
    data = []

    with open(completePath, "r") as file:

        data.append(title)

        fileContent = file.read()
        match = re.search(r"Stage 1:\s+([^\s<]+)", fileContent)
        print("Stage 1:", match.group(1).strip())
        data.append(match.group(1).strip())

        match = re.search(r"Stage 2:\s+([^\s<]+)", fileContent)
        print("Stage 2:", match.group(1).strip())
        data.append(match.group(1).strip())
        
        match = re.search(r"Stage 2.7:\s+([^\s<]+)", fileContent)
        print("Stage 2.7:", match.group(1).strip())
        data.append(match.group(1).strip())
        
        match = re.search(r"Stage 3:\s+([^\s<]+)", fileContent)
        print("Stage 3:", match.group(1).strip())
        data.append(match.group(1).strip())

        match = re.search(r"Stage 4:\s+([^\s<]+)", fileContent)
        print("Stage 4:", match.group(1).strip())
        data.append(match.group(1).strip())

        match = re.search(r"Last Commit:\s+([^\s<]+)", fileContent)
        print("Last Commit:", match.group(1).strip())
        data.append(match.group(1).strip())

    return data

def getStageBumpsAndLastCommit(stage):

    stagesAndLastCommit = []

    print("Extracting:", stage)

    if stage == "Inactive":
        path = f"Obsidian_TC39_Proposals/Proposals/{stage}/"
    else: 
        path = f"Obsidian_TC39_Proposals/Proposals/Stage {stage}/"

    print("Path:", path)

    stagesAndLastCommit.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit"])
    
    for each in os.listdir(path):
        
        try:

            completePath = os.path.join(path, each)
        
            title = each.split(".md")[0]

            print(title)

            stagesAndLastCommit.append(extractBumpsAndCommit(title, completePath))

        except Exception as e:
            print(f"Error with: {fullPath} - {e}")

    with open(f"Data Analysis/CSVFiles/CSVStages/Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(stagesAndLastCommit)




#########################################################################################################
#
# Run this script like this from project root: 
# 
# For extracting classifications (in lowercase): 
# python sharedMethods/getDataForScatterplot.py change api
# python sharedMethods/getDataForScatterplot.py change semantic
# python sharedMethods/getDataForScatterplot.py change syntactic
#
# For extracting specific stages with classifications (in lowercase): 
# python sharedMethods/getDataForScatterplot.py change api stage 4
# python sharedMethods/getDataForScatterplot.py change semantic stage 4
# python sharedMethods/getDataForScatterplot.py change syntactic stage 4
#
# In order to extract specific stages (separate for example semantic from semanic AND syntactic):
#
# python sharedMethods/getDataForScatterplot.py specific-change api
# python sharedMethods/getDataForScatterplot.py specific-change semantic
# python sharedMethods/getDataForScatterplot.py specific-change syntactic
#
#########################################################################################################

def extractProposalsWithClassification(keyword):

    classifications = []

    cleanKeyword = keyword.strip("[[]]")

    classifications.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])

    path = "Obsidian_TC39_Proposals/Proposals"

    for stages in os.listdir(path):
        stagePath = os.path.join(path, stages)

        if os.path.isdir(stagePath):
            print(f"########################### Extracting from {stages} ###########################")
            for proposal in os.listdir(stagePath):
                try:
                    title = proposal.split(".md")[0]
                    
                    fullPath = os.path.join(stagePath, proposal)

                    with open(fullPath, "r") as proposal:
                        content = proposal.read()
                        if keyword in content:
                            print(title)
                            bump = extractBumpsAndCommit(title, fullPath)
                            bump.append(cleanKeyword)
                            classifications.append(bump)
                                                 
                except Exception as e:
                    print(f"Error with: {fullPath} - {e}")
                    
    with open(f"Data Analysis/CSVFiles/CSVChanges/{cleanKeyword}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(classifications)


def extractStageWithClassification(keyword, stage):

    classifications = []

    cleanKeyword = keyword.strip("[[]]")

    classifications.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])

    if stage == "Inactive":
        path = f"Obsidian_TC39_Proposals/Proposals/{stage}/"
    else: 
        path = f"Obsidian_TC39_Proposals/Proposals/Stage {stage}/"

    print(f"########################### Extracting from {stage} ###########################")

    for proposal in os.listdir(path):
        try:
            title = proposal.split(".md")[0]
            
            fullPath = os.path.join(path, proposal)
            with open(fullPath, "r") as proposal:
                content = proposal.read()
                if keyword in content:
                    print(title)
                    bump = extractBumpsAndCommit(title, fullPath)
                    bump.append(cleanKeyword)
                    classifications.append(bump)
                                         
        except:
            print(f"Error with: {fullPath} - {e}")
                    
    with open(f"Data Analysis/CSVFiles/CSVChanges/{cleanKeyword} Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(classifications)

def getNonCrossoverClassifiedChanges(stage):
    api_syn_sem = []
    api_syn = []
    api_sem = []
    syn_sem = []
    syn = []
    sem = []
    api = []

    classificationKeywords = set()

    api_syn_sem.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])
    api_syn.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])
    api_sem.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])
    syn_sem.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])
    syn.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])
    sem.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])
    api.append(["Title", "Stage 1", "Stage 2", "Stage 2.7", "Stage 3", "Stage 4", "Last Commit", "Classification"])

    if stage == "Inactive":
        path = f"Obsidian_TC39_Proposals/Proposals/{stage}/"
    else: 
        path = f"Obsidian_TC39_Proposals/Proposals/Stage {stage}/"

    if os.path.isdir(path):
        print(f"########################### Extracting from {stage} ###########################")
        for proposal in os.listdir(path):
            try:
                title = proposal.split(".md")[0]
                
                fullPath = os.path.join(path, proposal)
                with open(fullPath, "r") as proposal:
                    content = proposal.read()
                    if "[[API Change]]" in content and "[[Syntactic Change]]" in content and "[[Semantic Change]]" in content:
                        print(title)
                        bump = extractBumpsAndCommit(title, fullPath)
                        api_syn_sem.append(bump)

                    if "[[API Change]]" in content and "[[Syntactic Change]]" in content and "[[Semantic Change]]" not in content:
                        print(title)
                        bump = extractBumpsAndCommit(title, fullPath)
                        api_syn.append(bump)

                    if "[[API Change]]" in content and "[[Semantic Change]]" in content and "[[Syntactic Change]]" not in content:
                        print(title)
                        bump = extractBumpsAndCommit(title, fullPath)
                        api_sem.append(bump)

                    if "[[Syntactic Change]]" in content and "[[Semantic Change]]" in content and "[[API Change]]" not in content:
                        print(title)
                        bump = extractBumpsAndCommit(title, fullPath)
                        syn_sem.append(bump)

                    if "[[Syntactic Change]]" in content and "[[Semantic Change]]" not in content and "[[API Change]]" not in content:
                        print(title)
                        bump = extractBumpsAndCommit(title, fullPath)
                        syn.append(bump)

                    if "[[Semantic Change]]" in content and "[[Syntactic Change]]" not in content and "[[API Change]]" not in content:
                        print(title)
                        bump = extractBumpsAndCommit(title, fullPath)
                        sem.append(bump)

                    if "[[API Change]]" in content and "[[Semantic Change]]" not in content and "[[Syntactic Change]]" not in content:
                        print(title)
                        bump = extractBumpsAndCommit(title, fullPath)
                        api.append(bump)

            except Exception as e:
                print(f"Error with: {fullPath} - {e}")


    with open(f"Data Analysis/CSVFiles/SpecificChanges/Stage {stage}/api_syn_sem Specific Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(api_syn_sem)
    
    with open(f"Data Analysis/CSVFiles/SpecificChanges/Stage {stage}/api_syn Specific Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(api_syn)

    with open(f"Data Analysis/CSVFiles/SpecificChanges/Stage {stage}/api_sem Specific Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(api_sem)

    with open(f"Data Analysis/CSVFiles/SpecificChanges/Stage {stage}/syn_sem Specific Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(syn_sem)

    with open(f"Data Analysis/CSVFiles/SpecificChanges/Stage {stage}/syn Specific Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(syn)

    with open(f"Data Analysis/CSVFiles/SpecificChanges/Stage {stage}/sem Specific Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sem)

    with open(f"Data Analysis/CSVFiles/SpecificChanges/Stage {stage}/api Specific Stage {stage}.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(api)
       
def getClassifiedChanges(change):
    print("Extracting:", change)

    if change == "api":
        keyword = "[[API Change]]"
        extractProposalsWithClassification(keyword)
    elif change == "syntactic":
        keyword = "[[Syntactic Change]]"
        extractProposalsWithClassification(keyword)
    elif change == "semantic":
        keyword = "[[Semantic Change]]"
        extractProposalsWithClassification(keyword)
    else:
        print("Error in getClassificationChanges method")
        return


def getStageSpecificClassifiedChanges(change, stage):
    print("Extracting:", change)

    if change == "api":
        keyword = "[[API Change]]"
        extractStageWithClassification(keyword, stage)
    elif change == "syntactic":
        keyword = "[[Syntactic Change]]"
        extractStageWithClassification(keyword, stage)
    elif change == "semantic":
        keyword = "[[Semantic Change]]"
        extractStageWithClassification(keyword, stage)
    else:
        print("Error in getClassificationChanges method")
        return



    


if __name__ == "__main__":

    if len(sys.argv) == 3:
        if sys.argv[1] == "stage":
            stage = sys.argv[2]
            getStageBumpsAndLastCommit(stage)
        elif sys.argv[1] == "change":
            change = sys.argv[2]
            getClassifiedChanges(change)
    elif len(sys.argv) == 4: 
        if sys.argv[1] == "noncrossover" and sys.argv[2] == "stage":
            stage = sys.argv[3]
            getNonCrossoverClassifiedChanges(stage)
    elif len(sys.argv) == 5: 
        if sys.argv[1] == "change" and sys.argv[3] == "stage":
            change = sys.argv[2]
            stage = sys.argv[4]
            getStageSpecificClassifiedChanges(change,stage)  
        

    
    
