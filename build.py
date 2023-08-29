import os, shutil
from mojo.extensions import ExtensionBundle

basePath = os.path.dirname(__file__)
sourcePath = os.path.join(basePath, 'source')
libPath = os.path.join(sourcePath, 'code')
htmlPath = os.path.join(sourcePath, 'docs')
resourcesPath = os.path.join(sourcePath, 'resources')
licensePath = os.path.join(basePath, 'LICENSE.txt')
pycOnly = False
extensionFile = 'LassoTool.roboFontExt'
extensionPath = os.path.join(basePath, extensionFile)

B = ExtensionBundle()
B.name = "LassoTool"
B.developer = 'TypeMyType'
B.developerURL = 'http://www.typemytype.com'
B.icon = None
B.version = '2.0'
B.launchAtStartUp = True
B.mainScript = 'lassoTool.py'
B.html = True
B.requiresVersionMajor = '4'
B.requiresVersionMinor = '4b'
B.addToMenu = []

with open(licensePath) as license:
    B.license = license.read()

# copy README + images to extension docs
if not os.path.exists(htmlPath):
    os.makedirs(htmlPath)
shutil.copyfile(os.path.join(basePath, 'README.md'), os.path.join(htmlPath, 'index.md'))

print('building extension...', end=' ')
B.save(extensionPath, libPath=libPath, htmlPath=htmlPath, resourcesPath=resourcesPath, pycOnly=pycOnly)
print('done!')

print()
print(B.validationErrors())
