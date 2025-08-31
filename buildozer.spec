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

# Android config
android.api = 34
android.ndk_path = /home/runner/android-sdk/ndk/25.1.8937393
android.sdk_path = /home/runner/android-sdk
android.accept_sdk_license = True
android.enable_androidx = True
# prevent Buildozer from trying to install/upgrade SDK stuff
android.skip_update = True

android.ndk_version = r25b

[buildozer]
log_level = 2
warn_on_root = 1
