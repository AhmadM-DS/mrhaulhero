#!/usr/bin/env python3
"""Build script for Mr Haul Hero site.
Generates all HTML pages from shared components so header/footer/nav stay consistent.
Output goes into /home/claude/mrhaulhero/
"""
import os

ROOT = "/home/claude/mrhaulhero"

PHONE = "214-517-2955"
PHONE_HREF = "tel:+12145172955"
SMS_HREF = "sms:+12145172955"
EMAIL = "kareem@mrhaulhero.com"
FORMSPREE = "https://formspree.io/f/YOUR_FORM_ID"  # <-- SWAP THIS for your real Formspree endpoint

# 16 cities: (slug, "Display Name, TX", intro paragraph, [nearby city names])
CITIES = [
    ("dallas", "Dallas, TX",
     "Mr Haul Hero provides fast, reliable junk removal throughout Dallas \u2014 from downtown high-rises to homes in Oak Cliff, Lakewood, and beyond. Whether it's a single couch or a full estate cleanout, our licensed and insured crew handles the heavy lifting so you don't have to.",
     ["Irving", "Richardson", "Grand Prairie", "Mesquite", "Garland"]),
    ("fort-worth", "Fort Worth, TX",
     "From the Stockyards to Sundance Square and every neighborhood in between, Mr Haul Hero keeps Fort Worth clear of clutter. We remove furniture, appliances, yard debris, and construction waste with same-day service seven days a week.",
     ["Arlington", "Grand Prairie", "Mansfield", "Southlake", "Roanoke"]),
    ("arlington", "Arlington, TX",
     "Mr Haul Hero serves all of Arlington with dependable, upfront-priced junk removal. Homeowners, renters, and businesses near the entertainment district and beyond count on us to haul away whatever they no longer need.",
     ["Fort Worth", "Grand Prairie", "Mansfield", "Irving", "Dallas"]),
    ("plano", "Plano, TX",
     "Serving Plano's neighborhoods and businesses, Mr Haul Hero makes decluttering effortless. From garage cleanouts to appliance removal, our crew arrives on time and leaves your space spotless.",
     ["Frisco", "McKinney", "Richardson", "Carrollton", "Allen"]),
    ("frisco", "Frisco, TX",
     "Mr Haul Hero brings same-day junk removal to Frisco homes and businesses \u2014 from single items to full property cleanouts. Growing fast means clearing out the old, and we're here to make that simple.",
     ["Plano", "McKinney", "Little Elm", "Prosper", "Allen"]),
    ("irving", "Irving, TX",
     "Centrally located Irving trusts Mr Haul Hero for quick, courteous junk removal. Near Las Colinas or anywhere in the city, we handle furniture, appliances, and debris with care and fair pricing.",
     ["Dallas", "Grand Prairie", "Carrollton", "Arlington", "Coppell"]),
    ("mckinney", "McKinney, TX",
     "Mr Haul Hero helps McKinney residents reclaim their space with hassle-free junk removal. Historic downtown or new developments \u2014 we recycle and donate as much as we can along the way.",
     ["Frisco", "Plano", "Allen", "Prosper", "Melissa"]),
    ("carrollton", "Carrollton, TX",
     "From Old Downtown Carrollton to the neighborhoods along the DART line, Mr Haul Hero clears junk quickly and responsibly. One item or a whole house \u2014 we've got the truck and the crew.",
     ["Irving", "Plano", "Lewisville", "Richardson", "Farmers Branch"]),
    ("richardson", "Richardson, TX",
     "Mr Haul Hero serves Richardson with prompt, professional junk removal. We handle everything from office cleanouts in the Telecom Corridor to household furniture and appliances.",
     ["Plano", "Dallas", "Carrollton", "Garland", "Allen"]),
    ("denton", "Denton, TX",
     "Up north in Denton, Mr Haul Hero delivers reliable junk removal for students, families, and businesses alike. We haul away furniture, appliances, and yard debris with same-day availability.",
     ["Roanoke", "Lewisville", "Trophy Club", "Corinth", "Argyle"]),
    ("lewisville", "Lewisville, TX",
     "Mr Haul Hero keeps Lewisville clutter-free with dependable, upfront-priced junk removal. From lakeside homes to busy retail spaces, our crew handles it all.",
     ["Carrollton", "Denton", "Trophy Club", "Flower Mound", "Coppell"]),
    ("grand-prairie", "Grand Prairie, TX",
     "Between Dallas and Fort Worth, Grand Prairie counts on Mr Haul Hero for fast junk removal. Furniture, appliances, construction debris \u2014 we clear it and clean up after.",
     ["Arlington", "Irving", "Fort Worth", "Mansfield", "Dallas"]),
    ("mansfield", "Mansfield, TX",
     "Mr Haul Hero serves Mansfield families and businesses with courteous, on-time junk removal. We donate and recycle whenever possible so less ends up in the landfill.",
     ["Arlington", "Grand Prairie", "Fort Worth", "Kennedale", "Midlothian"]),
    ("southlake", "Southlake, TX",
     "In Southlake, Mr Haul Hero offers premium, white-glove junk removal. From Town Square businesses to spacious homes, we handle every job with professionalism and care.",
     ["Trophy Club", "Roanoke", "Fort Worth", "Grapevine", "Keller"]),
    ("trophy-club", "Trophy Club, TX",
     "Mr Haul Hero provides friendly, reliable junk removal throughout Trophy Club. Whether you're renovating or just decluttering, our crew makes it easy.",
     ["Southlake", "Roanoke", "Denton", "Keller", "Westlake"]),
    ("roanoke", "Roanoke, TX",
     "Known as the Unique Dining Capital of Texas, Roanoke trusts Mr Haul Hero to keep homes and businesses clear. Same-day service, fair pricing, and a crew that cleans up after itself.",
     ["Trophy Club", "Southlake", "Denton", "Fort Worth", "Westlake"]),
]

# Order used in nav dropdown + service-area grid
CITY_ORDER = [c[0] for c in CITIES]
CITY_MAP = {c[0]: c for c in CITIES}


def head(title, description, css_prefix, canonical):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://www.mrhaulhero.com{canonical}">
  <link rel="icon" type="image/png" href="{css_prefix}assets/images/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.7.0/dist/tabler-icons.min.css">
  <link rel="stylesheet" href="{css_prefix}assets/css/styles.css">
</head>
<body>
"""


def nav(prefix, active):
    """prefix = relative path to site root e.g. '' or '../' or '../../'"""
    def cls(name):
        return ' class="active"' if active == name else ''
    # dropdown city links
    city_links = ""
    for slug in CITY_ORDER:
        name = CITY_MAP[slug][1].replace(", TX", "")
        city_links += f'<a href="{prefix}service-area/{slug}/"><i class="ti ti-map-pin-filled"></i>{name}</a>\n'
    sa_active = ' expanded-active' if active == 'service-area' else ''
    return f"""<header class="site-header">
  <nav class="nav" aria-label="Main navigation">
    <a class="brand" href="{prefix}index.html">
      <img src="{prefix}assets/images/logo.png" alt="Mr Haul Hero logo">
      <span>MR HAUL HERO</span>
    </a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false"><i class="ti ti-menu-2"></i></button>
    <div class="nav-links">
      <a href="{prefix}services/"{cls('services')}>Services</a>
      <a href="{prefix}pricing/"{cls('pricing')}>Pricing</a>
      <div class="nav-item">
        <a href="{prefix}service-area/"{' class="active"' if active=='service-area' else ''} aria-haspopup="true" aria-expanded="false">Service area <i class="ti ti-chevron-down dropdown-caret"></i></a>
        <div class="dropdown">
          <div class="dropdown-grid">
            {city_links}
          </div>
          <div class="dropdown-footer"><a href="{prefix}service-area/">View all service areas &rarr;</a></div>
        </div>
      </div>
      <a href="{prefix}about/"{cls('about')}>About</a>
      <a href="{prefix}contact/"{cls('contact')}>Contact</a>
      <a class="nav-phone" href="{PHONE_HREF}"><i class="ti ti-phone"></i>{PHONE}</a>
      <a class="btn btn-primary btn-sm" href="{prefix}#book" style="color:#fff;">Get a quote</a>
    </div>
  </nav>
</header>
"""


def footer(prefix):
    # short service-area summary links
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <img src="{prefix}assets/images/logo.png" alt="Mr Haul Hero logo">
          <span>MR HAUL HERO</span>
        </div>
        <p class="footer-about">DFW's junk removal hero. Licensed, insured, and always ready to haul \u2014 8am\u20138pm, 7 days a week.</p>
        <div class="footer-social">
          <a href="#" aria-label="Facebook"><i class="ti ti-brand-facebook"></i></a>
          <a href="#" aria-label="Instagram"><i class="ti ti-brand-instagram"></i></a>
          <a href="#" aria-label="TikTok"><i class="ti ti-brand-tiktok"></i></a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Quick links</h4>
        <a href="{prefix}services/">Services</a>
        <a href="{prefix}pricing/">Pricing</a>
        <a href="{prefix}service-area/">Service area</a>
        <a href="{prefix}about/">About</a>
        <a href="{prefix}contact/">Contact</a>
      </div>
      <div class="footer-col">
        <h4>Service area</h4>
        <a href="{prefix}service-area/dallas/">Dallas / Fort Worth</a>
        <a href="{prefix}service-area/plano/">Plano / Frisco</a>
        <a href="{prefix}service-area/mckinney/">McKinney / Allen area</a>
        <a href="{prefix}service-area/denton/">Denton / Southlake</a>
        <a href="{prefix}service-area/">+ all cities</a>
      </div>
      <div class="footer-col footer-contact">
        <h4>Contact</h4>
        <div class="line"><i class="ti ti-phone"></i><a href="{PHONE_HREF}">{PHONE}</a></div>
        <div class="line"><i class="ti ti-mail"></i><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="line"><i class="ti ti-clock"></i>Open 8am\u20138pm, 7 days</div>
        <div class="line"><i class="ti ti-shield-check"></i>Licensed &amp; insured</div>
      </div>
    </div>
    <div class="footer-bottom">&copy; <span id="year">2026</span> Mr Haul Hero. All rights reserved.</div>
  </div>
</footer>
<script src="{prefix}assets/js/main.js"></script>
</body>
</html>
"""


def truck_svg():
    return """<svg width="340" height="240" viewBox="0 0 340 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pickup truck loaded with junk">
  <ellipse cx="170" cy="205" rx="150" ry="10" fill="#D2D6DB"/>
  <rect x="20" y="130" width="150" height="60" fill="#132247"/>
  <rect x="20" y="130" width="150" height="10" fill="#1C2E5A"/>
  <rect x="20" y="130" width="150" height="60" fill="none" stroke="#6E7890" stroke-width="1.5"/>
  <polygon points="170,120 200,120 232,148 232,190 170,190" fill="#0A1B3D" stroke="#6E7890" stroke-width="1.5"/>
  <polygon points="176,128 198,128 218,148 176,148" fill="#9AA4B5"/>
  <rect x="176" y="128" width="22" height="20" fill="#C7CCD4" opacity="0.7"/>
  <rect x="150" y="176" width="16" height="8" fill="#C7CCD4"/>
  <circle cx="58" cy="192" r="22" fill="#1C2331"/><circle cx="58" cy="192" r="22" fill="none" stroke="#0A1B3D" stroke-width="3"/><circle cx="58" cy="192" r="9" fill="#B7BEC8"/>
  <circle cx="200" cy="192" r="22" fill="#1C2331"/><circle cx="200" cy="192" r="22" fill="none" stroke="#0A1B3D" stroke-width="3"/><circle cx="200" cy="192" r="9" fill="#B7BEC8"/>
  <rect x="32" y="140" width="34" height="22" fill="none" stroke="#6E7890" stroke-width="1"/>
  <text x="49" y="155" text-anchor="middle" font-family="Poppins, sans-serif" font-weight="700" font-size="11" fill="#C7CCD4">HH</text>
  <rect x="30" y="82" width="30" height="48" fill="#7C8698"/><rect x="30" y="82" width="30" height="48" fill="none" stroke="#5C6577" stroke-width="1"/>
  <line x1="30" y1="94" x2="60" y2="94" stroke="#5C6577" stroke-width="1"/><line x1="30" y1="106" x2="60" y2="106" stroke="#5C6577" stroke-width="1"/><line x1="30" y1="118" x2="60" y2="118" stroke="#5C6577" stroke-width="1"/>
  <rect x="64" y="70" width="34" height="60" fill="#C9642F"/><rect x="64" y="70" width="34" height="60" fill="none" stroke="#9A4A21" stroke-width="1"/><rect x="70" y="78" width="22" height="10" fill="#A8521F"/>
  <rect x="102" y="88" width="26" height="42" fill="#95A0AE"/><circle cx="115" cy="100" r="6" fill="#7C8698"/>
  <polygon points="130,130 150,92 172,130" fill="#8B5A2B" stroke="#6B4420" stroke-width="1"/>
  <rect x="176" y="98" width="24" height="32" fill="#B7BEC8"/><rect x="176" y="98" width="24" height="32" fill="none" stroke="#8B93A6" stroke-width="1"/><rect x="176" y="108" width="24" height="4" fill="#8B93A6"/><rect x="176" y="118" width="24" height="4" fill="#8B93A6"/>
  <rect x="20" y="128" width="150" height="4" fill="#6E7890"/>
</svg>"""


# Service icon SVGs (navy on silver)
SVC_ICONS = {
    "junk": '<svg width="88" height="88" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><ellipse cx="50" cy="88" rx="36" ry="5" fill="#0A1B3D" opacity="0.15"/><path d="M26 44 L74 44 L69 88 L31 88 Z" fill="#0A1B3D"/><path d="M35 44 L38 88 M50 44 L50 88 M65 44 L62 88" stroke="#3C5A8C" stroke-width="2"/><path d="M19 34 L81 34 L74 44 L26 44 Z" fill="#132A55"/><rect x="41" y="15" width="18" height="19" rx="1" fill="#132A55"/><rect x="44" y="18" width="12" height="4" fill="#3C5A8C"/><circle cx="50" cy="10" r="4" fill="#0A1B3D"/><path d="M60 55 l6 6 M60 61 l6 -6" stroke="#5C7AB0" stroke-width="2" stroke-linecap="round"/><circle cx="42" cy="70" r="3" fill="#5C7AB0"/></svg>',
    "garage": '<svg width="88" height="88" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><ellipse cx="50" cy="90" rx="42" ry="4" fill="#0A1B3D" opacity="0.12"/><polygon points="10,42 50,10 90,42 90,50 50,20 10,50" fill="#0A1B3D"/><rect x="20" y="48" width="60" height="42" fill="#0A1B3D"/><line x1="20" y1="57" x2="80" y2="57" stroke="#3C5A8C" stroke-width="1.5"/><line x1="20" y1="66" x2="80" y2="66" stroke="#3C5A8C" stroke-width="1.5"/><line x1="20" y1="75" x2="80" y2="75" stroke="#3C5A8C" stroke-width="1.5"/><line x1="20" y1="84" x2="80" y2="84" stroke="#3C5A8C" stroke-width="1.5"/><line x1="34" y1="48" x2="34" y2="90" stroke="#132A55" stroke-width="1"/><line x1="66" y1="48" x2="66" y2="90" stroke="#132A55" stroke-width="1"/></svg>',
    "furniture": '<svg width="88" height="88" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><ellipse cx="50" cy="88" rx="42" ry="5" fill="#0A1B3D" opacity="0.12"/><path d="M16 62 Q16 46 32 46 L68 46 Q84 46 84 62 L84 70 L16 70 Z" fill="#0A1B3D"/><path d="M20 48 Q20 40 30 40 L38 40 Q44 40 44 48 L44 58 L20 58 Z" fill="#132A55"/><path d="M56 48 Q56 40 62 40 L70 40 Q80 40 80 48 L80 58 L56 58 Z" fill="#132A55"/><rect x="16" y="70" width="68" height="10" fill="#132A55"/><rect x="12" y="76" width="9" height="16" fill="#0A1B3D"/><rect x="79" y="76" width="9" height="16" fill="#0A1B3D"/></svg>',
    "yard": '<svg width="88" height="88" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><ellipse cx="50" cy="90" rx="30" ry="4" fill="#0A1B3D" opacity="0.12"/><path d="M50 14 C34 26 28 40 36 50 C26 52 20 63 28 73 C36 82 52 82 55 70 C63 79 78 74 76 62 C84 57 82 44 72 41 C77 30 66 18 50 14 Z" fill="#0A1B3D"/><path d="M50 20 C48 34 48 50 51 66" stroke="#3C5A8C" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M51 38 C58 42 63 47 63 54" stroke="#3C5A8C" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M48 55 C41 58 36 63 37 70" stroke="#3C5A8C" stroke-width="2.5" fill="none" stroke-linecap="round"/><rect x="46" y="80" width="8" height="12" fill="#132A55"/></svg>',
    "appliance": '<svg width="88" height="88" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><ellipse cx="50" cy="90" rx="24" ry="4" fill="#0A1B3D" opacity="0.12"/><rect x="32" y="10" width="36" height="78" rx="2" fill="#0A1B3D"/><rect x="32" y="10" width="36" height="24" fill="#132A55"/><line x1="32" y1="34" x2="68" y2="34" stroke="#3C5A8C" stroke-width="1.5"/><rect x="37" y="16" width="4" height="12" rx="1.5" fill="#5C7AB0"/><rect x="37" y="40" width="4" height="14" rx="1.5" fill="#5C7AB0"/><line x1="32" y1="70" x2="68" y2="70" stroke="#132A55" stroke-width="1"/></svg>',
    "construction": '<svg width="88" height="88" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><ellipse cx="50" cy="90" rx="38" ry="4" fill="#0A1B3D" opacity="0.12"/><rect x="15" y="58" width="70" height="30" fill="#0A1B3D"/><line x1="15" y1="68" x2="85" y2="68" stroke="#3C5A8C" stroke-width="1.2"/><line x1="15" y1="78" x2="85" y2="78" stroke="#3C5A8C" stroke-width="1.2"/><line x1="32" y1="58" x2="32" y2="88" stroke="#3C5A8C" stroke-width="1.2"/><line x1="50" y1="58" x2="50" y2="88" stroke="#3C5A8C" stroke-width="1.2"/><line x1="68" y1="58" x2="68" y2="88" stroke="#3C5A8C" stroke-width="1.2"/><g transform="rotate(35 55 30)"><rect x="51" y="10" width="8" height="42" rx="2" fill="#132A55"/><rect x="44" y="6" width="22" height="14" rx="2" fill="#3C5A8C"/></g></svg>',
}

SERVICES = [
    ("junk", "General Junk Removal", "Old furniture, clutter, broken electronics \u2014 if it's junk, we'll haul it away same day.", "Starting at $89"),
    ("garage", "Garage Cleanout", "Reclaim your garage. We clear out years of stored junk, boxes, and tools in one visit.", "Starting at $299"),
    ("furniture", "Furniture Removal", "Couches, mattresses, dressers, tables \u2014 we lift, load, and haul the heavy stuff.", "Starting at $89"),
    ("yard", "Yard Debris Removal", "Branches, brush, old fencing, and yard waste cleared so your outdoor space looks its best.", "Get a free quote"),
    ("appliance", "Appliance Removal", "Fridges, washers, dryers, and more \u2014 safely removed and responsibly recycled.", "Starting at $89"),
    ("construction", "Construction Debris Removal", "Drywall, wood, tile, and renovation waste hauled off so your job site stays clear.", "Get a free quote"),
]

TIERS = [
    ("Single item<br>(minimum)", "$89+", False),
    ("1/8 truck", "$100&ndash;175", False),
    ("1/4 truck", "$175&ndash;275", False),
    ("1/2 truck", "$300&ndash;450", False),
    ("3/4 truck", "$450&ndash;600", False),
    ("Full truck", "$700&ndash;850+", True),
]

ITEMS = [
    ("Mattress / Box Spring", "$89+"), ("Sofa / Couch", "$99+"), ("Refrigerator", "$109+"),
    ("Washer or Dryer", "$89+"), ("Dining Table", "$89+"), ("Exercise Equipment", "$99+"),
    ("Pool Table", "$89+"), ("Hot Tub", "$450+"), ("Shed Removal", "$500+"),
    ("Garage Cleanout", "Starting at $299"), ("Storage Unit Cleanout", "Starting at $199"),
    ("Estate Cleanout", "Free Estimate"), ("Office Cleanout", "Free Estimate"),
]

FAQS = [
    ("What items do you take?",
     "We haul almost anything non-hazardous: furniture, mattresses, appliances, electronics, yard debris, construction waste, and full cleanouts. We can't take hazardous materials like paint, chemicals, or asbestos \u2014 just ask if you're unsure."),
    ("How does pricing work?",
     "Pricing is based on how much space your junk takes up in the truck and its weight. We provide a free on-site estimate before any work begins, so you always know the price upfront \u2014 no hidden fees."),
    ("Do you offer same-day service?",
     "Yes, in most cases. We operate 8am\u20138pm, 7 days a week across DFW. Call or text early and we'll do our best to get to you the same day."),
    ("Are you licensed and insured?",
     "Absolutely. Mr Haul Hero is fully licensed and insured, so your property and our crew are covered on every job."),
    ("What happens to the junk you remove?",
     "We donate and recycle as much as we possibly can. Usable items go to local charities and recyclable materials are sorted out, keeping as much as possible out of the landfill."),
]


def discount_banner():
    return """<div class="discount">
  <div class="tag">NEW CUSTOMER</div>
  <div class="pct">15%</div>
  <div>
    <div class="d-title">Off your first job, guaranteed</div>
    <div class="d-sub">Applied automatically for every first-time customer</div>
  </div>
</div>"""


def tier_grid():
    cells = ""
    for label, price, full in TIERS:
        c = " tier-full" if full else ""
        cells += f'<div class="tier{c}"><div class="t-label">{label}</div><div class="t-price">{price}</div></div>\n'
    return f'<div class="tier-grid">\n{cells}</div>'


def price_box(city=None):
    title = f"{city} Pricing Snapshot" if city else "Priced by Truckload"
    sub = "Priced by truckload &mdash; free on-site estimate before any work begins" if city else "Based on weight &amp; volume &mdash; the more room your junk takes up, the more it costs"
    note = "" if city else '<div class="price-note"><i class="ti ti-info-circle"></i>Heavier items (appliances, construction debris) may be priced closer to the top of each range.</div>'
    return f"""<div class="price-box">
  <div class="price-box-head">
    <div class="ico"><i class="ti ti-truck"></i></div>
    <div><h3>{title}</h3><p>{sub}</p></div>
  </div>
  <div class="price-box-body">
    {tier_grid()}
    {note}
  </div>
</div>"""


def booking_form(prefix_note=""):
    return f"""<form class="form-wrap" action="{FORMSPREE}" method="POST" enctype="multipart/form-data">
  <!-- SWAP the form action above for your real Formspree endpoint -->
  <div class="form-row">
    <div class="field"><label for="name">Full name</label><input type="text" id="name" name="name" placeholder="Jane Smith" required></div>
    <div class="field"><label for="phone">Phone number</label><input type="tel" id="phone" name="phone" placeholder="(214) 555-0123" required></div>
  </div>
  <div class="field full"><label for="email">Email</label><input type="email" id="email" name="email" placeholder="jane@email.com" required></div>
  <div class="field full"><label for="address">Address</label><input type="text" id="address" name="address" placeholder="123 Main St, Dallas, TX" required></div>
  <div class="form-row">
    <div class="field"><label for="date">Preferred date</label><input type="date" id="date" name="preferred_date"></div>
    <div class="field"><label for="time">Preferred time</label>
      <select id="time" name="preferred_time">
        <option value="">Select a time</option>
        <option>Morning (8am\u201312pm)</option>
        <option>Afternoon (12\u20134pm)</option>
        <option>Evening (4\u20138pm)</option>
      </select>
    </div>
  </div>
  <div class="field full">
    <label for="junk-photo">Photo of your junk (optional)</label>
    <label class="field-file" for="junk-photo"><i class="ti ti-camera-plus"></i> <span class="field-file-text">Tap to upload a photo</span></label>
    <input type="file" id="junk-photo" name="photo" accept="image/*" multiple hidden>
  </div>
  <button type="submit" class="btn btn-primary btn-block">Request my free quote</button>
  <p class="form-note">Prefer to talk? Call or text <a href="{PHONE_HREF}">{PHONE}</a> \u2014 we're here 8am\u20138pm, 7 days a week.</p>
</form>"""


def cta_band(headline, sub, btn="Book now", href="/#book"):
    return f"""<div class="cta-band">
  <div><h3>{headline}</h3><p>{sub}</p></div>
  <a class="btn btn-light" href="{href}">{btn}</a>
</div>"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


# ---------------- HOME ----------------
def build_home():
    svc_cards = ""
    for key, name, desc, price in SERVICES:
        svc_cards += f"""<a class="svc-card" href="services/">
      <div class="svc-art">{SVC_ICONS[key]}</div>
      <div class="svc-body"><h3>{name}</h3><p>{desc}</p><div class="price">{price} &rarr;</div></div>
    </a>\n"""

    features = [
        ("ti-shield-check", "Licensed &amp; insured", "Every job covered, every time. No surprises."),
        ("ti-clock", "Open 8am&ndash;8pm", "7 days a week. Junk doesn't wait, and neither do we."),
        ("ti-recycle", "Donate &amp; recycle first", "We give back and keep junk out of landfills whenever we can."),
        ("ti-tag", "Upfront pricing", "Free on-site estimates, no hidden fees."),
    ]
    feat_html = ""
    for ico, h, p in features:
        feat_html += f'<div class="feature"><div class="ico"><i class="ti {ico}"></i></div><h3>{h}</h3><p>{p}</p></div>\n'

    steps = [
        ("ti-phone", "Get a free quote", "Call, text, or book online. Tell us what needs to go."),
        ("ti-clipboard-check", "We confirm the price", "On-site estimate, upfront price. You approve before we start."),
        ("ti-truck", "We haul it away", "We load, clean up, and donate or recycle what we can."),
    ]
    steps_html = ""
    for ico, h, p in steps:
        steps_html += f'<div class="step"><div class="ico"><i class="ti {ico}"></i></div><h3>{h}</h3><p>{p}</p></div>\n'

    faq_html = ""
    for q, a in FAQS:
        faq_html += f'<div class="faq-item"><div class="faq-q">{q}<i class="ti ti-chevron-down"></i></div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>\n'

    city_cards = ""
    for slug in CITY_ORDER:
        name = CITY_MAP[slug][1].replace(", TX", "")
        city_cards += f'<a class="city-links-a" href="service-area/{slug}/"><i class="ti ti-map-pin-filled"></i>{name}</a>\n'

    city_link_html = ""
    for slug in CITY_ORDER:
        name = CITY_MAP[slug][1].replace(", TX", "")
        city_link_html += f'<a href="service-area/{slug}/"><i class="ti ti-map-pin-filled"></i>{name}</a>\n'

    html = head(
        "Mr Haul Hero | Junk Removal in Dallas–Fort Worth, TX",
        "Same-day junk removal across DFW. Licensed, insured, open 8am–8pm 7 days a week. Furniture, appliances, garage cleanouts & more. 15% off your first job.",
        "", "/"
    )
    html += nav("", "home")
    html += f"""
<section class="hero">
  <div class="container hero-grid">
    <div>
      <div class="badge-line">DFW's junk removal hero \u00b7 8am\u20138pm daily</div>
      <h1>No junk survives<br>a Haul Hero.</h1>
      <p class="hero-sub">Same-day junk removal across Dallas\u2013Fort Worth. Licensed, insured, and available 8am\u20138pm, 7 days a week \u2014 from a single item to a full property cleanout.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="#book" style="color:#fff;">Book now</a>
        <a class="btn btn-outline" href="{SMS_HREF}"><i class="ti ti-phone"></i>Call or text</a>
      </div>
      <div class="hero-trust">
        <div><i class="ti ti-shield-check"></i>Licensed &amp; insured</div>
        <div><i class="ti ti-clock"></i>8am\u20138pm, 7 days</div>
        <div><i class="ti ti-map-pin"></i>Locally owned</div>
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-art">{truck_svg()}</div>
      <div class="hero-tag"><div class="num">15%</div><div class="lbl">off your first job</div></div>
    </div>
  </div>
</section>

<section class="section section-bg">
  <div class="container">
    <div class="section-head"><div class="eyebrow">Why choose us</div><h2>DFW trusts its junk to a hero</h2></div>
    <div class="grid grid-4">{feat_html}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><div class="eyebrow">Our services</div><h2>Whatever the junk, we haul it</h2></div>
    <div class="grid grid-3">{svc_cards}</div>
  </div>
</section>

<section class="section section-bg">
  <div class="container">
    <div class="section-head"><div class="eyebrow">How it works</div><h2>Three steps to junk-free</h2></div>
    <div class="steps">{steps_html}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><div class="eyebrow">Pricing</div><h2>Simple, upfront pricing</h2><p>Priced by truckload &mdash; free on-site estimate before any work begins.</p></div>
    <div style="display:flex;justify-content:center;margin-bottom:32px;">{discount_banner()}</div>
    {price_box()}
    <div style="text-align:center;margin-top:28px;"><a class="btn btn-primary" href="pricing/" style="color:#fff;">See full pricing</a></div>
  </div>
</section>

<section class="section section-bg" id="book">
  <div class="container">
    <div class="section-head"><div class="eyebrow">Book now</div><h2>Get your free quote</h2><p>Fill out the form, or call/text {PHONE} \u2014 we're here 8am\u20138pm, 7 days a week.</p></div>
    {booking_form()}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><div class="eyebrow">Service area</div><h2>Proudly serving all of DFW</h2><p>No storefront, no problem \u2014 we come to you.</p></div>
    <div class="area-grid">
      <div class="area-map">
        <iframe class="map-embed" src="https://www.google.com/maps?q=Dallas-Fort+Worth,+TX&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of Dallas-Fort Worth service area"></iframe>
      </div>
      <div class="city-box">
        <h3>Cities we serve</h3>
        <div class="city-links">{city_link_html}</div>
        <p style="font-size:12px;color:#8B93A6;margin-top:12px;font-style:italic;">...and surrounding areas</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-bg">
  <div class="container">
    <div class="section-head"><div class="eyebrow">FAQ</div><h2>Common questions</h2></div>
    <div class="faq">{faq_html}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><div class="eyebrow">Reviews</div><h2>Our first customers are writing this section</h2></div>
    <div class="reviews-ph"><i class="ti ti-star"></i><p>Reviews coming soon. Be one of our first DFW customers and help us build our reputation \u2014 plus get 15% off.</p></div>
  </div>
</section>

<section class="section-sm">
  <div class="container">{cta_band("No junk survives a Haul Hero.", "Free estimate, no obligation \u2014 " + PHONE, "Book now", "#book")}</div>
</section>
"""
    html += footer("")
    write("index.html", html)


# ---------------- SERVICES ----------------
def build_services():
    cards = ""
    for key, name, desc, price in SERVICES:
        arrow = f"{price} &rarr;"
        cards += f"""<div class="svc-card">
      <div class="svc-art">{SVC_ICONS[key]}</div>
      <div class="svc-body"><h3>{name}</h3><p>{desc}</p><div class="price">{arrow}</div></div>
    </div>\n"""
    html = head(
        "Our Services | Junk Removal, Cleanouts & Debris Hauling | Mr Haul Hero",
        "Furniture removal, garage cleanouts, appliance removal, yard debris & construction debris hauling across DFW. Licensed, insured, same-day service.",
        "../", "/services/"
    )
    html += nav("../", "services")
    html += f"""
<section class="page-hero">
  <div class="container"><div class="eyebrow">Our services</div><h1>Whatever the junk, we haul it</h1><p>From a single couch to a full property cleanout \u2014 licensed, insured, and ready across DFW.</p></div>
</section>
<section class="section">
  <div class="container"><div class="grid grid-3">{cards}</div></div>
</section>
<section class="section-sm">
  <div class="container">{cta_band("Not sure what you need hauled?", "Send us a photo and we'll quote it \u2014 free, no obligation.", "Get a free quote", "../#book")}</div>
</section>
"""
    html += footer("../")
    write("services/index.html", html)


# ---------------- PRICING ----------------
def build_pricing():
    items = ""
    for name, price in ITEMS:
        items += f'<div class="item-row"><span>{name}</span><span class="i-price">{price}</span></div>\n'
    html = head(
        "Pricing | Upfront Junk Removal Rates | Mr Haul Hero",
        "Straightforward junk removal pricing by truckload. Single item from $89, full truck $700+. Free on-site estimates. 15% off your first job.",
        "../", "/pricing/"
    )
    html += nav("../", "pricing")
    html += f"""
<section class="page-hero">
  <div class="container">
    <div class="eyebrow">Pricing</div>
    <h1>Straightforward pricing, no surprises</h1>
    <p>Priced by how much space your junk takes up and its weight. Every job starts with a free on-site estimate \u2014 you approve the price before we lift a finger.</p>
    <div style="margin-top:24px;">{discount_banner()}</div>
  </div>
</section>

<section class="section">
  <div class="container">{price_box()}</div>
</section>

<section class="section-sm">
  <div class="container">
    <div class="section-head"><div class="eyebrow">By item or job type</div><h2>Common items &amp; jobs</h2></div>
    <div class="item-list">{items}</div>
    <p class="fine">Prices vary based on volume, weight, and access. Final price confirmed on-site before work begins.</p>
  </div>
</section>

<section class="section-sm">
  <div class="container">{cta_band("Get your free, no-obligation estimate", "Call, text, or book online \u2014 " + PHONE, "Book now", "../#book")}</div>
</section>
"""
    html += footer("../")
    write("pricing/index.html", html)


# ---------------- ABOUT ----------------
def build_about():
    values = [
        ("ti-heart-handshake", "Give back", "We donate usable items to local charities so your junk can help someone in need."),
        ("ti-recycle", "Recycle first", "We sort and recycle whatever we can, keeping as much as possible out of the landfill."),
        ("ti-shield-check", "Do it right", "Licensed, insured, and respectful of your property on every single job."),
    ]
    val_html = ""
    for ico, h, p in values:
        val_html += f'<div class="feature"><div class="ico"><i class="ti {ico}"></i></div><h3>{h}</h3><p>{p}</p></div>\n'
    html = head(
        "About Us | Locally Owned Junk Removal in DFW | Mr Haul Hero",
        "Mr Haul Hero is a locally owned, licensed and insured junk removal company serving Dallas–Fort Worth. We donate, recycle, and give back on every job.",
        "../", "/about/"
    )
    html += nav("../", "about")
    html += f"""
<section class="page-hero">
  <div class="container"><div class="eyebrow">About us</div><h1>Your neighbors with a truck and a mission</h1><p>Mr Haul Hero is a locally owned junk removal company built on hard work, fair pricing, and giving back to the DFW community.</p></div>
</section>

<section class="section">
  <div class="container" style="max-width:760px;">
    <p style="font-size:16px;line-height:1.8;color:#3C4658;margin-bottom:20px;">We started Mr Haul Hero with a simple idea: junk removal should be easy, honest, and actually helpful. No vague pricing, no no-shows, no junk left behind \u2014 just a friendly crew that shows up, does the heavy lifting, and leaves your space clean.</p>
    <p style="font-size:16px;line-height:1.8;color:#3C4658;">Every load we haul is a chance to do some good. We donate what we can to local charities, recycle everything possible, and give back to the community we're proud to call home. When you book Mr Haul Hero, you're not just clearing clutter \u2014 you're keeping usable items in the hands of people who need them and out of the landfill.</p>
  </div>
</section>

<section class="section section-bg">
  <div class="container">
    <div class="section-head"><div class="eyebrow">What we stand for</div><h2>Our promise on every job</h2></div>
    <div class="grid grid-3">{val_html}</div>
  </div>
</section>

<section class="section-sm">
  <div class="container">{cta_band("Ready to work with your local hero?", "Free estimate, no obligation \u2014 " + PHONE, "Book now", "../#book")}</div>
</section>
"""
    html += footer("../")
    write("about/index.html", html)


# ---------------- CONTACT ----------------
def build_contact():
    html = head(
        "Contact | Book Junk Removal in DFW | Mr Haul Hero",
        "Contact Mr Haul Hero for junk removal in Dallas–Fort Worth. Call or text 214-517-2955, email us, or book online. Open 8am–8pm, 7 days a week.",
        "../", "/contact/"
    )
    html += nav("../", "contact")
    html += f"""
<section class="page-hero">
  <div class="container"><div class="eyebrow">Contact</div><h1>Let's get your junk hauled</h1><p>Call, text, email, or fill out the form \u2014 we'll get you a free quote fast.</p></div>
</section>

<section class="section">
  <div class="container area-grid">
    <div class="city-box">
      <h3>Get in touch</h3>
      <div class="footer-contact" style="color:#3C4658;">
        <div class="line" style="display:flex;align-items:center;gap:10px;margin-bottom:14px;"><i class="ti ti-phone" style="color:#0A1B3D;"></i><a href="{PHONE_HREF}">{PHONE}</a></div>
        <div class="line" style="display:flex;align-items:center;gap:10px;margin-bottom:14px;"><i class="ti ti-message" style="color:#0A1B3D;"></i><a href="{SMS_HREF}">Text us anytime</a></div>
        <div class="line" style="display:flex;align-items:center;gap:10px;margin-bottom:14px;"><i class="ti ti-mail" style="color:#0A1B3D;"></i><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="line" style="display:flex;align-items:center;gap:10px;margin-bottom:14px;"><i class="ti ti-clock" style="color:#0A1B3D;"></i>Open 8am\u20138pm, 7 days a week</div>
        <div class="line" style="display:flex;align-items:center;gap:10px;"><i class="ti ti-map-pin" style="color:#0A1B3D;"></i>Serving all of DFW \u2014 we come to you</div>
      </div>
    </div>
    <div>{booking_form()}</div>
  </div>
</section>

<section class="section-sm">
  <div class="container">{cta_band("Prefer to talk it through?", "Call or text \u2014 " + PHONE, "Call now", PHONE_HREF)}</div>
</section>
"""
    html += footer("../")
    write("contact/index.html", html)


# ---------------- SERVICE AREA OVERVIEW ----------------
def build_service_area_index():
    cards = ""
    for slug in CITY_ORDER:
        name = CITY_MAP[slug][1].replace(", TX", "")
        cards += f'<a class="city-card" href="{slug}/"><span>{name}</span><i class="ti ti-arrow-right"></i></a>\n'
    html = head(
        "Service Area | DFW Junk Removal Locations | Mr Haul Hero",
        "Mr Haul Hero provides junk removal across Dallas–Fort Worth including Dallas, Fort Worth, Plano, Frisco, McKinney, Denton and more. Find your city.",
        "../", "/service-area/"
    )
    html += nav("../", "service-area")
    html += f"""
<section class="page-hero">
  <div class="container"><div class="eyebrow">Service area</div><h1>Serving all of Dallas\u2013Fort Worth</h1><p>No storefront, no problem \u2014 we come to you, 8am\u20138pm, 7 days a week. Find your city below.</p></div>
</section>

<section class="section">
  <div class="container">
    <div class="area-map" style="margin-bottom:40px;height:360px;">
      <iframe class="map-embed" style="min-height:360px;" src="https://www.google.com/maps?q=Dallas-Fort+Worth,+TX&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of Dallas-Fort Worth service area"></iframe>
    </div>
    <div class="city-cards">{cards}</div>
    <p style="text-align:center;font-size:13px;color:#8B93A6;margin-top:24px;">...and surrounding areas. Don't see your city? <a href="{PHONE_HREF}" style="color:#0A1B3D;font-weight:500;">Give us a call</a> \u2014 chances are we cover you.</p>
  </div>
</section>

<section class="section-sm">
  <div class="container">{cta_band("Ready to clear the clutter?", "Free estimate, no obligation \u2014 " + PHONE, "Book now", "../#book")}</div>
</section>
"""
    html += footer("../")
    write("service-area/index.html", html)


# ---------------- CITY PAGES ----------------
def build_city_pages():
    for slug, display, intro, nearby in CITIES:
        name = display.replace(", TX", "")
        prefix = "../../"
        # services icon row (compact)
        svc_row = ""
        compact = [("junk", "General Junk"), ("garage", "Garage Cleanout"), ("furniture", "Furniture"),
                   ("yard", "Yard Debris"), ("appliance", "Appliances"), ("construction", "Construction")]
        icon_map = {"junk": "ti-trash", "garage": "ti-car-garage", "furniture": "ti-sofa",
                    "yard": "ti-leaf", "appliance": "ti-refrigerator", "construction": "ti-building-warehouse"}
        for key, lbl in compact:
            svc_row += f'<div class="feature" style="text-align:center;"><div class="ico" style="margin:0 auto 12px;"><i class="ti {icon_map[key]}"></i></div><h3 style="font-size:13px;">{lbl}</h3></div>\n'
        nearby_html = "".join(f'<div class="item-row" style="border-left-color:#0A1B3D;justify-content:center;"><span>{n}</span></div>' for n in nearby)
        map_q = display.replace(" ", "+").replace(",", "%2C")

        html = head(
            f"Junk Removal in {display} | Same-Day Hauling | Mr Haul Hero",
            f"Fast, licensed junk removal in {display}. Furniture, appliances, garage cleanouts & debris hauling. Free estimates, 15% off your first job. Call {PHONE}.",
            prefix, f"/service-area/{slug}/"
        )
        html += nav(prefix, "service-area")
        html += f"""
<div class="crumb"><div class="container"><a href="{prefix}service-area/">Service area</a> / <span class="here">{name}</span></div></div>

<section class="page-hero" style="text-align:left;">
  <div class="container area-grid" style="align-items:center;">
    <div>
      <div class="badge-line"><i class="ti ti-map-pin-filled"></i> Serving {display}</div>
      <h1>Junk Removal in {display}</h1>
      <p style="margin:0 0 24px;max-width:480px;">{intro}</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="{prefix}#book" style="color:#fff;">Book now</a>
        <a class="btn btn-outline" href="{PHONE_HREF}"><i class="ti ti-phone"></i>{PHONE}</a>
      </div>
    </div>
    <div class="area-map" style="min-height:240px;">
      <iframe class="map-embed" style="min-height:240px;" src="https://www.google.com/maps?q={map_q}&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of {display}"></iframe>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head"><div class="eyebrow">What we haul in {name}</div><h2>Our services</h2></div>
    <div class="grid grid-6">{svc_row}</div>
  </div>
</section>

<section class="section section-bg">
  <div class="container">{price_box(city=name)}</div>
</section>

<section class="section-sm">
  <div class="container">
    <div class="section-head"><div class="eyebrow">Nearby cities</div><h2>Also serving areas near {name}</h2></div>
    <div class="item-list" style="max-width:420px;">{nearby_html}</div>
  </div>
</section>

<section class="section-sm">
  <div class="container">{cta_band(f"Ready to clear your junk in {name}?", "Free estimate, no obligation \u2014 " + PHONE, "Book now", prefix + "#book")}</div>
</section>
"""
        html += footer(prefix)
        write(f"service-area/{slug}/index.html", html)


if __name__ == "__main__":
    build_home()
    build_services()
    build_pricing()
    build_about()
    build_contact()
    build_service_area_index()
    build_city_pages()
    print("\nDone. Site built into", ROOT)
