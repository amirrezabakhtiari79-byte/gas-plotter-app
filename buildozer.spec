[app]
# ... (keep existing)

# (int) Android SDK version to use
android.sdk = 34  # Upgrade from 33 for better Gradle 8.x support

# (str) Android NDK version to use
android.ndk = 25c  # Slight upgrade from 25b for stability

# (int) Android SDK build tools version
android.build_tools = 34.0.0

# (bool) Enable AndroidX support (already implied, but explicit)
android.enable_androidx = True

[android]
# (str) Gradle dependencies to add
android.gradle_dependencies =  # Empty unless you add libs (e.g., for ads)

# (list) add java compile options
android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8", "-Xmx2048m"  # Heap boost + Java 8 compat

# (str) args to pass when using custom signing key (for debug, adds heap)
# android.signing_args = --ks-pass env:KEYSTORE_PASSWD (skip for debug)

[buildozer]
# ... (keep existing)

# (int) Target Android SDK, should be as high as possible.
android.sdk = 33  # Back to 33 (stable with Java 17)

# (str) Android NDK to use
android.ndk = 25b  # Back to 25b

# (int) Android SDK build tools version
android.build_tools = 33.0.2  # Match SDK 33

# (list) add java compile options
android.add_compile_options = "sourceCompatibility = 17", "targetCompatibility = 17", "-Xmx2048m"  # Java 17 compat + heap
