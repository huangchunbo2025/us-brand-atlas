# US Brand Atlas

An interactive, offline-ready map featuring **261 brands** across the **48 contiguous U.S. states**. Click a brand to explore its founding or origin year, historical roots, industry, profile, and website.

**Live website: https://us-brand-atlas.onrender.com**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/huangchunbo2025/us-brand-atlas)

## Features

- An English interface and English profiles for all 261 brands.
- A draggable, zoomable map with clickable brands and state collections.
- Search by brand name or keywords, with exact-name matches ranked first.
- Combined state and industry filters, plus map and directory views.
- A desktop profile sidebar and mobile detail sheet, with keyboard navigation.
- A single HTML file without runtime dependencies or external font, script, or image requests.

Chinese brand names remain available as search aliases; displayed profiles are in English.

## Open locally

Download and open [`public/index.html`](public/index.html). No dependency installation, server, or API key is needed.

For local HTTP access, run this from the repository root:

```sh
python3 -m http.server 8000 --directory public
```

Then visit `http://localhost:8000`.

## Deploy on Render

This project uses a Render **Static Site**, without a paid Web Service, database, or background process. Free allowances and overage rules are subject to [Render's pricing](https://render.com/pricing).

Click **Deploy to Render** above, sign in, and create the site from the included `render.yaml` Blueprint.

| Setting | Value |
| --- | --- |
| Service type | Static Site |
| Repository | `https://github.com/huangchunbo2025/us-brand-atlas` |
| Branch | `main` |
| Build Command | Leave blank; publish the committed HTML |
| Publish Directory | `public` |
| Automatic deployments | On commits to `main` |

Render supplies an HTTPS `*.onrender.com` address. No environment variables are required.

## Edit and rebuild

Both source files and generated HTML are committed to the repository.

```text
data/brands.txt       Original reference data and Chinese search aliases
data/brands.en.txt    English origin and description for each brand
data/us-map.json      Pre-projected US Atlas state boundaries
src/template.html    English interface, styles, and interaction logic
tools/build.py       Generator using only the Python standard library
public/index.html    Standalone output and Render publish directory
tests/check.cjs      DOM-level interaction and English content checks
render.yaml          Render Static Site Blueprint
```

The original dataset has eight pipe-separated fields:

```text
name|Chinese alias|state code|origin year|historical roots|industry|description|website domain or reference path
```

The English dataset is keyed by the original brand name, with three pipe-separated fields:

```text
name|English historical roots|English description
```

The build requires an English profile for every entry and maps industries to English labels. To update the site, edit the source files, regenerate the HTML, and commit the output:

```sh
python3 tools/build.py
git add data src tools public
git commit -m "Update brand atlas"
git push
```

The build works offline. When updating historical information, check official sources and distinguish founding dates from brand launches, incorporations, and mergers.

## Validation

Development checks require Node.js 22+. The published website does not require Node.js.

```sh
npm ci
npm test
```

Checks cover all English profiles and state lists, accessibility labels, links, search and Chinese aliases, empty results, combined filters, zoom limits, previous/next navigation, the information dialog, and the mobile detail sheet.

Tests use LinkeDOM to check DOM and event logic. They do **not** replace visual or compatibility testing in a real browser.

## Methodology and sources

- Inspired by the supplied “United States of Brands” image, credited to International Relations Illustrated. The original image is not included in this repository.
- The collection includes identifiable brands from the reference and additional entries. It is not a complete reproduction of every mark in the image.
- Map positions indicate historical or headquarters connections, not consistently founding locations or current headquarters. Profiles separately explain historical roots. Some associations follow the reference image.
- Profiles summarize public historical information. Website links support further verification; business status and other information may not be current. Source-backed corrections are welcome.
- State boundaries come from [US Atlas](https://github.com/topojson/us-atlas), based on U.S. Census Bureau data. The ISC license is retained in [`licenses/us-atlas-ISC.txt`](licenses/us-atlas-ISC.txt) and the generated HTML.

## License

Project code and project-authored documentation use the [MIT License](LICENSE). Third-party map data retains its ISC license.

Brand names are used for identification and explanation, not as official logo artwork. Names, trademarks, and other third-party rights belong to their respective owners. The MIT license does not grant those rights, and inclusion does not imply endorsement or authorization.
