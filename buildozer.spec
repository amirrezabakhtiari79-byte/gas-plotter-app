[app]
title = Gas Plotter
package.name = gasplotter
package.domain = org.mycompany.gasplotter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,json
source.exclude_exts = spec
source.exclude_dirs = tests, bin, venv
source.exclude_patterns = license, *.pyc
requirements = python3,kivy==2.3.0,kivy-garden.graph,fpdf,arabic-reshaper,python-bidi,pyjnius
android.permissions = INTERNET,USE_BIOMETRIC,USE_FINGERPRINT
orientation = portrait
fullscreen = 1
version = 0.1

[buildozer]
log_level = 2
warn_on_root = 1

# --- Android Settings ---
android.accept_sdk_license = True
android.sdk = 33
android.ndk = r25b
android.minapi = 21
android.api = 31
android.build_tools = 34.0.0
android.enable_androidx = True
p4a.branch = develop
android.skip_update = True
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-sdk/ndk/25.1.8937393
