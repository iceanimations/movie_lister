@echo off
setlocal

set PATH=R:\Pipe_Repo\Users\Qurban\applications\ffmpeg\bin;%PATH%
set PATH=R:\Pipe_Repo\Users\Qurban\applications\Python27;%PATH%

python movie_lister.py %*
