import re

proposals = []
titles = []
linkTitles = []
authors = []
champions = []
dates = []

#TODO collect commit date
commitDate = []
links = []
proposalNoteLinks = []
proposalLinks = {}
notesLinks = {}

'''
This function extracts the details of the proposals from the file content

'''
def prepText(fileContent):

    global proposals

    first = fileContent.index("|")
    last = fileContent.rindex("|")

    proposalDetails = fileContent[first:last]

    textRaw = proposalDetails.splitlines()

    text = textRaw[2:]

    return text

def extractDetails(text, fileContent):

    for n in text:   
         
        words = n.strip().split("|")

        #Extract title and append to list 
        extractTitle(words, titles, linkTitles)

        #Extract author and append to list
        extractAuthor(words)

        #Extract champion(s) and append to list 
        extractChampion(words)

        #Extract date and append to list 
        extractDate(words)

    #Extract proposal link and append to list 
    extractProposalLink(fileContent)

    matchLinkWithProposal(linkTitles, proposalLinks)

    matchNoteLinkWithProposal(linkTitles, notesLinks)

    for i in range(len(titles)):
        proposals.append({
            "Title": titles[i], 
            "Author(s)": authors[i], 
            "Champion(s)": champions[i], 
            "Date": dates[i], 
            "Link Titles": "[["+linkTitles[i]+"]]", 
            "GitHub Link": links[i], 
            "GitHub Note Link": proposalNoteLinks[i]})

    #first line contains table title and line. remove this  

    return proposals

'''
This function extracts the title of the proposals from the file content
'''
def extractTitle(words, saveTitlesIn, saveLinksIn):
 
    extractedTitles = []

    compoundTitle = words[1].strip().split("[")

    for each in compoundTitle:
        # Preserve content with backticks, including brackets inside backticks
        if "`" in each:
            cleaned = each.strip()
        else:
            # Remove surrounding brackets and backticks outside backticks
            cleaned = re.sub(r"[`\[,\]]", "", each).strip()
            # Remove parentheses if not inside backticks
            cleaned = re.sub(r"[()]", "", cleaned).strip()

        # Remove any trailing `]` explicitly
        cleaned = re.sub(r"]$", "", cleaned).strip()

        cleaned = re.sub(r"`", "", cleaned).strip()

        extractedTitles.append(cleaned)

    try:
        saveTitlesIn.append(extractedTitles[1])
        saveLinksIn.append(extractedTitles[2])
    except Exception:
        saveTitlesIn.append("-------------error---------------")
        saveLinksIn.append("-------------error---------------")
        print("error with title", extractedTitles) 


def matchLinkWithProposal(linkTitles, proposalLinks):

    for each in linkTitles:
        addBrackets = "[" + each + "]"
        link = proposalLinks.get(addBrackets)
        links.append(link)

def matchNoteLinkWithProposal(linkTitles, notesLinks):
    for each in linkTitles:
        formatEach = "[" + each + "-notes" + "]"
        noteLink = notesLinks.get(formatEach)
        proposalNoteLinks.append(noteLink)

    
    
'''
This function extracts the author of the proposals from the file content 
'''

def extractAuthor(words):
    global authors
    author = words[2].strip()
    names = author.replace("<br />", ", ")
    authors.append(names)

'''
This function extracts the champion of the proposals from the file content
'''

def extractChampion(words):
    global champions 
    champion = words[3].strip()
    names = champion.replace("<br />", ", ")
    champions.append(names)

''' 
This function extracts the date of the proposals from the file content
'''

def extractDate(words):
    global dates 

    try:
        date = words[4].strip()

        if "&nbsp;" in words[5].strip():
            date = words[5].strip()

        extractedDate = ((date.split("][")[0])[1:])

        if "&nbsp;" in extractedDate:
            splitDate = extractedDate.split("&nbsp;")
            month = re.search(r"(\b[A-Z][a-z]*\b)", splitDate[0]).group()
            date = re.search(r"(\d[0-9]+)", splitDate[1]).group()
            finalDate = month + " " + date

            dates.append(finalDate)

        else:
            dates.append(extractedDate)
    except:
        print("no dates in repository")
        dates.append(None)

''' 
This function extracts the proposal link from the file content
'''

def extractProposalLink(words):
    global notesLinks
    global proposalLinks

    first = words.rindex("|")
    links = words[first:].splitlines()
    
    
    #Sort links into notes and proposals
    for link in links:

        try: 
            if "notes" in link:
                addLinkToDict(link, notesLinks)

            else:            
                addLinkToDict(link, proposalLinks)

        #log error message 
        except Exception:
            print("error with this link:", link) 
            
'''
This function adds a link to the dictionary
'''
def addLinkToDict(words, dictToUpdate):
    
    link = words.split()
    linkName = link[0].rstrip(":")
    url = link[1]

    dictToUpdate.update({linkName: url})

    




