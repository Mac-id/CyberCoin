[app]
title = CyberCoin
package.name = cybercoin
package.domain = org.pixelart

source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf

version = 0.1

# Requirements inklusive Pillow für bessere Bildverarbeitung und Cython-Fix
requirements = python3,kivy==2.3.1,pillow

orientation = portrait
fullscreen = 1

# Android Spezifikationen
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.2

# Berechtigungen für JsonStore/Speichern von Einstellungen
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1