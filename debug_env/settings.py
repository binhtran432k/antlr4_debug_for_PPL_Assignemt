languageName = "csel"

import os
targetPath = f'../target/main/{languageName}/parser' if os.name == 'posix' else os.path.normpath('../target/')
locpath = [
    f'./main/{languageName}/checker/',
    f'./main/{languageName}/parser/',
    f'./main/{languageName}/astgen/',
    f'./main/{languageName}/utils/',
    './test/',
    targetPath
]