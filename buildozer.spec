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

# --- Android Settings ---
android.api = 31
android.ndk_version = r25b
android.enable_androidx = True

# SOLUTION 3: Pin the SDK path to the one set up by the workflow
android.sdk_path = /usr/local/lib/android/sdk
