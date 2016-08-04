# Python & network Automation Class week 1 exercise 9
#   -Stacy Sherman 8/3/16

# Find all of the crypto map entries that are using PFS group2

from ciscoconfparse import CiscoConfParse

parse_cfg = CiscoConfParse("cisco_ipsec.txt")

pfs_maps = parse_cfg.find_objects_w_child(parentspec=r"^crypto map CRYPTO", 
    childspec=r"set pfs group2")

for map in pfs_maps:
    print map.text
