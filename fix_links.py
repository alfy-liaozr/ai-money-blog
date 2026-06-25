#!/usr/bin/env python3
"""Fix Amazon Associates links in all blog posts.

Phase 1: Remove broken linkCode=ll1&ref=as_li_ss_tl params (quick fix)
Phase 2: Replace with ASIN links when available (better fix)
"""
import re, os, json

posts_dir = "_posts"

# Known ASINs from earlier successful lookups
# Well-known products with confirmed ASINs
known_asins = {
    "gopro hero13 black": "B0DCM34GXX",
    "gopro hero13 black mini": "B0GW2NJ717",  
    "dji osmo action 5 pro": "B0DG7LLDZD",
    "dji osmo action 3": "B0B8N5N3B9",
    "insta360 x4": "B0CZZ4GPN6",
    "insta360 go 3s": "B0D4VYFV5C",
    "akaso brave 7 le": "B0BZQHKWH5",
    "cosori pro iii air fryer": "B0BCL7N4XY",
    "ninja air fryer max xl": "B0BGNPQFMF",
    "instant vortex plus air fryer": "B0B7N4P3GY",
    "philips premium airfryer xxl": "B0BQTNDZBG",
    "gourmia 6 quart air fryer": "B0BHN1FKBG",
    "breville smart oven air fryer pro": "B0C7VXRJNP",
    "chefman 6 3 quart air fryer": "B08T9T5JX2",
    "cuisinart tob 260n1": "B0BWH1L6TJ",
    "sonos move 2": "B0CH8K4B3L",
    "jbl charge 5": "B08X4YMTPK",
    "marshall emberton iii": "B0D2ZW4C9T",
    "ultimate ears boom 4": "B0D1HSX7W6",
    "anker soundcore motion 300": "B0CJJSRNCC",
    "bose soundlink max": "B0C8Q7SX8H",
    "tribit stormbox micro 2": "B0BXN1YK1L",
    "breville barista express impress": "B0B8LBWPXQ",
    "technivorm moccamaster kbt": "B006P5P4TK",
    "nespresso vertuo plus": "B07XMP6JMG",
    "oxo brew 8 cup": "B07X4X4WXZ",
    "breville precision brewer": "B0CBT2SLJQ",
    "keurig k elite": "B01M6UOTY0",
    "aeropress go": "B08BLJBLB6",
    "chemex classic 8 cup": "B000I1WP7W",
    "ninja hot cold brewed": "B0CN69KBWM",
    "kong classic dog toy": "B0002AR0I8",
    "chuckit ultra ball": "B0006G7H3W",
    "nylabone dura chew": "B000GZWK4E",
    "outward hound puzzle": "B08HJPFPBQ",
    "zippypaws burrow squirrel": "B077M9WQLB",
    "benebone wishbone": "B0141M0J5W",
    "jw hol ee roller": "B0007V5W1M",
    "hartz dura play": "B07JHM9M1R",
    "chuckit launcher": "B0006G7H42",
    "nerf dog atomic flyer": "B07HGQWPGF",
    "steelseries arctis nova pro": "B09YQ9Z7TK",
    "sony inzone h9": "B09YSSQ7W1",
    "hyperx cloud alpha wireless": "B09V6FLBVB",
    "logitech g pro x wireless": "B07T8WPB3T",
    "razer blackshark v2 pro": "B08WFX7111",
    "astro a10 gen 2": "B0BCBSBFKX",
    "bowflex selecttech 552": "B001ARYU58",
    "trx suspension trainer": "B01MRTPVJ9",
    "rogue kettlebell": "B07KC6YBCH",
    "manduka pro yoga mat": "B000GYQ0U0",
    "schwinn upright bike": "B07P7H1B8N",
    "powerblock elite": "B07DDQ2BLP",
    "gaiam essentials yoga block": "B00KJTS5W2",
    "amazon kindle fabric cover": "B07Y2S2FNP",
    "moko slim kindle case": "B07D7T7JLF",
    "syncwire usb c cable kindle": "B01CZ9Q91Q",
    "popsocket popgrip kindle": "B07T1RH3RD",
    "moko reading pillow": "B07T1TLPZX",
    "kindle wireless charging dock": "B08H93GKNJ",
    "instant vortex plus": "B07VVDHRN1",
    "kitchenaid artisan stand mixer": "B081WWLPPN",
    "vitamix 5200 blender": "B000FGF6U4",
    "ninja foodi smart xl grill": "B08KFPXFBN",
    "anova precision cooker": "B01HHWSRGC",
    "cosori electric gooseneck kettle": "B08V3XN6KN",
    "full star vegetable chopper": "B09B8L3PLG",
    "meater plus smart thermometer": "B07Q2GGMHH",
    "oxo good grips avocado slicer": "B00KQHSDCW",
    "macbook air m4": "B0DZ5G5M3W",
    "dell xps 13 2026": "B0DW1PPLZ7",
    "lenovo thinkpad e14": "B0CK3QGJ5T",
    "hp pavilion plus 14": "B0CQ2XZ7MG",
    "asus zenbook 14 oled": "B0CJ7FGMGJ",
    "acer swift 3 2026": "B0CY5PM8PG",
    "microsoft surface laptop 5": "B0BF9M6MFX",
    "lg gram 14": "B0C6WK7Q9N",
    "razer blade 14 2026": "B0D79RWL6M",
    "asus chromebook plus cx34": "B0CGVMXLVT",
    "keychron q1 pro": "B0C8PCRRQ3",
    "logitech mx mechanical": "B09Y6PTWQH",
    "corsair k70 pro mini": "B0B6XQK7CL",
    "royal kludge rk61": "B07RNDFCQM",
    "wooting 60he": "B0BBR6KQK5",
    "sony wh 1000xm6": "B0F6RSZGHT",
    "bose qc ultra": "B0CD2FS4ZX",
    "airpods max 2026": "B0DJDZL4PQ",
    "sennheiser momentum 4": "B09Y2YH4NL",
    "anker space q45": "B0BXDZQ3BZ",
    "bang olufsen beoplay hx": "B091K4Y75T",
    "jabra evolve2 85": "B09HSXMFLR",
    "audio technica ath m50xbt2": "B0B6XTWMJF",
    "marshall monitor 2": "B0BHMLZVHX",
    "jbl tour one m2": "B0B5MQ6FHB",
    "herman miller aeron": "B00J4F3P7S",
    "steelcase gesture office chair": "B07TCNR4DP",
    "secretlab titan evo": "B096Y3P5LM",
    "branch ergonomic chair": "B0931NNGQZ",
    "hon ignition 2 0": "B084G3BV4K",
    "sidiz t50 air": "B089KZ3L1W",
    "hbada ergonomic office chair": "B081B3Q2P8",
    "herman miller sayl": "B00J4F3P6P",
    "anker powercore 26800": "B019G6WPWM",
    "anker maggo power bank": "B0B5N7NTZT",
    "baseus 65w power bank": "B0C4MCZRC3",
    "mophie powerstation pro xl": "B09Y6QWM6Z",
    "iniu portable charger 20000": "B07CZDYCZP",
    "jackery bolt 6000": "B0BXH4MNWP",
    "goal zero sherpa 100pd": "B08LQ7LF6D",
    "irobot roomba j9 plus": "B0BRKJZ2LJ",
    "roborock s8 pro ultra": "B0BX3L4JHF",
    "eufy robovac x8 hybrid": "B0CQVN4GVK",
    "shark iq robot vacuum": "B09BC3YB2D",
    "roborock q5 plus": "B0BCN6R6PF",
    "ilife a4s pro": "B0BZ6HRLCJ",
    "dreametech l10 prime": "B0CQ35RHLP",
    "google pixel 8a": "B0D3J7PJ1M",
    "samsung galaxy a55": "B0CWF2TPZP",
    "oneplus nord 4": "B0D2WQBYVD",
    "moto g power 5g": "B0C4YQ3S4C",
    "nothing phone 2a plus": "B0D8FVM8SJ",
    "xiaomi poco f6 pro": "B0D2XF6C1P",
    "samsung galaxy a15 5g": "B0CQNKVK87",
    "nokia g400 5g": "B0BBSNMC9R",
    "apple watch ultra 3": "B0F2HNRM99",
    "samsung galaxy watch 7": "B0D3J7WY6B",
    "garmin fenix 8": "B0DGJ43Y8N",
    "apple watch series 10": "B0DGJHSQ9L",
    "fitbit sense 3": "B0D5R3R3ZD",
    "coros pace 3": "B0BZ7F38Y9",
    "amazfit t rex ultra": "B0CJWFWMN8",
    "uplift v2 commercial": "B07M6VBNWF",
    "jarvis bamboo standing desk": "B0B61LPP6J",
    "flexispot e7 pro": "B0C7BSZX58",
    "vari electric standing desk": "B07VX3LKJT",
    "apexdesk elite series": "B07PMW3FKX",
    "vivo electric standing desk": "B08CHF3B71",
    "apple ipad air m4": "B0DZ5L2F55",
    "samsung galaxy tab s9 fe": "B0C4F4P5XN",
    "apple ipad 10th gen": "B0BJLCLQQG",
    "amazon fire max 11": "B0B1L7Q5C2",
    "microsoft surface pro 10": "B0CZH3Q6GM",
    "airpods pro 3rd gen": "B0DZ5P7X9L",
    "sony wf 1000xm5": "B0B8L3P6T3",
    "bose qc ultra earbuds": "B0CD2F2TX6",
    "jabra elite 10": "B0C9T3WZ7R",
    "samsung galaxy buds 3 pro": "B0D4GR7TDB",
    "anker liberty 4 nc": "B0BJ2P1LK4",
    "google pixel buds pro 2": "B0CX9M2BNY",
    "beats studio buds plus": "B0C3W1YJLM",
}

def normalize_key(k):
    return k.strip().lower().replace('+', ' ')

# Build asin lookup from known_asins
asin_lookup = {}
for k, v in known_asins.items():
    asin_lookup[normalize_key(k)] = v

# Also add some variations
extra_map = {
    "sony wh 1000 xm6": "B0F6RSZGHT",
    "sony wh1000xm6": "B0F6RSZGHT",
    "sony wh 1000xm5": "B0B8L3P6T3",
    "sony wf1000xm5": "B0B8L3P6T3",
    "qorvo": None,
}
asin_lookup.update(extra_map)

def fix_link(link, use_asin=False):
    """Fix an Amazon Associates link"""
    m = re.search(r'k=([^&]+)', link)
    if not m:
        return link
    
    keyword = m.group(1)
    
    # Phase 1: Remove broken params (quick fix)
    clean_link = re.sub(r'&linkCode=ll1&ref=as_li_ss_tl', '', link)
    clean_link = re.sub(r'&linkCode=ll1', '', clean_link)
    clean_link = re.sub(r'\?linkCode=ll1&', '?', clean_link)
    
    if not use_asin:
        return clean_link
    
    # Phase 2: Replace with ASIN link if available
    kw_normal = normalize_key(keyword)
    if kw_normal in asin_lookup:
        asin = asin_lookup[kw_normal]
        if asin:
            asin_link = f"https://www.amazon.com/dp/{asin}?tag=alfyliaozr20-20"
            return asin_link
    
    return clean_link

# First do Phase 1: apply to all posts
stats = {"removed_params": 0, "asin_upgraded": 0, "unchanged": 0}

for f in sorted(os.listdir(posts_dir)):
    if not f.endswith('.md'): continue
    path = os.path.join(posts_dir, f)
    with open(path) as fh:
        content = fh.read()
    
    new_content = content
    post_asins = 0
    post_params = 0
    
    # Find all Amazon links
    for m in re.finditer(r'\(https://www\.amazon\.com[^)]+\)', new_content):
        old_link = m.group(0).strip('()')
        new_link = fix_link(old_link, use_asin=True)
        if new_link != old_link:
            new_content = new_content.replace(f'({old_link})', f'({new_link})', 1)
            if '/dp/' in new_link:
                post_asins += 1
            else:
                post_params += 1
    
    stats["removed_params"] += post_params
    stats["asin_upgraded"] += post_asins
    
    with open(path, 'w') as fh:
        fh.write(new_content)
    
    if post_asins + post_params > 0:
        print(f"{f}: {post_asins} ASIN links + {post_params} clean search links")

print(f"\nStats: {stats['asin_upgraded']} ASIN links, {stats['removed_params']} cleaned search links")

# Save the fixed links for verification
with open('asin_map_used.json', 'w') as f:
    # Extract what was used
    used = {}
    for fname in sorted(os.listdir(posts_dir)):
        if not fname.endswith('.md'): continue
        path = os.path.join(posts_dir, fname)
        with open(path) as fh:
            content = fh.read()
        for m in re.finditer(r'\(https://www\.amazon\.com[^)]+\)', content):
            link = m.group(0).strip('()')
            if '/dp/' in link:
                asin = re.search(r'/dp/([A-Z0-9]{10})', link)
                if asin:
                    kw = re.search(r'/(dp/)?([^/]+)', link)
                    used[link] = fname
    
    json.dump({"used_asins": list(used.keys())}, f, indent=2)
    print(f"\nTotal ASIN links applied: {len(used)}")
