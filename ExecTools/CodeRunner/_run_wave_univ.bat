@ECHO OFF

CALL ..\config\common_vars.bat > NUL
CALL ..\config\dbase_data_migr.bat > NUL

ECHO ------------------------------------------
ECHO Started:
ECHO Current local date:  %date%
ECHO Current local time:  %time%
ECHO Current file suffix: %datetimef%
ECHO Environment prefix:  %env%
ECHO sed cmd path:        %sed%
ECHO sed command:         %sed_cmd%
ECHO SQL executor path:   %sql_cmd%
ECHO Server IP address:   %dbserver%
ECHO Database login:      %dbuser%
ECHO Database password:   ***
ECHO Database name:       %dbdb%
ECHO Waves count:         %waves%
ECHO ==========================================

DEL .\OUT%1\*.log 2> NUL
DEL .\OUT%1\*.err 2> NUL

FOR /L %%w in (1,1,%waves%) DO (
    ECHO Wave %%w

    FOR %%i in (.\IN%1\*.%%w.sql) DO (
        ECHO Script %%i
        %sed_cmd% -e s/@ENV@/%ENV%/gi "%%i" > ".\WRK\%%~ni.sql"
        %sql_cmd% -j -W -s ^| -h -1 -f 1250 -S %dbserver% -U %dbuser% -P "%dbpass%" -d %dbdb% -i ".\WRK\%%~ni.sql" -o ".\OUT%1\%%~ni.log"

        FINDSTR "\[Microsoft" ".\OUT%1\%%~ni.log" | FINDSTR /V /C:"Null value is eliminated by an" | SORT /UNIQUE > ".\OUT%1\%%~ni.err"
    )
)
FOR %%F IN (.\OUT%1\*.err) DO IF %%~zF==0 DEL "%%F"

rem DEL .\OUT%1\*.log 2> NUL

ECHO ==========================================
ECHO Finished:
ECHO Current local date: %date%
ECHO Current local time: %time%
ECHO ------------------------------------------

ECHO ON

