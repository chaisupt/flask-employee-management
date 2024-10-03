import re

def is_valid_name(name, length_from=1, length_to=100):
    # Check if the length of the name is within the specified range
    if not (length_from <= len(name) <= length_to):
        return False
    
    # Check if the name contains only alphanumeric characters and spaces
    return bool(re.match("^[a-zA-Z0-9 -]+$", name))

def is_valid_address(name, length_from=1, length_to=400):
    # Check if the length of the name is within the specified range
    if not (length_from <= len(name) <= length_to):
        return False
    
    # Check if the name contains only alphanumeric characters and spaces
    return bool(re.match("^[a-zA-Z0-9\s,-]+$", name))

def is_valid_salary(salary):
    #check that salary need to be > 0 and be int or float if not then return false
    return isinstance(salary, (int, float)) and salary > 0

def is_valid_url(url):
    if not (len(url) <= 2000):
        return False
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or IPv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_regex, url) is not None