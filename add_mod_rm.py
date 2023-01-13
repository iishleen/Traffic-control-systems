import sys
# Creation of Road
def addStreet(full_str_lst,street,street_detail,city_map_dict):
    full_str_lst.append(street)
    newStr = []
    print(street_detail[1:])

    for i in range(0,len(street_detail[1:])):
        x = street_detail[i]
        y = street_detail[i+1]
        if x[-1] == ')' and y[-1] == ')':
            newStr.append( x + '-->'+ y )
        else:
            sys.stderr.write("Enter All Coordinates within parenthesis")
    city_map_dict[street] = newStr
    return city_map_dict

# Modify street
def modifyStreet(full_str_lst ,street,street_detail,city_map_dict):
    newStreet = []

    for i in range(0,len(street_detail[1:])):
        x = street_detail[i]
        y = street_detail[i+1]
        if x[-1] == ')' and  y[-1] == ')':
            newStreet.append( x + '-->'+ y )
        else:
            sys.stderr.write("Enter All Coordinates within parenthesis")
    city_map_dict[street] = newStreet
    return city_map_dict

# Removal of street
def removeStreet(city_map_dict,street,full_str_lst):
    del city_map_dict[street]
    full_str_lst.remove(street)
    pass

#Updating Dictionary
def updateDict(city_map,city_map_dict,street,full_str_lst):
    uindex = full_str_lst.index(street)
    # for lis in city_map[:]:
    city_map_dict[street] = city_map[uindex]


