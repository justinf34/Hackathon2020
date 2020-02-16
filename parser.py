import sys
import requests
from bs4 import BeautifulSoup

def get_course_link(course_name):
    url = "https://www.ucalgary.ca/pubs/calendar/current/course-desc-main.html"
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    soup.prettify()
    link_text_tags = soup.find_all('a', {'class' : 'link-text'})

    def get_course():
        for tag in link_text_tags:
            inner_text = tag.text
            if (course_name in inner_text):
                return tag.get('href')

    course_link = "https://www.ucalgary.ca/pubs/calendar/current/" + get_course()
    return course_link

def get_desc(course_link, course_code):
    r = requests.get(course_link).text
    soup = BeautifulSoup(r, 'lxml')
    soup.prettify()
    num_links = soup.find_all('a', {'class' : 'link-text'})
    
    def get_number():
        for tag in num_links:
            if (course_code in tag.text):
                return tag.get('href').split('#')[1]
    number = get_number()
    parent = soup.find('a', {'name' : number}).parent
    desc = parent.find('span', {'class' : 'course-desc'}).text
    # print(desc)
    return desc

def string_contains(str1,str2):
    lst1 = str1.split(' ')
    lst2 = str2.split(' ')

    if len(lst1) <= len(lst2):
        return lst1 == lst2[:len(lst1)]

    return False

common_pun = [",", ".", ";", ":"]
common_words = ["the", "to", "of", "and", " a ", "in", "that", "for", "it", "on", "with", "as", "do", "at", "this", "by", "from", "an", "all", "there", "their", "what"]
def remove_word(desc, wordIndex):
    if (wordIndex < 0):
        return desc
    if (string_contains(common_words[wordIndex], desc)):
        return remove_word(desc.replace(common_words[wordIndex],''), wordIndex - 1)
    else: 
        return remove_word(desc, wordIndex - 1)
    

def remove_pun(desc, punIndex):
    if(punIndex < 0):
        return desc
    arr = []
    for d in desc:
        for lol in d:
            returnValue = lol.split(common_pun[punIndex])
            arr.append(returnValue)

    return remove_pun(arr, punIndex - 1)

def get_key_words(course_name, course_code):
    try:
        description = get_desc(get_course_link(name), code)
        # d2 = remove_word(description, len(common_words) - 1) # doesn't work rn
        d3 = remove_pun([[description]], len(common_pun) - 1)
        d4 = []
        for i in d3:
            for j in i:
                if j:
                    d4.append(j.strip())
        return d4
    except:
       return -1 
