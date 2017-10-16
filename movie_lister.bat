@echo off
setlocal

set PATH=R:\Pipe_Repo\Users\Qurban\applications\ffmpeg\bin;%PATH%
set PATH=R:\Pipe_Repo\Users\Qurban\applications\Python27;%PATH%

python R:\Pipe_Repo\Users\Qurban\applications\runables\movie_lister\movie_lister.py %*
