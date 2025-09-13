[app]

# (str) Title of your application
title = Data Plotter

# (str) Package name
package.name = dataplotter

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,ttf,txt

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pango,kivy-garden.graph,fpdf,arabic-reshaper,bidi

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
#requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/gas.png

# (str) Supported orientation (one of landscape, sensorlandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://github.com/kivy/kivy/blob/master/doc/sources/guide/packaging-android.rst
# for more information about Lottie bundle folder requirements.
#android.presplash_lottie = "path/to/lottie/files.json"

# (str) Adaptive presplash lottie folder
#android.presplash_lottie_folder = <default>

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (list) features (adds uses-feature -tags to manifest)
#android.features = android.hardware.usb.host

# (int) Target Android SDK, should be as high as possible.
android.sdk = 33

# (str) Android NDK to use
#android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually equal android.minapi.
#android.ndk_api = 21

# (int) Android SDK version to use
#android.minapi = 21

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements.
# This is intended for automation only. If set to False, the default,
# you will be shown the license when first running buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA_*.jar or cudart*.jar or anything.jar (anything.jar will match anything)
# You can also use URL, for example:
# jars = https://mycompany.com/myproject.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar,https://mycompany.com/myproject.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Put these files or directories in the apk assets directory.
# Either form may be used, and assets need not exist or be in the local
# directory.
#android.add_assets = myapp.cfg
#android.add_assets = ./images/android-background.jpg

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' dependency.
#android.enable_androidx = False

# (list) add java compile options
# this can for example be necessary when using several pyjnius classes
# in the same package and using auto class loading.
# see https://github.com/kivy/python-for-android/pull/1804
#android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
# e.g. android.gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }"
#android.add_gradle_repositories =

# (list) packaging options to add 
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle_dependencies
# please enclose in double quotes 
# e.g. android.add_packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"
#android.add_packaging_options =

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) launchMode to use for the main activity
#android.manifest.launch_mode = standard

# (bool) If True, supporting screens element is added to the manifest
#android.manifest.create_screens_element = True

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
#android.uses_library =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Android logcat only display log for activity's pid
#android.logcat_pid_only = False

# (str) Android additional adb args to add when using logcat (i.e. "-d")
#android.adb_args = -H host.docker.internal

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic versionCode computation (used in yml)
# this is not the same as app version, it's an auto-increment within android studio
#android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) Name of keystore file for custom keystore, if not set fallback to the value of p4a.branch
# android.custom_keystore_name = %(p4a.branch)s

# (str) the signing key to use, passphrase will be prompted
# android.signing_key = upload-key.keystore

# (str) args to pass when using custom signing key
# android.signing_args = --ks-pass env:KEYSTORE_PASSWD

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64. Defaults to all.
#p4a.arch =

#
# python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android fork to use in case of using a custom fork or
# a development branch as a replacement for the stable master
#p4a.fork = kivy

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a.branch.
#p4a.commit = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port =

# Control whether buildozer generates Release or Debug builds
#p4a.debug = True

# (str) APACHE ANT version, must be the last version they
# will update, see https://ant.apache.org/bindownload.cgi
# for more information
#p4a.ant = 1.10.1

# (str) Android NDK version to use
#p4a.ndk = 25c

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#p4a.ndk_dir =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#p4a.sdk_dir =

# (str) ANDROID_SDK_HOME environment variable
#p4a.android_sdk_home =

# (str) Android NDK to use
#p4a.ndk = 25b

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#p4a.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#p4a.sdk_path =

# (str) Android NDK version to use
#p4a.ndk_version =

# (str) Android SDK version to use
#p4a.sdk =

# (str) Android NDK API to use. This is the minimum API your app will support, it should usually equal android.minapi.
#p4a.ndk_api = 21

# (str) Android SDK build tools version
#p4a.build_tools = 34.0.0

# (str) Android SDK Platform tools version
#p4a.platform_tools = 34.0.5

# (str) Android SDK command line tools version
#p4a.cmdline_tools = 11.0

# (str) Gradle version
#p4a.gradle = 8.5

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir =

 # (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team to use for signing the debug version
#ios.codesign.development_team.debug = <hexstring>

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s


# (str) The development team to use for signing
#ios.codesign.development_team.release = %(ios.codesign.development_team.debug)s

# (str) URL pointing to .ipa file to be installed
# This option should be defined along with `display_image_url` and `full_size_image_url` options.
#ios.manifest.app_url =

# (str) URL pointing to an icon (57x57px) to be displayed during download
# This option should be defined along with `app_url` and `full_size_image_url` options.
#ios.manifest.display_image_url =

# (str) URL pointing to a large icon (512x512px) to be used by iTunes
# This option should be defined along with `app_url` and `display_image_url` options.
#ios.manifest.full_size_image_url =


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    # List as sections containing values as tuples or single strings, e.g.:
#    #    [ (S.section1, key1, val1), (S.section1, key2, val2), ...
#    #      (S.section2, key3, val3) ]
#    #
#    # S.sectionN are references to the source 
#    # installable (created by bdist_ext and containing S.dist_dir) sections,
#    # S."section1" are references to the top level source section. Keys
#    # are "(section|key <=> val)", where key belongs to the section.
