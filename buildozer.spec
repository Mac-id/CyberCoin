[app]
# (str) Title of your application
title = CyberCoin

# (str) Package name
package.name = cybercoin

# (str) Package domain (needed for android packaging)
package.domain = org.pixelart

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,kv

# (str) Application versioning
version = 0.1

# (list) Application requirements - WICHTIG: sqlite3 für Kivy-Stabilität
requirements = python3,kivy==2.3.1,sqlite3

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (int) Target Android API (33 ist oft stabiler als 34 für Kivy 2.3.1)
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) use GNU STL instead of C++ shared
android.copy_libs = 1

# (bool) Enable AndroidX support (wichtig für moderne APIs)
android.enable_androidx = True

[buildozer]
# (int) Log level (2 für maximales Feedback in den GitHub Logs)
log_level = 2

warn_on_root = 1