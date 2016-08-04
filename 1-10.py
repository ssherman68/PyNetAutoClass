# Python & network Automation Class week 1 exercise 10
#   -Stacy Sherman 8/3/16

# Using ciscoconfparse find the crypto maps that are not using AES (based-on 
# the transform set name). Print these entries and their corresponding 
# transform set name.

from ciscoconfparse import CiscoConfParse

parse_cfg = CiscoConfParse("cisco_ipsec.txt")

noaes_maps = parse_cfg.find_objects_wo_child(parentspec=r"^crypto map CRYPTO", 
    childspec=r"AES")

for map in noaes_maps:
    print map.text
