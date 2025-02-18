# APPIUM OFFICE INSTALL GUIDE

https://appium.io/docs/en/latest/quickstart/install/

# 客户端版本

appium-python-client==4.1.0
PyYAML==5.4.1
selenium==3.141.0

pip uninstall appium-python-client
pip install appium-python-client
pip show appium-python-client
Version: 4.1.0

# 服务端版本

npm uninstall -g appium
npm install -g appium
appium -v
2.11.3

pip uninstall appium-python-client
npm uninstall -g appium

1. npm install -g appium
2. appium driver install uiautomator2
3. appium driver doctor uiautomator2
4. pip install Appium-Python-Client

paycharm install black formater

info Doctor ### Starting doctor diagnostics ###
info Doctor ✔ ANDROID_HOME is set to: C:\Users\lionf\AppData\Local\Android\Sdk
info Doctor Checking adb, emulator, apkanalyzer.bat
info Doctor      'adb' exists in C:\Users\lionf\AppData\Local\Android\Sdk\platform-tools\adb.exe
info Doctor      'emulator' exists in C:\Users\lionf\AppData\Local\Android\Sdk\emulator\emulator.exe
WARN Doctor ✖ apkanalyzer.bat could NOT be found in 'C:\Users\lionf\AppData\Local\Android\Sdk'!
info Doctor ✔ JAVA_HOME is set to: C:\Program Files\Java\jdk-22\
info Doctor ✔ 'bin\java.exe' exists under 'C:\Program Files\Java\jdk-22\'
WARN Doctor ✖ bundletool.jar cannot be found
WARN Doctor ✖ ffmpeg.exe cannot be found
WARN Doctor ✖ gst-launch-1.0.exe and/or gst-inspect-1.0.exe cannot be found
info Doctor ### Diagnostic completed, 1 required fix needed, 3 optional fixes possible. ###
info Doctor
info Doctor ### Manual Fixes Needed ###
info Doctor The configuration cannot be automatically fixed, please do the following first:
WARN Doctor ➜ Manually install Android SDK and set ANDROID_HOME. Read https://developer.android.com/studio#cmdline-tools
and https://developer.android.com/studio/intro/update#sdk-manager.
info Doctor
info Doctor ### Optional Manual Fixes ###
info Doctor To fix these optional issues, please do the following manually:
WARN Doctor ➜ ffmpeg.exe is used to capture screen recordings from the device under test. Please
read https://www.ffmpeg.org/download.html.
WARN Doctor ➜ gst-launch-1.0.exe and gst-inspect-1.0.exe are used to stream the screen of the device under test. Please
read https://gstreamer.freedesktop.org/documentation/installing/index.html?gi-language=c.
info Doctor
info Doctor ###
info Doctor
info Doctor Bye! Run doctor again when all manual fixes have been applied!
info Doctor