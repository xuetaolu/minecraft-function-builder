import os

file = 'png\\001.png'

cwd  = os.getcwd()

path = '\\'.join([cwd, file])

print(path)

os.system(f'pngTellRaw.exe "{path}"')