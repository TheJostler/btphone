Install pyinstaller: 

[Click here to find out more](https://pypi.org/project/pyinstaller/)

```
pip install pyinstaller
```

Install any other required modules using pip again

```
pip install <Module>
```

and run this command inside this directory to compile:

```
pyinstaller -F *.py --hidden-import pyi_splash --splash SplashV1.1.png -i SplashV1.1.png -n btphone-gui
```
```

If you are a developer compliling a release, please remember to copy res(dir) into dist/btphone-gui and rename the executable in the final directory to 'run'

Also please compress into a .tar.7z archive named with the following naming convention:

btphone_<OS>_<CPU-ARCH>_<VERSION>.tar.7z

e.g:

btphone_linux_x86_64_v1.1.tar.7z

(No Caps) - Thnx
