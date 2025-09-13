[app]
title = DataPlotter
package.name = dataplotter
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.1
requirements = python3,kivy,kivy_garden.graph,fpdf,android
garden_requirements = graph
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.archs = arm64-v8a, armeabi-v7a
android.ndk_api = 21
# Assets (your gas.png must be in same folder or assets/)
presplash.filename = gas.png
icon.filename = gas.png

[buildozer]
log_level = 2
warn_on_root = 1
