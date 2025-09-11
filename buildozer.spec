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
# THIS IS THE MOST IMPORTANT LINE IN THE ENTIRE FILE.
# It tells the builder to get kivy_biometric directly from GitHub.
requirements = python3,kivy==2.1.0,pyjnius,kivy-garden.graph,fpdf,arabic_reshaper,python-bidi,kivy_text_provider_pango,kivy_biometric @ git+https://github.com/kivy-garden/kivy_biometric.git

# (str) Presplash image
presplash.filename = %(source.dir)s/gas.png

# (str) Icon of the application
icon.filename = %(source.dir)s/gas.png

# (str) Supported orientation
orientation = portrait


[android]

# (list) The Android archs to build for. arm64-v8a is required for the Play Store.
android.archs = arm64-v8a

# (list) Android permissions (USE_BIOMETRIC is required for fingerprint)
android.permissions = INTERNET, USE_BIOMETRIC

# (int) Minimum API level your app supports (Android 5.0)
android.minapi = 21

# (bool) Accept the SDK license agreements automatically
android.accept_sdk_license = True


[buildozer]

# (int) Log level (2 = very verbose for debugging)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
