import os
import zipfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor

out_dir = 'GTA_VI_HighRes_Images'
os.makedirs(out_dir, exist_ok=True)

all_images = [
    # 1. Hero & Key Visual Artwork
    ("01_Jason_and_Lucia_Key_Art_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/poster_full.0az_iud2g3y4j.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("02_Key_Visual_Poster_Title_Logo.png", "https://www.rockstargames.com/VI/_next/static/media/poster_logo.0m-7c805zusl7.png?akim=1&imdensity=1&imwidth=3840"),
    ("03_Official_Meta_Visual.jpg", "https://www.rockstargames.com/VI/_next/static/media/meta.0t8ty~nlmxq2s.jpg"),
    ("04_Hero_Shard_Layer_0.png", "https://www.rockstargames.com/VI/_next/static/media/shard0.0_vm6ya9-h67x.png?akim=1&imdensity=1&imwidth=3840"),
    ("05_Hero_Shard_Layer_1.png", "https://www.rockstargames.com/VI/_next/static/media/shard1.14.-n-5n.4nws.png?akim=1&imdensity=1&imwidth=3840"),
    ("06_Hero_Shard_Layer_2.png", "https://www.rockstargames.com/VI/_next/static/media/shard2.0n4e6vntuoxgf.png?akim=1&imdensity=1&imwidth=3840"),
    ("07_Hero_Shard_Layer_3.png", "https://www.rockstargames.com/VI/_next/static/media/shard3.120i1.3ll3tb9.png?akim=1&imdensity=1&imwidth=3840"),
    ("08_Hero_Shard_Layer_4.png", "https://www.rockstargames.com/VI/_next/static/media/shard4.0bi8cg9mdh8p4.png?akim=1&imdensity=1&imwidth=3840"),
    ("09_Hero_Shard_Layer_5.png", "https://www.rockstargames.com/VI/_next/static/media/shard5.0qdavlhu9vx3m.png?akim=1&imdensity=1&imwidth=3840"),
    ("10_Hero_Shard_Layer_6.png", "https://www.rockstargames.com/VI/_next/static/media/shard6.0m27xv.6a~.pk.png?akim=1&imdensity=1&imwidth=3840"),
    ("11_Hero_Shard_Layer_7.png", "https://www.rockstargames.com/VI/_next/static/media/shard7.0r3-p5yp386ao.png?akim=1&imdensity=1&imwidth=3840"),
    ("12_Hero_Shard_Layer_8.png", "https://www.rockstargames.com/VI/_next/static/media/shard8.0-nawcceg2vqw.png?akim=1&imdensity=1&imwidth=3840"),
    ("13_Hero_Shard_Layer_9.png", "https://www.rockstargames.com/VI/_next/static/media/shard9.08p7clh5_sa.q.png?akim=1&imdensity=1&imwidth=3840"),

    # 2. Official Logos & Title Branding
    ("14_GTA_VI_Official_Emblem_Logo.png", "https://www.rockstargames.com/VI/_next/static/media/vi.0hxa9~pf214xe.png?akim=1&imdensity=1&imwidth=3840"),
    ("15_GTA_Title_Lettering_Logo.png", "https://www.rockstargames.com/VI/_next/static/media/logo_gta.0_~y3s2ni8fbj.png?akim=1&imdensity=1&imwidth=3840"),
    ("16_VI_Roman_Numeral_Gradient_Logo.png", "https://www.rockstargames.com/VI/_next/static/media/logo_vi.02gnpy7k4ozcz.png?akim=1&imdensity=1&imwidth=3840"),

    # 3. Trailers & Video Key Art
    ("17_An_Extended_Look_Desktop_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/an-extended-look.0zw.9~1j0ne~4.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("18_An_Extended_Look_Mobile.jpg", "https://www.rockstargames.com/VI/_next/static/media/an-extended-look-mobile.0f0-3vo3w9u26.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("19_Launch_Trailer_Key_Visual_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/launch-trailer.0cq1gbt4507ty.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("20_Trailer_2_Key_Visual_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/trailer-2.0l.7aqib91fz6.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("21_Trailer_1_Key_Visual_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/trailer-1.06b6paykx247w.jpg?akim=1&imdensity=1&imwidth=3840"),

    # 4. Game Editions & Pre-Order Packs
    ("22_Ultimate_Edition_Desktop_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/ultimate_desktop_en_us.0~shc~hnjifzu.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("23_Ultimate_Edition_Mobile.jpg", "https://www.rockstargames.com/VI/_next/static/media/ultimate_mobile_en_us.03~7e7tlo4k4r.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("24_Vintage_Vice_City_Pack_Artwork_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/VINTAGE_VICE_CITY_PACK_01.05zaof7o1uz.3.jpg?akim=1&imdensity=1&imwidth=3840"),

    # 5. Feature Highlights & Promotional Visuals
    ("25_Music_and_Soundtrack_Desktop_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/musicDesktop.0zwcbzhynnsc-.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("26_Music_and_Soundtrack_Mobile.jpg", "https://www.rockstargames.com/VI/_next/static/media/musicMobile.16pdg34v6lit..jpg?akim=1&imdensity=1&imwidth=3840"),
    ("27_Launch_Gallery_Promo_Desktop_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/screenshotsDesktop.0q9.0q677hl7h.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("28_Launch_Gallery_Promo_Mobile.jpg", "https://www.rockstargames.com/VI/_next/static/media/screenshotsMobile.01nsldjqbta4u.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("29_Media_Downloads_Desktop_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/mediaDesktop.11iioep6d3wsf.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("30_Media_Downloads_Mobile.jpg", "https://www.rockstargames.com/VI/_next/static/media/mediaMobile.0p_yfitphljim.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("31_Only_In_Leonida_Desktop_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/onlyInLeonidaDesktop.15y2n40f3axwo.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("32_Only_In_Leonida_Mobile.jpg", "https://www.rockstargames.com/VI/_next/static/media/onlyInLeonidaMobile.0mupfnk-x6x~r.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("33_Merchandise_Promo_Card_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/GTAVI_Merch_PromoCard.0_k5n2lk~h9h~.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("34_Collectors_Box_Vice_City_Collection.png", "https://www.rockstargames.com/VI/_next/static/media/collectorsMobile.09~60xnm5q~pr.png?akim=1&imdensity=1&imwidth=3840"),

    # 6. Featured News / Newswire Cards
    ("35_Newswire_PreLoad_Now_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/89834o94713o21.04n287k6o2lh9.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("36_Newswire_Explore_Launch_Gallery_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/39ak81277255o9.0lmk9f~r~10.x.jpg?akim=1&imdensity=1&imwidth=3840"),
    ("37_Newswire_PreLoad_Begins_Nov10_3840.jpg", "https://www.rockstargames.com/VI/_next/static/media/k4ak9okk485712.0cj_8hoskvfgy.jpg?akim=1&imdensity=1&imwidth=3840"),
]

def download_one(item):
    filename, url = item
    target_path = os.path.join(out_dir, filename)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        return f"OK (exists): {filename}"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.rockstargames.com/'
        })
        with urllib.request.urlopen(req, timeout=20) as resp, open(target_path, 'wb') as f:
            f.write(resp.read())
        return f"DOWNLOADED: {filename} ({os.path.getsize(target_path):,} bytes)"
    except Exception as e:
        return f"FAILED: {filename} -> {e}"

print(f"Downloading {len(all_images)} high-resolution images...")
with ThreadPoolExecutor(max_workers=6) as executor:
    results = list(executor.map(download_one, all_images))

for r in results:
    print(r)

# Create zip file
zip_path = "GTA_VI_Images_HiRes.zip"
print(f"\nCreating ZIP archive: {zip_path}...")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for filename, _ in all_images:
        fp = os.path.join(out_dir, filename)
        if os.path.exists(fp):
            zipf.write(fp, arcname=filename)

print(f"ZIP archive created successfully: {zip_path} ({os.path.getsize(zip_path):,} bytes)")
