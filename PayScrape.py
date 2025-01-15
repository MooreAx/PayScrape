#Scrape pairing info from VMO

import requests
from bs4 import BeautifulSoup
import string


#VMO link without PID
base_url = "https://cav.vmosolutions.net/cwa/pri/F7DF8AE5115C4BF7AA2ED3C74FC5B9A0859B9AA700FA40D09A11563B37DA0266?PID="

#PID (pairing ID)
PID = "76657"

#full link
url = base_url + PID

page = requests.get(url)

#Parse HTML contect
soup = BeautifulSoup(page.text, "html.parser")

def print_line(soup_obj):
    elements = [element.strip() for element in soup_obj.stripped_strings]
    combined_text = " ".join(elements)
    return(combined_text)

#s is a string that stores info extracted from the soup
s = ""

header1 = soup.find("div", id="mdivTop")
temp = print_line(header1)
s = temp
print(temp)

header2 = soup.find("div", id ="secTimes")
temp = print_line(header2)
s = s + '\n' + temp
print(temp)

rows = soup.find_all("tr")
for row in rows:
    temp = print_line(row)
    s = s + '\n' + temp
    print(temp)

#write data to file
with open(f'Pairings/{PID}.txt', 'w') as file:
    file.write(s)
