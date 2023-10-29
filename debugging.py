DEBUG = False
GRAPHICS_DEBUG = False 
COLOR_PRINTING = False

def log(msg='', end='\n',override=False):
    msg = str(msg)
    if DEBUG or override:
        print(msg,end=end)

def log_img(G):
    if GRAPHICS_DEBUG:
        G.save_grid()