
set file=%1
if %file%.==. goto noparam

if exist ".env" (
python -m virtualenv .env
call .env/Scripts/activate.bat
@echo on
python -m pip install -r requirements.txt
) else (
call .env/Scripts/activate.bat
@echo on
)
pyinstaller --noconfirm %file%
goto end

:noparam
echo filename not set
echo usage docker run -v .:/app/src --workdir /app/src -it pywininstaller main.py

:end
