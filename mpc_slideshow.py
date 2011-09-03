# for media player classic
# option -> player -> web interface -> check "listen on port"

import urllib
import urllib2
import os
import time
import random
import re
import traceback

# config
addr = "localhost"
port = "13579"
playtime_range = (20, 30) # (min, max) in seconds
search_path = [u"C:\\bt", u"E:\\bt", u"E:\\video\\av"]
file_types = [u"avi", u"wmv", u"mkv"]
smaller_window = True
always_ontop = True

def mpc_post(arg):
    return urllib2.urlopen("http://%s:%s/%s" % (addr, port, arg))

def mpc_ontop():
    mpc_post("command.html?wm_command=884")

def mpc_open(mov):
    mpc_post("browser.html?path=%s" % mov)

def mpc_zoom_50():
    mpc_post("command.html?wm_command=832")

def mpc_duration():
    f = mpc_post("controls.html")
    m = re.search('<td\s*id="time">.*</td>\s*<td>.*</td>\s*<td>(.*)</td>', f.read())
    return m.group(1)

def mpc_jump(time):
    mpc_post("command.html?wm_command=-1&position=%s" % time)

def rand_time(time, preserved=0):
    h, m, s = time.split(":")
    s = int(h)*3600 + int(m)*60 + int(s)
    s = random.randint(0, s - preserved)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return "%02d:%02d:%02d" % (h, m, s)

def get_movies(dirs):
    movs = []
    for folder in dirs:
        for root, dirs, files in os.walk(folder):
            for f in files:
                for ext in file_types:
                    if f.lower().endswith(ext):
                        movs.append(os.path.join(root, f))
    return movs

if __name__ == '__main__':
    movs = get_movies(search_path)
    if always_ontop:
        mpc_ontop()
    while True:
        mov = random.choice(movs)
        print mov
        playtime = random.randint(playtime_range[0], playtime_range[1])
        try:
            mpc_open(mov)
            if smaller_window:
                mpc_zoom_50()
            duration = mpc_duration()
            t = rand_time(duration, playtime)
            mpc_jump(t)
            print "jump to %s / %s" % (t, duration)
        except:
            traceback.print_exc()
        time.sleep(playtime)
