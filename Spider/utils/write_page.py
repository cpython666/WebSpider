def write_page(file_name,text):
    with open(file_name, "w",encoding="utf-8") as f:
        f.write(text)