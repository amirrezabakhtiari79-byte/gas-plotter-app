[app]

# (str) Title of your application
title = Gas Data Plotter

# (str) Package name
package.name = gasplotter

# (str) Package domain (needed for Android)
package.domain = org.company.gasplotter

# (str) Source code directory
source.dir = .

# (list) Source files to include (py, graphics, fonts, data, etc.)
source.include_exts = py,png,jpg,ttf,txt,json

# (str) Application versioning scheme
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.1.0,kivy-garden.graph,fpdf

# --- FIX: Added a splash screen to hide the black screen on startup ---
# (str) Presplash image
presplash.filename = %(source.dir)s/gas.png

# (str) Icon of the application
icon.filename = %(source.dir)s/gas.png

# (str) Supported orientation
orientation = portrait


[android]

# (list) The Android archs to build for. arm64-v8a is required for the Play Store.
android.archs = arm64-v8a

# (list) Android permissions needed for file saving/reading.
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Android API to target. 34 is the modern standard for new apps.
android.api = 34

# (int) Minimum API level your app supports (Android 5.0)
android.minapi = 21

# (str) Android NDK version to use. 25b is a stable choice.
android.ndk = 25b

# (str) Android build tools version. 34.0.0 is the corresponding modern version.
android.build_tools = 34.0.0

# (bool) Accept the SDK license agreements automatically
android.accept_sdk_license = True


[buildozer]

# (int) Log level (2 = very verbose for debugging)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
```
