import ast
import requests
import base64
import os
from dotenv import load_dotenv

from sharedMethods.askGPT import classifyProposal

path = "Obsidian_TC39_Proposals/Proposals/Stage 0 Proposals"

with open("Stage_0/outputMD/apiResults.md", "r") as file:
    fileContent = file.readlines()

data_list = [ast.literal_eval(line.strip()) for line in fileContent]

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
                print("Cannot extract commitDate for", link_titles)
                returnDate = "None"

            #----------api call for readme------------------------
            
            try:
                load_dotenv()
                githubReadme = f"https://api.github.com/repos/tc39/{apiProposalName}/contents/README.md"
                response = requests.get(githubReadme, auth=(os.getenv("USERNAME"), os.getenv("API_KEY")))
                data = response.json()
                file_content = base64.b64decode(data["content"]).decode("utf-8")

                try: 
                    print("sending", link_titles, "to GPT for processing")
                    classification = str(classifyProposal(link_titles, file_content))
                    print("gpt response", classification)
                except:
                    print("error with asking open ai:", title)

            except:
                print("Error with link:", link_titles)
                with open(f"Obsidian_TC39_Proposals/Proposals/Stage 0 Proposals/{link_titles}.md", "w") as proposals:
                    proposals.write(
                        f"#Stage0Tag\n"
                        f"Classification:\n"
                        f"Human Validated: No\n"
                        f"Title: {title}\n"
                        f"Authors: {authors}\n"
                        f"Champions: {champions}\n"
                        f"Date: {date}\n"
                        f"Last Commit: {returnDate}\n"
                        f"GitHub Link: {github_link}\n"
                        f"GitHub Note Link: {github_note_link}\n\n"
                        f"# Proposal Description:\n"
                )
                continue

            #-----------------------------------------------------
            with open(f"Obsidian_TC39_Proposals/Proposals/Stage 0 Proposals/{link_titles}.md", "w") as proposals:
                proposals.write(
                    f"#Stage0Tag\n"
                    f"Classification: {classification}\n"
                    f"Human Validated: No\n"
                    f"Title: {title}\n"
                    f"Authors: {authors}\n"
                    f"Champions: {champions}\n"
                    f"Date: {date}\n"
                    f"Last Commit: {returnDate}\n"
                    f"GitHub Link: {github_link}\n"
                    f"GitHub Note Link: {github_note_link}\n\n"
                    f"# Proposal Description:\n{file_content}"
                )
                
