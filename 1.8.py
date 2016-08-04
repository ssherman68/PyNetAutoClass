# Python & network Automation Class week 1 exercise 8
#   -Stacy Sherman 8/2/16

# Write a Python program using ciscoconfparse that parses this config file. 
# Note, this config file is not fully valid (i.e. parts of the configuration 
# are missing). The script should find all of the crypto map entries in the 
# file (lines that begin with 'crypto map CRYPTO') and for each crypto map 
# entry print out its children.

from ciscoconfparse import CiscoConfParse

parse_cfg = CiscoConfParse("cisco_ipsec.txt")

crypto_maps = parse_cfg.find_objects(r"^crypto map CRYPTO")

for c in crypto_maps:
    print ('\n')
    print c.text
    for child in c.children:
        print child.text
