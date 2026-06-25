#!/usr/bin/env python3
"""Batch lookup ASINs for all products from Amazon search"""
import requests, re, time, json, sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

products = [
    "gopro hero13 black",
    "dji osmo action 5 pro",
    "insta360 x4",
    "gopro hero13 black mini",
    "dji osmo action 3",
    "akaso brave 7 le",
    "insta360 go 3s",
    "cosori pro III air fryer",
    "ninja air fryer max xl",
    "instant vortex plus air fryer",
    "philips premium airfryer xxl",
    "gourmia 6 quart air fryer",
    "breville smart oven air fryer pro",
    "chefman 6 3 quart air fryer",
    "cuisinart tob 260n1",
    "sonos move 2",
    "jbl charge 5",
    "marshall emberton III",
    "ultimate ears boom 4",
    "anker soundcore motion 300",
    "bose soundlink max",
    "tribit stormbox micro 2",
    "breville barista express impress",
    "technivorm moccamaster kbt",
    "nespresso vertuo plus",
    "oxo brew 8 cup",
    "breville precision brew",
    "keurig k elite",
    "aeropress go",
    "chemex classic 8 cup",
    "ninja hot cold brewed",
    "kong classic dog toy",
    "chuckit ultra ball",
    "nylabone dura chew",
    "outward hound puzzle",
    "zippypaws burrow squirrel",
    "benebone wishbone",
    "jw hol ee roller",
    "hartz dura play",
    "chuckit launcher",
    "nerf dog atomic flyer",
    "steelseries arctis nova pro",
    "sony inzone h9",
    "hyperx cloud alpha wireless",
    "logitech g pro x wireless",
    "razer blackshark v2 pro",
    "astro a10 gen 2",
    "bowflex selecttech 552",
    "trx suspension trainer",
    "rogue kettlebell",
    "manduka pro yoga mat",
    "schwinn upright bike",
    "powerblock elite",
    "gaiam essentials yoga block",
    "amazon kindle fabric cover",
    "moko slim kindle case",
    "syncwire usb c cable kindle",
    "popsocket popgrip kindle",
    "moko reading pillow",
    "kindle wireless charging dock",
    "instant vortex plus",
    "kitchenaid artisan stand mixer",
    "vitamix 5200 blender",
    "ninja foodi smart xl grill",
    "anova precision cooker",
    "cosori electric gooseneck kettle",
    "full star vegetable chopper",
    "meater plus smart thermometer",
    "oxo good grips avocado slicer",
    "macbook air m4",
    "dell xps 13 2026",
    "lenovo thinkpad e14",
    "hp pavilion plus 14",
    "asus zenbook 14 oled",
    "acer swift 3 2026",
    "microsoft surface laptop 5",
    "lg gram 14",
    "razer blade 14 2026",
    "asus chromebook plus cx34",
    "keychron q1 pro",
    "logitech mx mechanical",
    "corsair k70 pro mini",
    "royal kludge rk61",
    "wooting 60he",
    "sony wh 1000xm6",
    "bose qc ultra",
    "airpods max 2026",
    "sennheiser momentum 4",
    "anker space q45",
    "bang olufsen beoplay hx",
    "jabra evolve2 85",
    "audio technica ath m50xbt2",
    "marshall monitor 2",
    "jbl tour one m2",
    "herman miller aeron",
    "steelcase gesture office chair",
    "secretlab titan evo",
    "branch ergonomic chair",
    "hon ignition 2 0",
    "sidiz t50 air",
    "hbada ergonomic office chair",
    "herman miller sayl",
    "anker powercore 26800",
    "anker maggo power bank",
    "baseus 65w power bank",
    "mophie powerstation pro xl",
    "iniu portable charger 20000",
    "jackery bolt 6000",
    "goal zero sherpa 100pd",
    "irobot roomba j9 plus",
    "roborock s8 pro ultra",
    "eufy robovac x8 hybrid",
    "shark iq robot vacuum",
    "roborock q5 plus",
    "ilife a4s pro",
    "dreametech l10 prime",
    "google pixel 8a",
    "samsung galaxy a55",
    "oneplus nord 4",
    "moto g power 5g",
    "nothing phone 2a plus",
    "xiaomi poco f6 pro",
    "samsung galaxy a15 5g",
    "nokia g400 5g",
    "apple watch ultra 3",
    "samsung galaxy watch 7",
    "garmin fenix 8",
    "apple watch series 10",
    "fitbit sense 3",
    "coros pace 3",
    "amazfit t rex ultra",
    "uplift v2 commercial",
    "jarvis bamboo standing desk",
    "flexispot e7 pro",
    "vari electric standing desk",
    "apexdesk elite series",
    "vivo electric standing desk",
    "apple ipad air m4",
    "samsung galaxy tab s9 fe",
    "apple ipad 10th gen",
    "amazon fire max 11",
    "microsoft surface pro 10",
    "airpods pro 3rd gen",
    "sony wf 1000xm5",
    "bose qc ultra earbuds",
    "jabra elite 10",
    "samsung galaxy buds 3 pro",
    "anker liberty 4 nc",
    "google pixel buds pro 2",
    "beats studio buds plus",
]

def lookup_asin(product_name):
    """Search Amazon and extract first ASIN"""
    k = product_name.replace(' ', '+')
    url = f'https://www.amazon.com/s?k={k}'
    try:
        r = requests.get(url, headers=headers, timeout=15)
        asins = re.findall(r'/dp/([A-Z0-9]{10})/', r.text)
        if asins:
            return asins[0]
        # Fallback: data-asin attributes
        asins2 = re.findall(r'data-asin="([A-Z0-9]{10})"', r.text)
        if asins2:
            return asins2[0]
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

results = {}
total = len(products)
for i, prod in enumerate(products, 1):
    sys.stdout.write(f"\r[{i}/{total}] {prod}... ")
    sys.stdout.flush()
    asin = lookup_asin(prod)
    results[prod] = asin
    if asin:
        sys.stdout.write(f"→ {asin}")
    else:
        sys.stdout.write("→ FAILED")
    sys.stdout.flush()
    time.sleep(1.5)  # Be respectful, delay between requests

print(f"\n\n=== RESULTS ===")
for prod, asin in results.items():
    status = f"✓ {asin}" if asin else "✗ NOT FOUND"
    print(f"{status}: {prod}")

# Save to JSON
with open('asin_map.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to asin_map.json")
