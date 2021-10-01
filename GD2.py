def process_gesture(pos_history:dict,buffer_size):
    pos_dict = {}
    for i,j in pos_history.items():
        if j[-1] is None:
            continue
        valid_bboxes = []
        consec_none_ct = 0
        for ii in range(1, buffer_size+1):
            if j[-ii] is None or j[-ii] is [0,0,0,0]:
                consec_none_ct+=1
            else:
                valid_bboxes.append(j[-ii])
                consec_none_ct = 0
            if consec_none_ct>5:
                break
        # if len(valid_bboxes)>0:
        #     print(len(valid_bboxes))
        if len(valid_bboxes)>20:
            xs,ys,ws,hs = valid_bboxes[0]
            xe,ye,we,he = valid_bboxes[-1]
            dx = xe-xs
            dy = ye-ys
            if dx<10 and dy<10:
                continue
            dyd = 1 if dy==0 else dy
            xyr = dx/dyd
            if not 0.3<xyr<3:
                if abs(dx)>abs(dy):
                    if dx<0:
                        pos_dict[i] = "left"
                    else:
                        pos_dict[i] = "right"
                else:
                    if dy>0:
                        pos_dict[i] = "up"
                    else:
                        pos_dict[i] = "down"
            #print(valid_bboxes)
    return pos_dict

