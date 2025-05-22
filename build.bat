@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Building application...
python -m PyInstaller mundo_de_letras.spec

xcopy "./MUNDO_DE_LETRAS/ImagenesLecturas" "./dist/ImagenesLecturas" /E /I /Y
xcopy "./MUNDO_DE_LETRAS/lista_ejercicios" "./dist/lista_ejercicios" /E /I /Y
xcopy "./MUNDO_DE_LETRAS/preguntas/lecturas.db" "./dist/preguntas" /I /Y
xcopy "./MUNDO_DE_LETRAS/recursos" "./dist/recursos" /E /I /Y
xcopy "./MUNDO_DE_LETRAS/reporte" "./dist/reporte" /E /T /I /Y
xcopy "./MUNDO_DE_LETRAS/respuestas" "./dist/respuestas" /E /T /I /Y

echo Build completed!
echo The executable is located in the 'dist' folder.
pause