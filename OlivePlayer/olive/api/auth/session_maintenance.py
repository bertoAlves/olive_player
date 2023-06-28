import os, time, sys

current_time = time.time()
last_changed_date = current_time
while (current_time - last_changed_date) < 3600:
    try:
        last_changed_date = os.path.getmtime('../session')
    except:
        sys.exit('Session ended')    
    current_time = time.time()
    
os.remove('../session')
