[app]

# (str) Title of your application
title = Data Plotter

# (str) Package name
package.name = dataplotter

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,ttf,txt

# (str) Application versioning (method 1)
version = 1.0

# (list) Garden requirements to install
garden_requirements = graph

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pango,fpdf,kivy-garden.graph,arabic_reshaper,python-bidi,kivy_text_provider_pango

# (str) Icon of the application
icon.filename = %(source.dir)s/gas.png

# (str) Supported orientation (one of landscape, sensorlandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually equal android.minapi.
android.ndk_api = 21

# (bool) If True, then automatically accept SDK license agreements.
android.accept_sdk_license = True

# (list) Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
