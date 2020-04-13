


def str_concat(list_of_str):
    for item in list_of_str:
        item = item.strip()
    full_str = " ".join(list_of_str)
    return full_str

def str_concat_nospace(list_of_str):
    for item in list_of_str:
        item = item.strip()
    full_str = "".join(list_of_str)
    return full_str

def str_concat_comma(list_of_str):
    for item in list_of_str:
        item = item.strip()
    full_str = ", ".join(list_of_str)
    return full_str