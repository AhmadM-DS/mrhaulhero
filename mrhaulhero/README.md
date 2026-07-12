# Mr Haul Hero — Website

Static website for Mr Haul Hero Junk Removal (Dallas–Fort Worth). Built with plain HTML, CSS, and JavaScript — no build tools or server required. Ready to host on GitHub Pages.

## Structure

```
mrhaulhero/
├── index.html              Home
├── services/               Services page
├── pricing/                Pricing page
├── about/                  About page
├── contact/                Contact page
├── service-area/           Service Area overview + 16 city pages
│   ├── index.html
│   ├── dallas/  fort-worth/  arlington/  plano/  frisco/ ...
├── assets/
│   ├── css/styles.css      All site styles
│   ├── js/main.js          Nav dropdown/accordion, FAQ, form helpers
│   └── images/logo.png     Company logo
├── .nojekyll               Tells GitHub Pages to serve assets as-is
└── README.md
```

Clean URLs (e.g. `/service-area/frisco/`) work because each page is an `index.html` inside its own folder.

## Before you go live — 3 things to update

1. **Booking form (IMPORTANT).** Both booking forms currently point to a placeholder Formspree endpoint. Search the project for `YOUR_FORM_ID` (in `index.html` and `contact/index.html`) and replace `https://formspree.io/f/YOUR_FORM_ID` with your real Formspree endpoint.
   - Sign up free at https://formspree.io, create a form, and paste your endpoint URL. Submissions (including photo uploads) will be emailed to you.

2. **Social links.** In `assets/... ` the footer social icons (Facebook, Instagram, TikTok) currently link to `#`. Once you have your handles, update the `href="#"` values in the footer of each page. (Tip: edit `build_site.py`'s `footer()` function and re-run it — see below — so all pages update at once.)

3. **Logo.** `assets/images/logo.png` is your provided logo. Swap it if you get a higher-res or transparent version (keep the same filename).

## Editing content the easy way (optional)

All pages are generated from `build_site.py` (included in the parent folder of this download, or ask for it). Editing the script and re-running `python3 build_site.py` regenerates every page consistently — the best way to change shared parts like the header, footer, phone number, or pricing. If you'd rather hand-edit, just open the individual `.html` files.

## Deploy to GitHub Pages

```bash
cd mrhaulhero
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Then in your GitHub repo: **Settings → Pages → Source: Deploy from a branch → main / (root) → Save.**

Your site will publish at `https://YOUR_USERNAME.github.io/YOUR_REPO/`. To use **mrhaulhero.com**, add a `CNAME` file containing `www.mrhaulhero.com` and point your domain's DNS to GitHub Pages (Settings → Pages → Custom domain walks you through it).

## Business details baked into the site

- Phone: 214-517-2955 (click-to-call and text links)
- Email: kareem@mrhaulhero.com
- Hours: 8am–8pm, 7 days a week
- Licensed & insured
- 15% off first-time customers
- Pricing by truckload + per-item table
- 16 service-area city pages with individual maps

---
© Mr Haul Hero. All rights reserved.
