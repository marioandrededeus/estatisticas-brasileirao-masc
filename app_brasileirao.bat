set root=C:\ProgramData\Anaconda3
call %root%\Scripts\activate.bat
call activate pycaret3
call streamlit run "C:\Users\m4005001\Documents\_SG\Pessoal\Estatisticas_Brasileirao\estatisticas-brasileirao-masc\app\app.py" --theme.base="light"
PAUSE