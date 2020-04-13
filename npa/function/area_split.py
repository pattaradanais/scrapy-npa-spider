
def area_split(area):
  
    if '-' in area:
        splited = area.split('-')
        if len(splited) >= 3:
            try:
                rai = splited[0]
                ngan =splited[1]
                sq_wa = splited[2].split('/')[0]
            except:
                sq_wa = splited[2]
                rai = splited[0]
                ngan =splited[1]
        elif len(splited) == 2:
            rai = splited[0]
            ngan = int(float(splited[1].split('/')[0])/100)
            sq_wa = float(splited[1].split('/')[0]) % 100

    else:
        sq_wa = 0
        ngan = 0
        rai = 0
    area_dict = {
        'rai' : rai,
        'ngan' : ngan,
        'sq_wa' : sq_wa,
    }

    return area_dict