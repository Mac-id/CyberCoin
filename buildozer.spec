[app]
title = FLIP IT
package.name = cybercoin
package.domain = org.pixelart

source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf

version = 0.1
icon.filename = pixil-frame-0-startkopf.png

# 'sh' und 'six' entfernt, werden nicht auf dem Gerät benötigt
requirements = python3,kivy==2.3.1,pillow

orientation = portrait
fullscreen = 1

android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25c
android.build_tools_version = 34.0.0

# Rechte entfernt, da die App nun in den internen Speicher schreibt
# android.permissions = 
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1