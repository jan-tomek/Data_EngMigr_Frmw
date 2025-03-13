@ECHO OFF

ECHO Current local date:  %date%
ECHO Current local time:  %time%

SET datetimef=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
SET datetimef=%datetimef: =0%
ECHO Datetime suffix:     %datetimef%

SET env=%cd:~-7,-5%
ECHO Environment prefix:  %env%

SET dir=%cd%
ECHO Local directory:     %dir%

SET repo=C:\_migr\mapping
ECHO Repository:          %repo%

SET zip_cmd="C:\Program Files\7-Zip\7z.exe"
