import os

res_auth = '_'
res_link_lib = '_'

while(res_auth.strip() != '' and res_link_lib.strip() != ''):
    res_auth = os.popen("wmic process where CommandLine='flask  run -h localhost -p 100' get processid").read()
    res_player = os.popen("wmic process where CommandLine='flask  run -h localhost -p 200' get processid").read() 
    res_link_lib = os.popen("wmic process where CommandLine='flask  run -h localhost -p 300' get processid").read()

if res_auth.strip() == '':
    print('Auth server stopped running...')
    print('Stopping all servers')
    os.popen("wmic process where CommandLine='flask  run -h localhost -p 200' delete")
    os.popen("wmic process where CommandLine='flask  run -h localhost -p 300' delete")

if res_player.strip() == '':
    print('Player server stopped running...')
    print('Stopping all servers')
    os.popen("wmic process where CommandLine='flask  run -h localhost -p 100' delete")
    os.popen("wmic process where CommandLine='flask  run -h localhost -p 300' delete")   
    
if res_link_lib.strip() == '':
    print('Link Library server stopped running...')
    print('Stopping all servers')
    os.popen("wmic process where CommandLine='flask  run -h localhost -p 100' delete")
    os.popen("wmic process where CommandLine='flask  run -h localhost -p 200' delete")