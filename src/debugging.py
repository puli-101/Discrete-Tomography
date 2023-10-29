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

def toggle(graphics=False):
    global GRAPHICS_DEBUG
    global COLOR_PRINTING
    global DEBUG
    GRAPHICS_DEBUG = graphics