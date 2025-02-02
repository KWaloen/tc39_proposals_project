import ast

with open("Stage_1/outputMD/apiResults.md", "r") as file:
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

            with open(f"Obsidian_TC39_Proposals/Proposals/Stage 1 Proposals/{link_titles}.md", "w") as proposals:
                proposals.write(
                    f"#Stage1\n"
                    f"Authors: {authors}\n"
                    f"Champions: {champions}\n"
                    f"Date: {date}\n"
                    f"Link Titles: {link_titles}\n"
                    f"GitHub Link: {github_link}\n"
                    f"GitHub Note Link: {github_note_link}\n"
                )
                
