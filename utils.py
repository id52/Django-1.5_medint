# - coding: utf-8  -
import string
from random import choice

def random_string(l):
    return ''.join([choice(string.letters + string.digits) for i in range(l)])
