def makeIntlineDict(base,compar,intercordinal,intercordinal_keys,lineeqn,V):
    l1 = base
    l2 = compar
    temp = []
    if l1 not in lineeqn:
        lineeqn.append(l1)
    if l2 not in lineeqn:
        lineeqn.append(l2)

    if V not in intercordinal_keys:
        intercordinal_keys.append(V)
        temp.append(l1)
        temp.append(l2)
        intercordinal[V]= temp[:]
    else:
        if not l1 in intercordinal[V]:
            intercordinal[V].append(l1)
        if not l2 in intercordinal[V]:
            intercordinal[V].append(l2)

#Calculate Intersection points
def find_intersection(x1,y1,x2,y2,x3,y3,x4,y4) :

    s10_x = x2 - x1
    s10_y = y2 - y1
    s32_x = x4 - x3
    s32_y = y4 - y3
    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0 :
        x,y = '',''
        return (x,y) # collinear
    denom_is_positive = denom > 0
    s02_x = x1 - x3
    s02_y = y1 - y3
    s_numer = s10_x * s02_y - s10_y * s02_x
    if (s_numer < 0) == denom_is_positive :
        x,y = '',''
        return (x,y) # no collision
    t_numer = s32_x * s02_y - s32_y * s02_x
    if (t_numer < 0) == denom_is_positive :
        x,y = '',''
        return (x,y) # no collision
    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive :
        x,y = '',''
        return (x,y) # no collision
    t = t_numer / denom # collision detected
    x,y = x1 + (t * s10_x), y1 + (t * s10_y)
    return x,y
def point_exists_InLine(x1,y1,x2,y2,x3,y3,x4,y4,vpointdist):

    if not (x4 - x3) == 0 and not (x2 - x1) == 0:
        slope1 = (y2 - y1) / (x2 - x1)
        slope2 = (y4-y3) / (x4-x3)
        if slope1 == slope2:

            Intercept1 = y1 - (slope1 * x1)
            Intercept2 = y3 - (slope2 * x3)

                ##Check if X1,Y1 lies in Equation2
            Interceptcheck = y1 - (slope2 * x1)
            if Interceptcheck == Intercept2:

                # if (x2-x1) == 0 or  (x4-x3) == 0:
                if min(x1,x2) <= min(x3,x4) and max(x1,x2) >= max(x3,x4) and min(y1,y2) <= min(y3,y4) and max(y1,y2) >= max(y3,y4):

                        vpointdist.append(x3)
                        vpointdist.append(y3)
                        vpointdist.append(x4)
                        vpointdist.append(y4)
                elif min(x3,x4) <= min(x1,y1) and max(x3,x4) >= max(x1,x2) and min(y3,y4) <= min(y1,y2) and max(y3,y4) >= max(y1,y2):

                        vpointdist.append(x1)
                        vpointdist.append(y1)
                        vpointdist.append(x2)
                        vpointdist.append(y2)
    else:

        if x1 == x2 == x3 == x4:
            if min(x1,x2) <= min(x3,x4) and max(x1,x2) >= max(x3,x4) and min(y1,y2) <= min(y3,y4) and max(y1,y2) >= max(y3,y4):

                    vpointdist.append(x3)
                    vpointdist.append(y3)
                    vpointdist.append(x4)
                    vpointdist.append(y4)
            elif min(x3,x4) <= min(x1,y1) and max(x3,x4) >= max(x1,x2) and min(y3,y4) <= min(y1,y2) and max(y3,y4) >= max(y1,y2):

                    vpointdist.append(x1)
                    vpointdist.append(y1)
                    vpointdist.append(x2)
                    vpointdist.append(y2)

        # elif x2-x1 == 0 and ( x1 == x3 or x1 == x4):
        # 	vpointdist.append(x1)
        # 	slope2 = (y4-y3) / (x4-x3)
        # 	Inter = y3 - (slope2 * x3)
        # 	yn = (slope2*x1) + Inter
        # 	vpointdist.append(yn)

        # elif x3-x4 == 0 and (x4 == x1 or x4 == x2):
        # 	vpointdist.append(x3)
        # 	slope2 = (y2-y1) / (x2-x1)
        # 	Inter = y2 - (slope2 * x2)
        # 	yn = (slope2*x3) + Inter
        # 	vpointdist.append(yn)

    return(vpointdist)