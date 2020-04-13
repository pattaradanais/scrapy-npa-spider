from w3lib.html import remove_tags

def remove_html(text_data):
    cleaned_data = ''
    try:
        cleaned_data = remove_tags(text_data)
    except TypeError:
        cleaned_data = 'No data'
    return cleaned_data

def remove_space_tag(text_data):
    if "\n" in text_data:
        text_data.replace('\n','')
    if "&nbsp" in text_data:
        text_data.replace('&nbsp','')
    return text_data