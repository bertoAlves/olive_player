start /D ..\olive\api\auth\routes\ flask run -h localhost -p 100

start /D ..\olive\api\player\routes\ flask run -h localhost -p 200

start /D ..\olive\api\link_library\routes\ flask run -h localhost -p 300

start server_maintenance.py

REM #--cert=adhoc

cd _PLAYER & start.py

exit