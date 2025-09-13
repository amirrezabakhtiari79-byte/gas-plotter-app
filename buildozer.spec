[app]
title = Data Plotter
package.name = dataplotter
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = gas.png,data.txt
version = 1.0
requirements = python3,hostpython3,kivy==2.2.1,kivy-garden.graph,statistics,fpdf,pyjnius,hashlib
orientation = portrait
icon = gas.png

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.ndk = 23.1.7779620
android.sdk = 33
android.arch = armeabi-v7a,arm64-v8a
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.add_aars = 
android.entrypoint = org.kivy.android.PythonActivity
p4a.branch = master
p4a.local_recipes = .
