[app]
# (str) Title of your application
title = Gas Plotter

# (str) Package name
package.name = gasplotter

# (str) Package domain (must be unique)
package.domain = org.mycompany.gasplotter

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (extensions)
source.include_exts = py,png,jpg,kv,atlas,ttf,txt

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.1.0,kivy_garden.graph,arabic_reshaper,python-bidi

# (str) Application orientation (portrait, landscape or all)
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 1


[buildozer]
# (int) Logging level (0 = error only, 1 = warning, 2 = info, 3 = debug, 4 = trace)
log_level = 2

# (bool) Warn when root access is detected
warn_on_root = 1

# (str) Android NDK version (must match installed version)
android.ndk_version = r25b

# (int) Android API level to use
android.api = 33

# (str) Android build tools version (must match installed version)
android.build_tools_version = 33.0.2

# (str) Path to preinstalled Android SDK (we set this in GitHub Actions)
android.sdk_path = $HOME/android-sdk

# (bool) Automatically accept SDK licenses
android.accept_sdk_license = True

# (bool) Enable AndroidX
android.enable_androidx = True
