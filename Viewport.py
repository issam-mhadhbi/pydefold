import webbrowser

def check_whatsapp(number):
    # number must be in international format without +
    url = f"https://wa.me/{number}"
    webbrowser.open(url)

# Example
check_whatsapp("49918190915323")