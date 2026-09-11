[app]

# (str) Title of your application
title = Astro Trading App

# (str) Package name
package.name = astrotradingapp

# (str) Package domain
package.domain = org.astro

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
requirements = python3,kivy

# (str) Application versioning
version = 1.0.0

# (list) Permissions
permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK licenses
android.accept_sdk_license = True

# (str) Target Architecture
android.archs = arm64-v8a

# (bool) Enable AndroidX
android.enable_androidx = True

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
