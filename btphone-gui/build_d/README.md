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
pyinstaller -D *.py --hidden-import pyi_splash --splash SplashV1.0.png -i SplashV1.0.png -n btphone-gui
```
