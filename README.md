# Hines Keep website

The studio website for Hines Keep (Austin Hines), published by GitHub Pages from `main` at https://hineskeep.com.

| Path | Page |
|---|---|
| `/` | Studio home with the Tide Trail card |
| `/tidetrail/` | Tide Trail game page |
| `/tidetrail/privacy/` | Privacy policy, true for the current pre-release build. Update it before ads, analytics, purchases or reminders ship |
| `/tidetrail/support/` | Support and FAQ |
| `/app-ads.txt` | Placeholder (comments only) until the ad network is picked |

No cookies, analytics, ads or third-party scripts. Fonts are self-hosted (Fredoka, SIL OFL).

## Images
`_tools/build_assets.py` rebuilds `assets/`, the favicons and the Open Graph images from a GameStudio clone:

    py -3 _tools/build_assets.py --studio C:/dev/GameStudio

Never publish anything from `_ArtDevelopment/References/`, any `*gate_board*` image or concepts marked internal. Add the App Store badge only once the app is live.
