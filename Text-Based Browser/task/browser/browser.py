import sys
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore


EXIT = 'exit'
BACK = 'back'


def is_url_correct(string):
    if string.find('.') == -1:
        print('Error. The URL is incorrect! It should contain "." symbol.')
        return False
    return True


def get_prefix(string):
    prefix = ('www.', 'http://', 'https://')
    sort_of_prefix = [string.startswith(prfx) for prfx in prefix]
    if any(sort_of_prefix):
        pref_id = sort_of_prefix.index(True)
        return prefix[pref_id]
    return None


def get_file_name(page):
    global dir_name
    f_name = page.replace('.', '_')
    if os.path.exists(os.getcwd() + '\\' + dir_name + '\\' + f_name):
        return f_name
    if is_url_correct(page):
        pref = get_prefix(page)
        while pref is not None:
            page = page[len(pref):]
            pref = get_prefix(page)
        return page[:page.rfind('.')].replace('.', '_')
    return None


def make_full_url(page):
    prfx = get_prefix(page)
    if prfx in ('http://', 'https://'):
        return page
    return 'http://' + page


def parse(response):
    tag_list = ('p', 'h1', 'h2', 'h3', 'h4', 'h5',
                'h6', 'a', 'ul', 'ol', 'li')
    result_str = ''
    soup = BeautifulSoup(response.content, 'html.parser')
    tags_all = soup.find_all(tag_list)
    for tag in tags_all:
        if tag.name == 'a':
            result_str += '<a>' + tag.text + '</a>'
        else:
            result_str += tag.text
    return result_str


def print_page(file):
    for line in file.readlines():
        a_start_ind = line.find('<a>')
        if a_start_ind != -1:
            a_end_ind = line.find('</a>')
            print(line[:a_start_ind], end='')
            print(Fore.BLUE, line[a_start_ind + 3:a_end_ind], end='')
            print(line[a_end_ind + 4:])
        else:
            print(line)


def show_page(page):
    global dir_name
    file_name = get_file_name(page)
    if file_name is not None:
        if not os.path.exists(os.getcwd() + '\\' + dir_name + '\\' + file_name):
            with open(os.getcwd() + '\\' + dir_name + '\\' + file_name, 'w') as file:
                url = make_full_url(page)
                res = requests.get(url)
                text_content = parse(res)
                file.write(text_content)
        with open(os.getcwd() + '\\' + dir_name + '\\' + file_name) as file:
            print_page(file)
    else:
        raise ValueError


args = sys.argv
dir_name = args[1]
# dir_name = 'tb_tabs'
if not os.path.exists(dir_name):
    os.mkdir(os.getcwd() + '\\' + dir_name)

history = deque()
in_str = input()
while in_str != EXIT:
    if in_str == BACK:
        history.pop()  # get the last page, but we need the page before the last
        show_page(history.pop())
    else:  # in_str contains page
        try:
            show_page(in_str)
            history.append(get_file_name(in_str))
        except ValueError:
            print("Error. There isn't the web page")
    in_str = input()
