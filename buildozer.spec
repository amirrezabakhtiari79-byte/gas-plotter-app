[app]
title = Data Plotter
package.name = dataplotter
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = gas.png,data.txt
version = 1.0
requirements = python3,hostpython3,kivy==2.2.1,kivy-garden.graph,fpdf,pyjnius
orientation = portrait
icon = gas.png

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 35
android.minapi = 21
android.ndk = 26.1.10909125
android.sdk = 35
android.arch = armeabi-v7a,arm64-v8a
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.add_aars = 
android.entrypoint = org.kivy.android.PythonActivity
p4a.branch = master
p4a.local_recipes = .
