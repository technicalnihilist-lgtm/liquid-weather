package com.liquidweather.app;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;
import android.webkit.GeolocationPermissions;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

/**
 * Liquid Weather — a thin native shell around the self-contained HTML app.
 *
 * The whole UI (design, scenes, forecasts, search) lives in assets/index.html.
 * This activity only supplies what a browser page cannot do on its own inside
 * an APK: a WebView with JavaScript + storage, and the Android runtime location
 * permission that the page's navigator.geolocation call needs.
 */
public class MainActivity extends Activity {

    private static final String BASE_URL = "https://liquidweather.app/";
    private static final int REQ_LOCATION = 1001;

    private WebView web;
    /* Every prompt the page has open, not just the newest one. Two
       getCurrentPosition() calls can be in flight at once — the silent locate()
       the page runs at boot, and a tap on "Use my current location" while that
       prompt is still up — and each reaches this activity as its own
       onGeolocationPermissionsShowPrompt(). A single stored callback pair kept
       only the later request: the earlier callback was overwritten and never
       invoked, so the WebView never answered that getCurrentPosition(), and the
       page sat on its own watchdog (15s, or 35s while a prompt is pending)
       before giving up — toasting "Could not reach your location" and turning
       the pinned row into a saved New Delhi while a fix was available. The
       callbacks are kept in arrival order and every one of them gets the same
       answer. */
    private final List<GeolocationPermissions.Callback> geoCallbacks = new ArrayList<>();
    private final List<String> geoOrigins = new ArrayList<>();
    /* One system permission request at a time. requestPermissions() issued
       while another is still being answered is dropped by the platform (its
       result never arrives), so a second prompt joins the list above and waits
       for the answer to the request that is already out. */
    private boolean geoAsking = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        web = new WebView(this);
        web.setLayoutParams(new ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        web.setBackgroundColor(0xFF0A0B14);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        web.setFitsSystemWindows(true);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setGeolocationEnabled(true);
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(false);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        s.setTextZoom(100);

        web.setWebViewClient(new WebViewClient());

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onGeolocationPermissionsShowPrompt(String origin,
                                                           GeolocationPermissions.Callback callback) {
                if (hasLocationPermission()) {
                    // Already granted: allow, and let the page cache the position.
                    callback.invoke(origin, true, true);
                    return;
                }
                geoCallbacks.add(callback);
                geoOrigins.add(origin);
                if (!geoAsking) {
                    geoAsking = true;
                    requestPermissions(new String[]{
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                    }, REQ_LOCATION);
                }
            }
        });

        setContentView(web);
        // Serving the page from an https origin keeps it a secure context, which
        // geolocation and localStorage both require.
        web.loadDataWithBaseURL(BASE_URL, readAsset("index.html"), "text/html", "UTF-8", null);
    }

    private boolean hasLocationPermission() {
        return checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
                || checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED;
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] results) {
        super.onRequestPermissionsResult(requestCode, permissions, results);
        if (requestCode != REQ_LOCATION) return;
        /* Any granted result counts. `results[0]` alone is the FINE_LOCATION
           answer, so on Android 12+ a user who picks "Approximate location"
           (COARSE granted, FINE denied) was reported to the page as a refusal:
           the app announced that location was blocked and dropped to New Delhi
           even though a coarse fix was available. */
        boolean granted = false;
        for (int r : results) {
            if (r == PackageManager.PERMISSION_GRANTED) granted = true;
        }
        if (!granted) granted = hasLocationPermission();
        // Even when denied we hand control back to the page: it falls back to
        // a default city and the user can pick one from the search sheet.
        answerGeo(granted);
    }

    /* Answers every prompt that is still waiting, oldest first, and forgets
       them. A callback that was never invoked leaves the page's
       getCurrentPosition() unanswered for good, so this is the only exit for a
       prompt — granted, denied, or the activity going away. */
    private void answerGeo(boolean granted) {
        geoAsking = false;
        for (int i = 0; i < geoCallbacks.size(); i++) {
            GeolocationPermissions.Callback callback = geoCallbacks.get(i);
            if (callback != null) callback.invoke(geoOrigins.get(i), granted, false);
        }
        geoCallbacks.clear();
        geoOrigins.clear();
    }

    private String readAsset(String name) {
        try (InputStream in = getAssets().open(name)) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[8192];
            int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
            return out.toString("UTF-8");
        } catch (Exception e) {
            return "<html><body style='background:#0a0b14;color:#fff;font-family:sans-serif;padding:24px'>"
                    + "Could not load the app assets.<br><small>" + e + "</small></body></html>";
        }
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) web.goBack();
        else super.onBackPressed();
    }

    /* The activity never told the WebView it had gone away, so everything the
       page keeps running kept running: the 60-second forecast re-check, the
       layout and parsing work, and the compositor animations (drifting clouds,
       the pulsing sun, the shimmer on a loading card) carried on for as long as
       the activity was stopped instead of on screen. WebView.onPause() and
       onResume() are the documented pair for that, and they are the only signal
       the page gets: with them the renderer idles in the background and picks
       straight up where it was on return. Nothing on screen changes — the
       activity is invisible while paused, and onResume() restores the timers
       and the page's own visibility handling runs exactly as before. */
    @Override
    protected void onPause() {
        if (web != null) web.onPause();
        super.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) web.onResume();
    }

    @Override
    protected void onDestroy() {
        if (web != null) {
            /* A location prompt that was still up when the activity went away
               leaves its callback stored here and the page's geolocation call
               unanswered: the callback (and through it the WebView) is held
               until the activity is collected. Hand back a refusal — the same
               answer a denied prompt gives — to every prompt still waiting,
               not just the newest one, and drop them. */
            answerGeo(false);
            /* destroy() is only safe once the WebView is out of the view tree:
               called while it is still attached, the compositor and the native
               AwContents stay tied to a window that is being torn down, and the
               platform logs 'WebView.destroy() called while still attached'.
               Detach first, stop the load that was in flight, then destroy. */
            ViewParent parent = web.getParent();
            if (parent instanceof ViewGroup) ((ViewGroup) parent).removeView(web);
            web.stopLoading();
            web.destroy();
            web = null;
        }
        super.onDestroy();
    }
}
