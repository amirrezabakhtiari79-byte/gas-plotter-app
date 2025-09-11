[app]

# (str) Title of your application
title = Gas Data Plotter

# (str) Package name
package.name = gasplotter

# (str) Package domain (needed for Android)
package.domain = org.company.gasplotter

# (str) Source code directory (if not the same as the spec file)
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,ttf,txt,json

# (str) Application versioning scheme
version = 1.0

# (list) Application requirements
# This is the most important line for your app. It includes:
# - Kivy and its dependencies (pyjnius)
# - The Farsi text rendering fixes (pango, reshaper, bidi)
# - PDF and Graphing libraries
# - The direct GitHub link for the biometric library
requirements = python3,kivy==2.1.0,pyjnius,kivy-garden.graph,fpdf,arabic_reshaper,python-bidi,kivy_text_provider_pango,kivy_biometric @ git+https://github.com/kivy-garden/kivy_biometric.git

# (str) Custom source folders for requirements
# requirements.source.kivy_biometric = /path/to/kivy_biometric

# (str) Presplash background color (for new android AAB)
# android.presplash_color = #FFFFFF

# (str) Presplash image
presplash.filename = %(source.dir)s/gas.png

# (str) Icon of the application
icon.filename = %(source.dir)s/gas.png

# (str) Supported orientation (one of landscape, portrait, all)
orientation = portrait


[android]

# (list) The Android archs to build for. arm64-v8a is required for the Play Store.
android.archs = arm64-v8a

# (list) Android permissions
# INTERNET is a good default, and USE_BIOMETRIC is required for the fingerprint feature.
android.permissions = INTERNET, USE_BIOMETRIC

# (int) Android API level to use. Let buildozer choose a sensible default.
# android.api = 31

# (int) Minimum API level your app supports (Android 5.0)
android.minapi = 21

# (bool) Accept the SDK license agreements
android.accept_sdk_license = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (very verbose))
# Set to 2 for debugging build errors.
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
