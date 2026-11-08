#!/bin/bash
# Build Liquid Weather APK without Gradle: aapt2 + javac + d8 + apksigner.
#
# Requirements: JDK 17, Android SDK with platform android-34 and build-tools 34.0.0.
#   export ANDROID_SDK_ROOT=/path/to/android-sdk   (or ANDROID_HOME)
#   export JAVA_HOME=/path/to/jdk-17               (optional if java is on PATH)
set -e -o pipefail
cd "$(dirname "$0")"

SDK="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-$HOME/Android/Sdk}}"
BT=$(ls -d "$SDK"/build-tools/* 2>/dev/null | sort -V | tail -1)
AJAR=$(ls "$SDK"/platforms/android-*/android.jar 2>/dev/null | sort -V | tail -1)
if [ -z "$BT" ] || [ -z "$AJAR" ]; then
  echo "Android SDK not found. Set ANDROID_SDK_ROOT (needs platforms;android-34 and build-tools;34.0.0)." >&2
  exit 1
fi
echo "build-tools: $BT"
echo "android.jar: $AJAR"

rm -rf build && mkdir -p build/gen build/classes build/dex

echo "[1/6] aapt2 compile"
"$BT/aapt2" compile --dir res -o build/res.zip

echo "[2/6] aapt2 link"
"$BT/aapt2" link -o build/app-unsigned.apk \
  -I "$AJAR" \
  --manifest AndroidManifest.xml \
  build/res.zip \
  -A assets \
  --java build/gen \
  --min-sdk-version 23 --target-sdk-version 34 \
  --version-code 43 --version-name 1.7.4 \
  --no-version-vectors

echo "[3/6] javac"
javac --release 11 -nowarn -cp "$AJAR" -d build/classes \
  java/com/liquidweather/app/MainActivity.java \
  build/gen/com/liquidweather/app/R.java

echo "[4/6] d8"
"$BT/d8" --release --min-api 23 --lib "$AJAR" --output build/dex \
  $(find build/classes -name '*.class')

echo "[5/6] package + align"
(cd build/dex && zip -q -X ../app-unsigned.apk classes.dex)
"$BT/zipalign" -f -p 4 build/app-unsigned.apk build/app-aligned.apk

echo "[6/6] sign"
if [ ! -f release.keystore ]; then
  keytool -genkeypair -keystore release.keystore -alias liquidweather \
    -keyalg RSA -keysize 2048 -validity 10950 \
    -storepass liquidweather -keypass liquidweather \
    -dname "CN=Liquid Weather, OU=Mobile, O=Liquid Weather, L=Pune, S=Maharashtra, C=IN"
fi
"$BT/apksigner" sign --ks release.keystore --ks-pass pass:liquidweather \
  --key-pass pass:liquidweather --min-sdk-version 23 \
  --out build/LiquidWeather.apk build/app-aligned.apk

# Verify the signature that was just written, and insist it is this project's
# key. Two things were wrong with the old one-liner, `apksigner verify
# --print-certs ... | head -4`: the pipeline's exit status is head's, so a
# build that printed "DOES NOT VERIFY" still exited 0 and CI went green with an
# unsigned APK; and nothing checked *which* certificate signed it, so a build
# made with a different keystore also passed — an APK that cannot install over
# the published one. Verification output is captured and the signer digest is
# compared with the certificate named in CHECKSUMS.txt.
EXPECTED_CERT_SHA256="2035d69f949e12e56728cc83964fb7fa663c40fa45765cb3b880dc08229e3b8b"
"$BT/apksigner" verify --print-certs build/LiquidWeather.apk > build/verify.txt
head -4 build/verify.txt
if ! grep -qi "certificate SHA-256 digest: ${EXPECTED_CERT_SHA256}" build/verify.txt; then
  echo "ERROR: APK is not signed by the project key (expected ${EXPECTED_CERT_SHA256})." >&2
  echo "       Do not publish this build: it cannot install over the released app." >&2
  exit 1
fi
ls -lh build/LiquidWeather.apk
