@echo off
REM Script para gerar o ícone PNG, converter para ICO e compilar o executável com PyInstaller

REM Passo 1: Gerar o ícone PNG
python generate_icon.py
if errorlevel 1 (
    echo Erro ao gerar o ícone PNG.
    exit /b 1
)

REM Passo 2: Converter PNG para ICO automaticamente
python convert_png_to_ico.py
if errorlevel 1 (
    echo Erro ao converter PNG para ICO.
    exit /b 1
)

REM Passo 3: Compilar o executável com PyInstaller
pyinstaller --onefile --noconsole --clean --log-level=WARN --icon=app_icon.ico cfg_value_modifier.py
if errorlevel 1 (
    echo Erro ao compilar o executável.
    exit /b 1
)

echo Compilação concluída com sucesso.
pause
