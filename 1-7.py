# Python & network Automation Class week 1 exercise 7
#   -Stacy Sherman 8/2/16

# Write a Python program that reads both the YAML file and the JSON file 
# created in exercise6 and pretty prints the data structure that is returned.

import yaml
import json
from pprint import pprint as pp

with open("ymallist.yml", 'r') as y:
    prettyaml = yaml.load(y)

with open("jsonlist.json", 'r') as j:
    prettyjson = json.load(j)

pp(prettyaml)
pp(prettyjson)
