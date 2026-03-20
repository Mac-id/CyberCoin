[app]
title = FLIP IT
package.name = flipit
package.domain = org.pixelart
icon.filename = %(source.dir)s/assets/pixel-frame-0-startkopf.png

source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf
source.include_patterns = assets

version = 0.1

requirements = python3, kivy, pyjnius, pillow, sh, six
orientation = portrait
fullscreen = 1

android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.build_tools_version = 34.0.0

android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
