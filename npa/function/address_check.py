import json


with open('./assets/thailand.json',encoding='utf8') as json_file:
    data = json.load(json_file)


def address_check(address):
    p_value = ""
    d_value = ""
    sub_d_value = ""

    #find province from address string
    for province in data: 
        for lang in data[province]['name']:
            if str(data[province]['name'][lang]) in address:  #in data address from scraping data
                p_value = data[province]['name'][lang]
                # print(data[province]['name'][lang])

    #find district from address string            
                for district in data[province]['amphoes']:
                    for d_lang in data[province]['amphoes'][district]['name']:
                        if ("เขต" + str(data[province]['amphoes'][district]['name'][d_lang])) in address or ("อ." + str(data[province]['amphoes'][district]['name'][d_lang])) in address or ("อำเภอ" + str(data[province]['amphoes'][district]['name'][d_lang])) in address:
                            d_value = data[province]['amphoes'][district]['name'][d_lang]
                            # print(data[province]['amphoes'][district]['name'][d_lang])

    #find sub_district from address string 
                            for sub_district in data[province]['amphoes'][district]['tambons']:
                                for sub_d_lang in data[province]['amphoes'][district]['tambons'][sub_district]['name']:
                                    if str(data[province]['amphoes'][district]['tambons'][sub_district]['name'][sub_d_lang]) in address:
                                        sub_d_value = data[province]['amphoes'][district]['tambons'][sub_district]['name'][sub_d_lang]
                                        # print(data[province]['amphoes'][district]['tambons'][sub_district]['name'][sub_d_lang])

    #------------------------------------------ End for ------------------------------------------------

    return {
        'province': p_value,
        'district': d_value,
        'sub_district': sub_d_value
    }

    #------------------------------------------ End func ------------------------------------------------
       


# print(address_check(" 516 โครงการ เดอะไพรเวท (เจ้าพระยา 3) แขวงศาลาธรรมสพน์ เขตทวีวัฒนา จังหวัดกรุงเทพมหานคร"))

