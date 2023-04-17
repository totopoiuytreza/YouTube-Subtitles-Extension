# YouTube-Subtitles-Extension

Install Whisper :

pip install git+https://github.com/openai/whisper.git

Install FFMPEG :
    - install Chocolatey : On cmd administration permission : 
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
    - install ffmpeg : choco install ffmpeg

Verify if packages are installed (Test on cmd or powershell):
    - python -V
    - ffmpeg
    - whisper

Warning, you need to verify (if you have multiple python), if whisper is installed in the python path you are currently using
Python needs to be version > 3.7 




RUN THE FLASK SERVER :
    - Be on the data repository : cd src
    - run command : set FLASK_APP=app.py
    - run command : flask run



 
