[app]
title = CyberCoin
package.name = cybercoin
package.domain = org.pixelart

source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf

version = 0.1

# Wir fügen 'sh' und 'six' hinzu, da Kivy-Interna das oft brauchen
requirements = python3,kivy==2.3.1,pillow,sh,six,cython==3.0.10
orientation = portrait
fullscreen = 1

# Erhöhung der API auf 34 (Standard für 2024/25) und NDK Fix
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25c
android.build_tools_version = 34.0.0

# Berechtigungen entfernt, da sie auf Android 13+ oft blockiert werden 
# und für den internen App-Speicher (user_data_dir) nicht benötigt werden.
# android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
