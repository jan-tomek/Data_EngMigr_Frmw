@ECHO OFF

CALL ..\config\dbase_data_migr.bat > NUL

ECHO ------------------------------------------
ECHO Started:
ECHO Current local date:  %date%
ECHO Current local time:  %time%
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

DEL .\3_LOG\*.log 2> NUL

FOR %%i IN (.\1_IN\*.xlsx) DO (
    ECHO %%i
    @py ExcelLoader.py --infile "%%i" --manual --codetest

    DEL .\2_RUN\*.sql 2> NUL
    MOVE .\1_IN\*.sql .\2_RUN\ > NUL 2> NUL
    DEL .\1_IN\*.sql 2> NUL
    FOR %%j IN (.\2_RUN\*.sql) DO (
        ECHO %%j
        %sed_cmd% -e s/@ENV@/%ENV%/gi "%%j" > ".\Y_WRK\%%~nj.sql"
        %sql_cmd% -j -W -s ^| -h -1 -f 65001 -S %dbserver% -U %dbuser% -P "%dbpass%" -d %dbdb% -i ".\Y_WRK\%%~nj.sql" -o ".\3_LOG\%%~nj.log"

        COPY "%%j" .\X_ALL\ > NUL 2> NUL
        COPY ".\3_Log\%%~nj.log" .\X_ALL\ > NUL 2> NUL

        FINDSTR "[" ".\3_LOG\%%~nj.log" | SORT /UNIQUE > ".\3_LOG\%%~nj.err" 2> NUL

        COPY ".\3_LOG\%%~nj.err" .\X_ALL\ > NUL 2> NUL

    )
    COPY "%%i" .\X_ALL\ > NUL 2> NUL
    MOVE "%%i" .\4_DONE\
)
FOR %%F IN (.\3_LOG\*.err) DO IF %%~zF==0 DEL "%%F"
FOR %%F IN (.\x_ALL\*.err) DO IF %%~zF==0 DEL "%%F"

ECHO ==========================================
ECHO Finished:
ECHO Current local date: %date%
ECHO Current local time: %time%
ECHO ------------------------------------------

ECHO ON

