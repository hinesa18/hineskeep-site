# Hines Keep website

The studio website for Hines Keep (Austin Hines), published by GitHub Pages from `main` at https://hineskeep.com.

| Path | Page |
|---|---|
| `/` | Studio home with the Tide Trail card |
| `/tidetrail/` | Tide Trail game page |
| `/tidetrail/privacy/` | Privacy policy for 1.0: the save file, Unity LevelPlay (ironSource Ads), Firebase Analytics and Remote Config, Apple purchases, the tracking question, the daily reminder. Update it before a service is added |
| `/tidetrail/support/` | Support and FAQ |
| `/tidetrail/press/` | Press kit: the facts, what's in at launch, six real screenshots (full size in `assets/press/`), the icon and logo, the contact. Built by `_tools/build_assets.py --only press`; a slot for the public TestFlight link |
| `/app-ads.txt` | Authorized ad sellers: `OWNERDOMAIN`, the ironSource Ads line (needs the LevelPlay publisher ID) and ironSource's reseller list from Unity's docs |

No cookies, analytics, ads or third-party scripts. Fonts are self-hosted (Fredoka, SIL OFL).

## Images
`_tools/build_assets.py` rebuilds `assets/`, the favicons and the Open Graph images from a GameStudio clone:

    py -3 _tools/build_assets.py --studio C:/dev/GameStudio
    python3 _tools/build_assets.py --studio ~/Developer/GameStudio-web-store --only icon,og   # on the Mac; --only skips the font step (needs fonttools)

Never publish anything from `_ArtDevelopment/References/`, any `*gate_board*` image or concepts marked internal. Add the App Store badge only once the app is live.
