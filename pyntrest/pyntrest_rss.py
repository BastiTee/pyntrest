from pyntrest_config import RSS_ENABLED, RSS_REFRESH_INTERVAL_SEC
from os import walk, path
from time import sleep, time
import threading
    
def rss_init (main_images_path, file_pattern):

    if not RSS_ENABLED:
        print 'RSS feature disabled.'
        return
    interval = 5
    if RSS_REFRESH_INTERVAL_SEC < 5:
        interval = 5
        
    sleep(1)
    t1 = threading.Thread(target=rss_refresh, 
                          args=(main_images_path, interval, file_pattern))
    t1.start()
 
def rss_refresh(main_images_path, interval, file_pattern):
    
    print 'RSS :: Main images path: {}'.format(main_images_path)
    print 'RSS :: Refresh interval: {}'.format(interval)
    
    while True:
        print 'RSS :: Refresh start-time: {}'.format(time())
         
        for dirname, _, filenames in walk(main_images_path):
            if '\.' in dirname:
                continue
            dir_ctime = path.getctime(dirname)
            print 'RSS :: WALK :: DIR - {} [{}]'.format(dirname, dir_ctime)
            for filename in filenames:
                absolute_path = path.join(dirname, filename)
                if '\.' in absolute_path:
                    continue
                file_ctime = path.getctime(absolute_path)
                print 'RSS :: WALK ::     - {} [{}]'.format(absolute_path,
                                                       file_ctime)
        
        print 'RSS :: Refresh end-time: {}'.format(time())
        sleep(interval)
