@echo off
echo ==============================
echo  Running IR Processing Scripts
echo ==============================
echo.

REM Jalankan semua file python berurutan
python translate\translate.py
if %errorlevel% neq 0 goto error

python stopword\Stopword.py
if %errorlevel% neq 0 goto error

python stemming\steming.py
if %errorlevel% neq 0 goto error

python tf-idf\tfidf_vector.py
if %errorlevel% neq 0 goto error

python cosine_simmiliarity\cosine_similarity.py
if %errorlevel% neq 0 goto error

python export_to_excel.py
if %errorlevel% neq 0 goto error

echo.
echo ✅ Semua proses selesai tanpa error.
pause
exit

:error
echo ❌ Terjadi error! Proses dihentikan.
pause
exit /b 1
