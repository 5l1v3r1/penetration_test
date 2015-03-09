rem Description: Win Juicy info extractor 
rem Author: greyshell

echo 1. Search the file system for file names containing keywords - "pass,cred,vnc,config" > my_win_juice.txt
echo ------------------------------------------------------------------------------------->> my_win_juice.txt
echo. >> my_win_juice.txt
dir /s  *pass* == *cred* == *vnc* == *config* == *sysprep* == *unattended* >> my_win_juice.txt
dir /s  /a:h *pass* == *cred* == *vnc* == *config* == *sysprep* == *unattended* >> my_win_juice.txt

echo. >> my_win_juice.txt
echo 2. Search a keyword "password" inside few certain types of files: txt, xml, ini >> my_win_juice.txt
echo ------------------------------------------------------------------------------->> my_win_juice.txt
echo.>> my_win_juice.txt
findstr /si password *.xml *.ini *.txt >> my_win_juice.txt
echo.>> my_win_juice.txt

echo. >> my_win_juice.txt
echo 3. Search inside registry HKLM,HKCU for keyword - "password" >> my_win_juice.txt
echo ------------------------------------------------------------>> my_win_juice.txt
echo. >> my_win_juice.txt
reg query HKLM /f password /t REG_SZ /s >> my_win_juice.txt
reg query HKCU /f password /t REG_SZ /s  >> my_win_juice.txt






