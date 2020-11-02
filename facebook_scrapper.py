
def get_fb_info(driver):
    # Warning: CSS selector may change with time
    elements = driver.find_elements_by_css_selector("._4bl9")
    likes = ""
    followers = ""
    for i in elements:
        #print(i.text)
        if "like" in i.text:
            likes = i.text.split(" ")[0]
        if "follow" in i.text:
            followers = i.text.split(" ")[0]
            
    return likes, followers


