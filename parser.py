import sys
import requests
from bs4 import BeautifulSoup

name = sys.argv[1]
code = sys.argv[2]
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
    print(desc)
    return desc
    
try:
    get_desc(get_course_link(name), code)
except:
    pass


        