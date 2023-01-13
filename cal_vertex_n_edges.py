import re
import math
import ast
from calc_intersection import *
def calculateVertices(city_map_dict,full_str_lst,vertices,vdict):


    #Local Declaraions
    vlist = []
    vkeys = []
    vertices1 = {}
    intercordinal = {}
    lineeqn = []
    intercordinal_keys = []

    for i in range(0,len(full_str_lst)-1):   		#looping through all the streets
        key1 = full_str_lst[i]
        print("key1 : ", key1)
        for base in city_map_dict[key1][:]:
            print("base : ", base)
            j = i + 1
            line1 = re.findall(r'(-?\d+\.?\d*)',base) 			   #BAse line Segment to Compare
            print("line1 : ", line1)

            for k in range (j,len(full_str_lst)):
                for compar in city_map_dict[full_str_lst[k]][:]:
                    print("compar : ", compar)
                    line2 = re.findall(r'(-?\d+\.?\d*)',compar)       #comparator line Segment to Compare with
                    print("line2:", line2)
                    #Coordinates x,y values for both line1 and line2
                    x1, y1 = float(line1[0]), float(line1[1])
                    x2, y2 = float(line1[2]), float(line1[3])
                    x3, y3 = float(line2[0]), float(line2[1])
                    x4, y4 = float(line2[2]), float(line2[3])
                    print("x1 : ", x1, " and y1 : ", y1)
                    print("x2 : ", x2, " and y2 : ", y2)
                    print("x3 : ", x3, " and y3 : ", y3)
                    print("x4 : ", x4, " and y4 : ", y4)

    #Case1: Check if they have common points meaning they end and another street starts
                    #or if the end and then new street begins (overlapping)
                    if x1 == x3 and y1 == y3:
                        V = '(' + str(x1) + ',' + str(y1) +')' 	#If yes take the common point as intersection
                        print("V : ", V)
                        if V not in vkeys:			#Check if its a new i.point

                            #Vertex Calculation Dict Purpose
                            vkeys.append(V)			#Append it to vkey(storing all int points)
                            print("vkeys :", vkeys)
                            vlist.append('(' + str(x2) + ',' + str(y2) +')')
                            vlist.append('(' + str(x4) + ',' + str(y4) +')')
                            print("vlist :", vlist)
                            vdict[V] = vlist[:]		#Append to Vdict by storing i.point as key and others as points
                            print("vdict :", vdict)
                            del vlist[:]			#causing the i.point

                        #Edge- Intersection Lines Dict purpose
                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)

                        else: #If it exists already append only the new coordinate causing I.point to vidct's value in the same key

                        #Vertex Duplication Reduction purpose
                            tempcoord = '(' + str(x2) + ',' + str(y2) +')'
                            if tempcoord not in vdict[V]:
                                vdict[V].append(tempcoord)
                            tempcoord = '(' + str(x4) + ',' + str(y4) +')'
                            if tempcoord not in vdict[V]:
                                vdict[V].append(tempcoord)

                        #Edge Calculation Dict purpose
                            #Edge- Intersection Lines Dict purpose
                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)

    #Case2:
                    elif x1 == x4 and y1 == y4:
                        V = '(' + str(x1) + ',' + str(y1) +')'
                        if V not in vkeys:

                            vkeys.append(V)
                            vlist.append('(' + str(x2) + ',' + str(y2) +')')
                            vlist.append('(' + str(x3) + ',' + str(y3) +')')
                            vdict[V] = vlist[:]
                            del vlist[:]
                        #Edge- Intersection Lines Dict purpose
                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)



                        else:
                            tempcoord = '(' + str(x2) + ',' + str(y2) +')'
                            if tempcoord not in vdict[V]:
                                vdict[V].append(tempcoord)
                            tempcoord = '(' + str(x3) + ',' + str(y3) +')'
                            if tempcoord not in vdict[V]:
                                vdict[V].append(tempcoord)
                        #Edge- Intersection Lines Dict purpose
                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)


    #Case3:
                    elif x2 == x3 and y2 == y3:
                        V = '(' + str(x2) + ',' + str(y2) +')'
                        if V not in vkeys:

                            vkeys.append(V)
                            vlist.append('(' + str(x1) + ',' + str(y1) +')')
                            vlist.append('(' + str(x4) + ',' + str(y4) +')')
                            vdict[V] = vlist[:]
                            del vlist[:]

                            #Edge- Intersection Lines Dict purpose
                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)

                        else:
                            tempcoord = '(' + str(x1) + ',' + str(y1) +')'
                            if tempcoord not in vdict[V]:
                                vdict[V].append(tempcoord)
                            tempcoord = '(' + str(x4) + ',' + str(y4) +')'
                            if tempcoord not in vdict[V]:
                                vdict[V].append(tempcoord)
                            #Edge- Intersection Lines Dict purpose
                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)

    #Case4
                    elif x2 == x4 and y2 == y4:
                        V = '(' + str(x2) + ',' + str(y2) +')'
                        if V not in vkeys:

                            vkeys.append(V)
                            vlist.append('(' + str(x1) + ',' + str(y1) +')')
                            vlist.append('(' + str(x3) + ',' + str(y3) +')')
                            vdict[V] = vlist[:]
                            del vlist[:]
                        #Edge- Intersection Lines Dict purpose
                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)

                        else:
                            tempcoord = '(' + str(x1) + ',' + str(y1) +')'
                            if tempcoord not in vdict[V]:
                                vdict[V].append(tempcoord)
                            tempcoord = '(' + str(x3) + ',' + str(y3) +')'
                            if tempcoord not in vdict[V]:
                                vdict[V].append(tempcoord)
                            #Edge- Intersection Lines Dict purpose
                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)


    #Case5:Find I.point using slope	function
                    else:

                        xcoor,ycoor = find_intersection(x1,y1,x2,y2,x3,y3,x4,y4)
                        if not xcoor == '' and not ycoor == '':
                            V = '(' + str(xcoor) + ',' + str(ycoor) +')'

                            #If intersection found then and its unique
                            if V not in vkeys:

                                #Vertice Calculation Dict Purpose
                                vkeys.append(V)
                                vlist.append('(' + str(x1) + ',' + str(y1) +')')
                                vlist.append('(' + str(x2) + ',' + str(y2) +')')
                                vlist.append('(' + str(x3) + ',' + str(y3) +')')
                                vlist.append('(' + str(x4) + ',' + str(y4) +')')
                                vdict[V] = vlist[:]
                                del vlist[:]

                                #Edge- Intersection Lines Dict purpose
                                makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)


                            else:#If intersection found and its already present

                                #Vertices Calculation purpose (Removing duplicates)
                                tempcoord = '(' + str(x1) + ',' + str(y1) +')'
                                if tempcoord not in vdict[V]:
                                    vdict[V].append(tempcoord)
                                tempcoord = '(' + str(x2) + ',' + str(y2) +')'
                                if tempcoord not in vdict[V]:
                                    vdict[V].append(tempcoord)
                                tempcoord = '(' + str(x3) + ',' + str(y3) +')'
                                if tempcoord not in vdict[V]:
                                    vdict[V].append(tempcoord)
                                tempcoord = '(' + str(x4) + ',' + str(y4) +')'
                                if tempcoord not in vdict[V]:
                                    vdict[V].append(tempcoord)

                                #Edge- Intersection Lines Dict purpose
                                makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)
                        else:
                                vpointdist = []
                                i = 0
                                vpointdist = point_exists_InLine(x1,y1,x2,y2,x3,y3,x4,y4,vpointdist)
                                if not vpointdist == []:
                                    for eindex in range(0,len(vpointdist)-1,2):
                                        V = '(' + str(vpointdist[eindex]) + ',' + str(vpointdist[eindex+1]) +')'

                                        #If intersection found then and its unique
                                        if V not in vkeys:

                                            #Vertice Calculation Dict Purpose
                                            vkeys.append(V)
                                            vlist.append('(' + str(x1) + ',' + str(y1) +')')
                                            vlist.append('(' + str(x2) + ',' + str(y2) +')')
                                            vlist.append('(' + str(x3) + ',' + str(y3) +')')
                                            vlist.append('(' + str(x4) + ',' + str(y4) +')')
                                            vdict[V] = vlist[:]
                                            del vlist[:]

                                            #Edge- Intersection Lines Dict purpose
                                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)


                                        else:#If intersection found and its already present

                                            #Vertices Calculation purpose (Removing duplicates)
                                            tempcoord = '(' + str(x1) + ',' + str(y1) +')'
                                            if tempcoord not in vdict[V]:
                                                vdict[V].append(tempcoord)
                                            tempcoord = '(' + str(x2) + ',' + str(y2) +')'
                                            if tempcoord not in vdict[V]:
                                                vdict[V].append(tempcoord)
                                            tempcoord = '(' + str(x3) + ',' + str(y3) +')'
                                            if tempcoord not in vdict[V]:
                                                vdict[V].append(tempcoord)
                                            tempcoord = '(' + str(x4) + ',' + str(y4) +')'
                                            if tempcoord not in vdict[V]:
                                                vdict[V].append(tempcoord)

                                            #Edge- Intersection Lines Dict purpose
                                            makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V)




    verticesOrder(vertices,vkeys,vdict,vertices1) #Vertice Calculation and order
    return (intercordinal,lineeqn,intercordinal_keys)

def verticesOrder(vertices,vkeys,vdict,vertices1):
    if not vdict == {}:
        vertices.clear()
        ikey = 0
        for key in vkeys:
            vertices[ikey] =ast.literal_eval(key)
            ikey =ikey + 1
        for value in vdict.values():
            for item in range(0,len(value)):
                if not ast.literal_eval(value[item]) in list(vertices.values()):
                    vertices[ikey] =  ast.literal_eval(value[item])
                    ikey = ikey + 1
    else:
        vertices.clear()


def calculatEdges(intercordinal, vdict, vertices, lineeqn):
    intersecs = []
    iodistance = []
    edges = []
    for line in lineeqn:
        for k, v in intercordinal.items():
            if line in v:
                if k not in intersecs:
                    intersecs.append(k)
        a1, a2, a3, a4 = re.findall(r'(-?[+-]?\d*\.?\d+)', line)
        if len(intersecs) == 1:
            ck1 = '(' + a1 + ',' + a2 + ')'
            ck2 = '(' + a3 + ',' + a4 + ')'
            ck1 = ast.literal_eval(ck1)
            ck2 = ast.literal_eval(ck2)
            if not str(list(vertices.keys())[list(vertices.values()).index(ast.literal_eval(intersecs[0]))]) == str(
                    list(vertices.keys())[list(vertices.values()).index(ck1)]):
                e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(ast.literal_eval(intersecs[0]))]) + ',' + str(
                    list(vertices.keys())[list(vertices.values()).index(ck1)]) + '>'
                if e1 not in edges: edges.append(e1)
                #if not str(list(list(vertices.keys()))[list(list(vertices.values())).index(ast.literal_eval(intersecs[0]))]) == str(
               #     list(list(vertices.keys()))[list(list(vertices.values())).index(ck1)]):
                #e1 = ''
                #
                #
            if not str(list(vertices.keys())[list(vertices.values()).index(ast.literal_eval(intersecs[0]))]) == str(
                    list(vertices.keys())[list(vertices.values()).index(ck2)]):
                e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(ast.literal_eval(intersecs[0]))]) + ',' + str(
                    list(vertices.keys())[list(vertices.values()).index(ck2)]) + '>'
                if e1 not in edges: edges.append(e1)
            del intersecs[:]
            ck1, ck2 = '', ''

        if len(intersecs) > 2:

            pointointdistance = []
            endpointdistance = []
            for echi in range(0, len(intersecs)):
                c1, c2 = re.findall(r'(-?[+-]?\d*\.?\d+)', intersecs[echi])
                pidist = math.sqrt((float(c2) - float(a2)) ** 2 + (float(c1) - float(a1)) ** 2)
                pointointdistance.append(pidist)
                endpidist = math.sqrt((float(c2) - float(a4)) ** 2 + (float(c1) - float(a3)) ** 2)
                endpointdistance.append(endpidist)

            f1, f2 = re.findall(r'(-?[+-]?\d*\.?\d+)', (intersecs[pointointdistance.index(min(pointointdistance))]))
            g1, g2 = re.findall(r'(-?[+-]?\d*\.?\d+)', (intersecs[endpointdistance.index(min(endpointdistance))]))
            newintersecs = intersecs[:]

            ck1 = '(' + f1 + ',' + f2 + ')'
            ck2 = '(' + a1 + ',' + a2 + ')'
            reference = ck1
            newintersecs.remove(ck1)
            ck1 = ast.literal_eval(ck1)
            ck2 = ast.literal_eval(ck2)

            if not str(list(vertices.keys())[list(vertices.values()).index(ck1)]) == str(
                    list(vertices.keys())[list(vertices.values()).index(ck2)]):
                e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(ck1)]) + ',' + str(
                    list(vertices.keys())[list(vertices.values()).index(ck2)]) + '>'
                if e1 not in edges: edges.append(e1)

            ck1 = ''
            ck2 = ''

            ck1 = '(' + g1 + ',' + g2 + ')'
            ck2 = '(' + a3 + ',' + a4 + ')'
            # newintersecs.remove(ck1)
            # endrefer = ck1
            ck1 = ast.literal_eval(ck1)
            ck2 = ast.literal_eval(ck2)

            if not str(list(vertices.keys())[list(vertices.values()).index(ck1)]) == str(
                    list(vertices.keys())[list(vertices.values()).index(ck2)]):
                e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(ck1)]) + ',' + str(
                    list(vertices.keys())[list(vertices.values()).index(ck2)]) + '>'
                if e1 not in edges: edges.append(e1)

            ck1 = ''
            ck2 = ''

            for inte in newintersecs[:]:
                # if not len(newintersecs) == 1:
                for ke in range(0, len(newintersecs)):
                    b1, b2 = re.findall(r'(-?[+-]?\d*\.?\d+)', reference)
                    b3, b4 = re.findall(r'(-?[+-]?\d*\.?\d+)', newintersecs[ke])
                    dist = math.sqrt((float(b4) - float(b2)) ** 2 + (float(b3) - float(b1)) ** 2)
                    iodistance.append(dist)
                if not iodistance == []:
                    kindex = iodistance.index(min(iodistance))
                    b = re.findall(r'(-?[+-]?\d*\.?\d+)', (newintersecs[kindex]))
                    b3 = b[0]
                    b4 = b[1]
                    ck1 = reference
                    ck2 = '(' + b3 + ',' + b4 + ')'
                    ck1 = ast.literal_eval(ck1)
                    ck2 = ast.literal_eval(ck2)
                    if not str(list(vertices.keys())[list(vertices.values()).index(ck1)]) == str(
                            list(vertices.keys())[list(vertices.values()).index(ck2)]):
                        e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(ck1)]) + ',' + str(
                            list(vertices.keys())[list(vertices.values()).index(ck2)]) + '>'
                        if e1 not in edges: edges.append(e1)
                    reference = '(' + b3 + ',' + b4 + ')'
                    newintersecs.pop(kindex)
                    ck1, ck2 = '', ''
                    iodistance = []
                # else:
                # 	if not str(list(vertices.keys())[list(vertices.values()).index(endrefer)]) == str(list(vertices.keys())[list(vertices.values()).index(newintersecs[0])]):
                # 		e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(endrefer)]) + ',' + str(list(vertices.keys())[list(vertices.values()).index(newintersecs[0])]) + '>'
                # 	if e1 not in edges:edges.append(e1)
                else:
                    break


        elif len(intersecs) == 2:
            twodistance = []
            c1, c2 = re.findall(r'(-?[+-]?\d*\.?\d+)', intersecs[0])
            twodist = math.sqrt((float(c2) - float(a2)) ** 2 + (float(c1) - float(a1)) ** 2)
            twodistance.append(twodist)
            twodist = math.sqrt((float(c2) - float(a4)) ** 2 + (float(c1) - float(a3)) ** 2)
            twodistance.append(twodist)

            if twodistance.index(min(twodistance)) == 0:
                fr1 = ast.literal_eval(intersecs[0])
                end1 = ast.literal_eval(intersecs[1])
            else:
                fr1 = ast.literal_eval(intersecs[1])
                end1 = ast.literal_eval(intersecs[0])
            ck1 = '(' + a1 + ',' + a2 + ')'
            ck2 = '(' + a3 + ',' + a4 + ')'
            ck1 = ast.literal_eval(ck1)
            ck2 = ast.literal_eval(ck2)

            if not str(list(vertices.keys())[list(vertices.values()).index(fr1)]) == str(
                    list(vertices.keys())[list(vertices.values()).index(ck1)]):
                e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(fr1)]) + ',' + str(
                    list(vertices.keys())[list(vertices.values()).index(ck1)]) + '>'
                if e1 not in edges: edges.append(e1)
            if not str(list(vertices.keys())[list(vertices.values()).index(end1)]) == str(
                    list(vertices.keys())[list(vertices.values()).index(ck2)]):
                e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(end1)]) + ',' + str(
                    list(vertices.keys())[list(vertices.values()).index(ck2)]) + '>'
                if e1 not in edges: edges.append(e1)

            i1 = ast.literal_eval(intersecs[0])
            i2 = ast.literal_eval(intersecs[1])
            if not str(list(vertices.keys())[list(vertices.values()).index(i1)]) == str(
                    list(vertices.keys())[list(vertices.values()).index(i2)]):
                e1 = '<' + str(list(vertices.keys())[list(vertices.values()).index(i1)]) + ',' + str(
                    list(vertices.keys())[list(vertices.values()).index(i2)]) + '>'
                if e1 not in edges: edges.append(e1)
        intersecs = []

    # U=0
    # for i in range(0,len(edges)):
    # 	edges[i] = ast.literal_eval(edges[i])
    return (edges)
