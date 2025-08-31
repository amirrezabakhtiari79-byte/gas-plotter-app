[app]
title = Gas Plotter
package.name = gasplotter
package.domain = org.mycompany.gasplotter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt
version = 0.1
requirements = python3,kivy==2.1.0,kivy_garden.graph,arabic_reshaper,python-bidi
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1

# STABILITY FIXES
android.ndk_version = r25b
# API 33 is the latest stable, works fine for Play Store
android.api = 33
android.build_tools_version = 33.0.2
android.accept_sdk_license = True
android.enable_androidx = True

