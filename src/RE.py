import re

def regex(post, regex_input) :
    return re.search(regex_input, post)