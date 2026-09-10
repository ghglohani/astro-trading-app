[app]
title = AstroTrading
package.name = astrotrading
package.domain = org.astro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Pure Python library 'flatlib' - Android par 100% compile hoga
requirements = python3,kivy,flatlib

orientation = portrait
osx.kivy_version = 2.0.0
fullscreen = 0

# Android SDK/NDK Settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
