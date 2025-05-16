import requests
import base64
import os
from dotenv import load_dotenv
import datetime

from sharedMethods.askGPT import classifyProposal, getKeyWords
from sharedMethods.stageUpgrades import getStageUpgrades

def sendToObsidian(obsidianFile, apiFile):
    path = f"Obsidian_TC39_Proposals/Proposals/{obsidianFile}"

    with open(f"{apiFile}/outputMD/apiResults.md", "r") as file:
        fileContent = file.readlines()

    data_list = []
    for line in fileContent:
        # remove whitespace/newline
        stripped = line.strip()
        # create dictionary from stripped line
        item = eval(stripped)
        # collect it
        data_list.append(item)

    # Iterate over each dictionary and use pattern matching
    for entry in data_list:
        match entry:
            case {
                "Title": title,
                "Author(s)": authors,
                "Champion(s)": champions,
                "Date": date,
                "Link Titles": link_titles,
                "GitHub Link": github_link,
                "GitHub Note Link": github_note_link
            }:

                link_title = link_titles.strip("[[]]")

                invalid_chars = '\\/*?:"<>|'

                for char in invalid_chars:
                    link_titles = link_title.replace(char, "")

                file_path = os.path.join(path, f"{link_titles}.md")

                # Check if the file already exists
                if os.path.exists(file_path):
                    print(f"File '{link_titles}' already exists. Skipping...")
                    continue 

                try:
                    apiProposalName = github_link.split("/")[-1]
                    if "#" in apiProposalName:
                        apiProposalName = apiProposalName.split("#")[0]
                except:
                    print("Error with link:", link_title)

                try:
                    # default branch called main
                    try: 
                        commitDate = f"https://api.github.com/repos/tc39/{apiProposalName}/branches/main"

                        commitDateResponse = requests.get(commitDate, auth=(os.getenv("USERNAME"), os.getenv("API_KEY")))
                        commitDate = commitDateResponse.json()
                        commitDateIso = commitDate["commit"]["commit"]["author"]["date"]
                        commitDate = commitDateIso.split("T")
                        returnDate = commitDate[0]

                    # default branch called master
                    except:
                        commitDate = f"https://api.github.com/repos/tc39/{apiProposalName}/branches/master"

                        commitDateResponse = requests.get(commitDate, auth=(os.getenv("USERNAME"), os.getenv("API_KEY")))
                        commitDate = commitDateResponse.json()
                        commitDateIso = commitDate["commit"]["commit"]["author"]["date"]
                        commitDate = commitDateIso.split("T")
                        returnDate = commitDate[0]
                except:
                    returnDate = None

                try:
                    stageUpgrades = getStageUpgrades(github_link).strip()
                    print(stageUpgrades)
                except:
                    stageUpgrades = None
                    print("error with getStageUpgrade for", github_link)

                #----------api call for readme------------------------
                try:
                    load_dotenv()
                    githubReadme = f"https://api.github.com/repos/tc39/{apiProposalName}/contents/README.md"
                    response = requests.get(githubReadme, auth=(os.getenv("USERNAME"), os.getenv("API_KEY")))
                    data = response.json()
                    file_content = base64.b64decode(data["content"]).decode("utf-8")

                    keywords = getKeyWords(title, file_content)

                    with open(f"Obsidian_TC39_Proposals/Analysis/Keywords/Terms.md", "a") as keywordList:
                        keywordList.write(f"Proposal: {link_titles} \n {keywords}\n\n")


                    print(keywords)

                    try: 
                        print("sending", link_titles, "to GPT for processing")
                        classification = str(classifyProposal(link_titles, file_content))
                        print("gpt response", classification)
                    except:
                        print("error with asking open ai:", title)
                except:
                    print("Error with link:", link_titles)
                    with open(f"Obsidian_TC39_Proposals/Proposals/{obsidianFile}/{link_titles}.md", "w") as proposals:
                        proposals.write(
                            f"[[{obsidianFile}]]<br>"
                            f"Classification<br>"
                            f"Human Validated: No<br>"
                            f"Title: {title}<br>"
                            f"Authors: {authors}<br>"
                            f"Champions: {champions}<br>"
                            f"Last Presented: {date}<br>"
                            f"Stage Upgrades:<br>{stageUpgrades}<br>"
                            f"Last Commit: {returnDate}<br>"
                            f"Keywords:<br>"
                            f"GitHub Link: {github_link} <br>"
                            f"GitHub Note Link: {github_note_link}\n"
                            f"# Proposal Description:<br>"
                    )
                    continue
                #-----------------------------------------------------
                with open(f"Obsidian_TC39_Proposals/Proposals/{obsidianFile}/{link_titles}.md", "w") as proposals:
                    proposals.write(
                        f"[[{obsidianFile}]]<br>"
                        f"Classification: {classification}<br>"
                        f"Human Validated: No<br>"
                        f"Title: {title}<br>"
                        f"Authors: {authors}<br>"
                        f"Champions: {champions}<br>"
                        f"Last Presented: {date}<br>"
                        f"Stage Upgrades:<br>{stageUpgrades}<br>"
                        f"Last Commit: {returnDate}<br>"
                        f"Keywords: {keywords}<br>"
                        f"GitHub Link: {github_link} <br>"
                        f"GitHub Note Link: {github_note_link}\n"
                        f"# Proposal Description:\n{file_content}<br>"
                    )
