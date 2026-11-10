import os
import math
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    font_names = [
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibri.ttf",
        "arial.ttf"
    ]
    if bold:
        font_names = [
            "C:\\Windows\\Fonts\\segoeuib.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "C:\\Windows\\Fonts\\calibrib.ttf",
            "arialbd.ttf"
        ] + font_names
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()

MATERIAL_THEMES = {
    "Bamboo": {
        "bg_top": (245, 243, 235),
        "bg_bottom": (224, 235, 218),
        "accent": (76, 120, 68),
        "highlight": (180, 160, 120),
        "badge_bg": (232, 245, 233),
        "badge_fg": (46, 125, 50),
    },
    "Steel": {
        "bg_top": (240, 244, 248),
        "bg_bottom": (216, 226, 236),
        "accent": (74, 95, 120),
        "highlight": (160, 180, 200),
        "badge_bg": (227, 242, 253),
        "badge_fg": (25, 118, 210),
    },
    "Organic Cotton": {
        "bg_top": (250, 247, 242),
        "bg_bottom": (230, 240, 232),
        "accent": (82, 128, 92),
        "highlight": (210, 195, 170),
        "badge_bg": (236, 248, 240),
        "badge_fg": (46, 125, 50),
    },
    "Glass": {
        "bg_top": (240, 248, 252),
        "bg_bottom": (210, 235, 245),
        "accent": (40, 130, 160),
        "highlight": (170, 220, 238),
        "badge_bg": (224, 247, 250),
        "badge_fg": (0, 131, 143),
    },
    "Recycled Plastic": {
        "bg_top": (240, 249, 246),
        "bg_bottom": (215, 240, 230),
        "accent": (38, 135, 105),
        "highlight": (120, 200, 175),
        "badge_bg": (224, 242, 238),
        "badge_fg": (0, 121, 107),
    },
}

def draw_gradient(draw, width, height, c_top, c_bottom):
    for y in range(height):
        factor = y / float(height)
        r = int(c_top[0] + (c_bottom[0] - c_top[0]) * factor)
        g = int(c_top[1] + (c_bottom[1] - c_top[1]) * factor)
        b = int(c_top[2] + (c_bottom[2] - c_top[2]) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_illustration(draw, p_id, cx, cy, accent, highlight):
    # cx, cy is the center of the illustration area (around 400, 270 on an 800x600 canvas)
    # Generic soft shadow below illustration
    draw.ellipse([cx - 130, cy + 95, cx + 130, cy + 125], fill=(200, 210, 205))

    if p_id == 1:  # Bamboo Toothbrush
        # Handle
        draw.polygon([(cx - 110, cy + 60), (cx + 80, cy - 20), (cx + 90, cy - 10), (cx - 100, cy + 75)], fill=highlight)
        # Brush head
        draw.rounded_rectangle([cx + 65, cy - 35, cx + 115, cy - 5], radius=8, fill=highlight)
        # Bristles
        for i in range(5):
            bx = cx + 72 + i * 8
            draw.line([(bx, cy - 35), (bx, cy - 55)], fill=(255, 255, 255), width=4)
        # Leaf accent
        draw.polygon([(cx - 15, cy + 10), (cx + 5, cy - 10), (cx + 5, cy + 15)], fill=accent)

    elif p_id in [2, 9, 23]:  # Steel Bottle / Glass Bottle / Water Jug
        # Bottle body
        draw.rounded_rectangle([cx - 50, cy - 50, cx + 50, cy + 90], radius=16, fill=accent)
        # Highlight streak
        draw.rounded_rectangle([cx - 35, cy - 40, cx - 22, cy + 80], radius=6, fill=highlight)
        # Bottle neck
        draw.rectangle([cx - 22, cy - 85, cx + 22, cy - 50], fill=accent)
        # Cap
        draw.rounded_rectangle([cx - 28, cy - 105, cx + 28, cy - 85], radius=6, fill=highlight)
        if p_id == 23:  # Handle for Jug
            draw.arc([cx + 35, cy - 40, cx + 85, cy + 50], start=270, end=90, fill=accent, width=12)

    elif p_id in [3, 21]:  # T-Shirt / Hoodie
        # T-Shirt body
        draw.polygon([
            (cx - 35, cy - 70), (cx + 35, cy - 70),  # collar
            (cx + 80, cy - 40), (cx + 120, cy - 10), (cx + 95, cy + 25), (cx + 70, cy + 0), # right sleeve
            (cx + 65, cy + 85), (cx - 65, cy + 85),  # bottom hem
            (cx - 70, cy + 0), (cx - 95, cy + 25), (cx - 120, cy - 10), (cx - 80, cy - 40) # left sleeve
        ], fill=accent)
        # Collar curve
        draw.arc([cx - 25, cy - 80, cx + 25, cy - 55], start=0, end=180, fill=(255, 255, 255), width=6)
        # Leaf or Eco symbol in chest
        draw.ellipse([cx - 18, cy - 25, cx + 18, cy + 15], fill=highlight)

    elif p_id in [4, 19]:  # Glass Storage Jar / Spice Jar Set
        # Jar body
        draw.rounded_rectangle([cx - 60, cy - 40, cx + 60, cy + 85], radius=14, fill=highlight)
        # Jar glass reflection
        draw.line([(cx - 45, cy - 20), (cx - 45, cy + 70)], fill=(255, 255, 255), width=6)
        draw.line([(cx + 45, cy - 20), (cx + 45, cy + 70)], fill=(255, 255, 255), width=6)
        # Wooden/Bamboo Lid
        draw.rounded_rectangle([cx - 66, cy - 65, cx + 66, cy - 40], radius=8, fill=accent)
        # Label
        draw.rounded_rectangle([cx - 38, cy + 5, cx + 38, cy + 45], radius=4, fill=(255, 255, 255))
        draw.line([(cx - 25, cy + 20), (cx + 25, cy + 20)], fill=accent, width=3)
        draw.line([(cx - 20, cy + 30), (cx + 20, cy + 30)], fill=accent, width=3)

    elif p_id in [5, 20]:  # Notebook / Pen Pack
        if p_id == 5:
            # Notebook cover
            draw.rounded_rectangle([cx - 70, cy - 85, cx + 65, cy + 85], radius=8, fill=accent)
            # Spine highlight
            draw.rectangle([cx - 70, cy - 85, cx - 45, cy + 85], fill=highlight)
            # Leaf emblem on cover
            draw.ellipse([cx - 10, cy - 20, cx + 30, cy + 20], fill=(255, 255, 255))
            draw.ellipse([cx, cy - 10, cx + 20, cy + 10], fill=accent)
            # Bookmark ribbon
            draw.polygon([(cx + 20, cy + 75), (cx + 35, cy + 75), (cx + 27, cy + 105)], fill=highlight)
        else:
            # 3 Pens
            for idx, off in enumerate([-35, 0, 35]):
                draw.rounded_rectangle([cx + off - 8, cy - 75, cx + off + 8, cy + 65], radius=5, fill=accent if idx%2==0 else highlight)
                draw.polygon([(cx + off - 6, cy + 65), (cx + off + 6, cy + 65), (cx + off, cy + 85)], fill=(50, 50, 50))
                draw.rectangle([cx + off - 9, cy - 55, cx + off - 6, cy - 25], fill=(200, 200, 200)) # clip

    elif p_id in [6, 17]:  # Eco Shopping Bag / Reusable Grocery Bags
        # Bag body
        draw.rounded_rectangle([cx - 75, cy - 30, cx + 75, cy + 85], radius=10, fill=highlight)
        # Handles
        draw.arc([cx - 45, cy - 85, cx + 45, cy - 10], start=180, end=0, fill=accent, width=10)
        # Center green leaf imprint
        draw.ellipse([cx - 25, cy + 5, cx + 25, cy + 55], fill=accent)
        draw.line([(cx, cy + 10), (cx, cy + 50)], fill=(255, 255, 255), width=3)

    elif p_id in [7, 28]:  # Bamboo Cutlery Set / Steel Cutlery Set
        # Fork
        draw.rounded_rectangle([cx - 65, cy - 70, cx - 35, cy - 30], radius=4, fill=accent)
        draw.line([(cx - 58, cy - 70), (cx - 58, cy - 45)], fill=(240, 240, 240), width=4)
        draw.line([(cx - 42, cy - 70), (cx - 42, cy - 45)], fill=(240, 240, 240), width=4)
        draw.rounded_rectangle([cx - 53, cy - 30, cx - 47, cy + 75], radius=3, fill=accent)
        # Knife
        draw.polygon([(cx - 6, cy - 75), (cx + 8, cy - 65), (cx + 8, cy - 20), (cx - 6, cy - 20)], fill=highlight)
        draw.rounded_rectangle([cx - 4, cy - 20, cx + 4, cy + 75], radius=3, fill=accent)
        # Spoon
        draw.ellipse([cx + 35, cy - 75, cx + 70, cy - 25], fill=accent)
        draw.rounded_rectangle([cx + 49, cy - 25, cx + 56, cy + 75], radius=3, fill=accent)

    elif p_id in [8, 18, 24, 25]:  # Lunch Box / Food Container / Storage Box
        # Box container
        draw.rounded_rectangle([cx - 95, cy - 40, cx + 95, cy + 70], radius=16, fill=highlight)
        # Box lid
        draw.rounded_rectangle([cx - 105, cy - 65, cx + 105, cy - 35], radius=10, fill=accent)
        # Clips/latches
        draw.rounded_rectangle([cx - 80, cy - 45, cx - 55, cy - 25], radius=4, fill=(80, 80, 80))
        draw.rounded_rectangle([cx + 55, cy - 45, cx + 80, cy - 25], radius=4, fill=(80, 80, 80))
        # Divider line
        draw.line([(cx - 80, cy + 15), (cx + 80, cy + 15)], fill=(255, 255, 255), width=3)

    elif p_id == 10:  # Recycled Plastic Chair
        # Chair backrest
        draw.rounded_rectangle([cx - 55, cy - 85, cx + 55, cy - 10], radius=12, fill=accent)
        # Chair seat
        draw.rounded_rectangle([cx - 70, cy - 10, cx + 70, cy + 15], radius=6, fill=highlight)
        # Chair legs
        draw.line([(cx - 55, cy + 15), (cx - 65, cy + 85)], fill=accent, width=8)
        draw.line([(cx + 55, cy + 15), (cx + 65, cy + 85)], fill=accent, width=8)
        draw.line([(cx - 30, cy + 15), (cx - 20, cy + 80)], fill=(120, 120, 120), width=6)
        draw.line([(cx + 30, cy + 15), (cx + 20, cy + 80)], fill=(120, 120, 120), width=6)

    elif p_id in [11, 22]:  # Bedsheet / Bath Towel
        # Stack of folded fabrics
        for i, y_off in enumerate([40, 0, -40]):
            col = accent if i % 2 == 0 else highlight
            draw.rounded_rectangle([cx - 85, cy + y_off - 20, cx + 85, cy + y_off + 25], radius=12, fill=col)
            draw.arc([cx - 85, cy + y_off - 20, cx - 55, cy + y_off + 25], start=90, end=270, fill=(255, 255, 255), width=4)

    elif p_id == 12:  # Bamboo Hair Brush
        # Brush head
        draw.ellipse([cx - 55, cy - 80, cx + 55, cy + 10], fill=highlight)
        # Handle
        draw.rounded_rectangle([cx - 12, cy + 10, cx + 12, cy + 85], radius=6, fill=accent)
        # Bristles pins
        for rx in range(-35, 45, 18):
            for ry in range(-60, 0, 18):
                draw.ellipse([cx + rx - 3, cy + ry - 3, cx + rx + 3, cy + ry + 3], fill=accent)

    elif p_id in [13, 14]:  # Coffee Mug / Glass Tea Cup
        # Cup body
        draw.rounded_rectangle([cx - 60, cy - 45, cx + 40, cy + 65], radius=14, fill=accent)
        # Mug handle
        draw.arc([cx + 10, cy - 25, cx + 75, cy + 45], start=270, end=90, fill=accent, width=12)
        # Inner steam
        for sx in [-30, -10, 10]:
            draw.arc([cx + sx, cy - 85, cx + sx + 20, cy - 50], start=180, end=360, fill=highlight, width=4)

    elif p_id == 15:  # Yoga Mat
        # Rolled cylindrical mat
        draw.rounded_rectangle([cx - 100, cy - 40, cx + 80, cy + 45], radius=24, fill=accent)
        # Roll spiral on right
        draw.ellipse([cx + 50, cy - 40, cx + 105, cy + 45], fill=highlight)
        draw.ellipse([cx + 68, cy - 22, cx + 88, cy + 27], fill=accent)
        # Straps
        draw.line([(cx - 40, cy - 40), (cx - 40, cy + 45)], fill=(40, 40, 40), width=8)
        draw.line([(cx + 20, cy - 40), (cx + 20, cy + 45)], fill=(40, 40, 40), width=8)

    elif p_id == 16:  # Bamboo Straw Set
        # Straws bundle
        for idx, (sx, rot) in enumerate([(-30, -15), (-10, -5), (10, 10), (30, 20)]):
            draw.line([(cx + sx - 15, cy + 75), (cx + sx + 15, cy - 75)], fill=highlight if idx%2==0 else accent, width=12)
        # Band holding them
        draw.rounded_rectangle([cx - 45, cy - 10, cx + 45, cy + 15], radius=4, fill=(60, 60, 60))

    elif p_id == 26:  # Socks
        # Pair of socks
        for ox in [-30, 25]:
            draw.polygon([
                (cx + ox - 20, cy - 70), (cx + ox + 15, cy - 70),
                (cx + ox + 15, cy + 10), (cx + ox + 45, cy + 45),
                (cx + ox + 35, cy + 70), (cx + ox - 5, cy + 55),
                (cx + ox - 20, cy + 15)
            ], fill=accent if ox < 0 else highlight)
            # Cuff stripe
            draw.line([(cx + ox - 20, cy - 60), (cx + ox + 15, cy - 60)], fill=(255, 255, 255), width=4)

    elif p_id == 27:  # Bamboo Laptop Stand
        # Angled riser stand
        draw.polygon([(cx - 85, cy + 50), (cx + 85, cy - 35), (cx + 95, cy - 20), (cx - 65, cy + 65)], fill=highlight)
        draw.polygon([(cx - 95, cy + 50), (cx - 80, cy + 10), (cx - 60, cy + 15), (cx - 75, cy + 55)], fill=accent)
        draw.line([(cx - 90, cy + 50), (cx + 70, cy + 50)], fill=accent, width=14)

    elif p_id == 29:  # Glass Serving Bowl
        # Bowl shape
        draw.pieslice([cx - 90, cy - 50, cx + 90, cy + 80], start=0, end=180, fill=highlight)
        draw.ellipse([cx - 90, cy - 55, cx + 90, cy - 15], fill=accent)
        # Fruit or eco contents inside
        draw.ellipse([cx - 30, cy - 40, cx, cy - 10], fill=(230, 80, 80))
        draw.ellipse([cx - 5, cy - 45, cx + 25, cy - 15], fill=(76, 175, 80))
        draw.ellipse([cx + 15, cy - 35, cx + 45, cy - 5], fill=(255, 193, 7))

    elif p_id == 30:  # Recycled Plastic Dustbin
        # Bin body
        draw.polygon([(cx - 55, cy - 35), (cx + 55, cy - 35), (cx + 42, cy + 75), (cx - 42, cy + 75)], fill=accent)
        # Bin lid
        draw.rounded_rectangle([cx - 65, cy - 55, cx + 65, cy - 35], radius=6, fill=highlight)
        # Handle on lid
        draw.arc([cx - 20, cy - 70, cx + 20, cy - 45], start=180, end=0, fill=highlight, width=6)
        # Recycle symbol mark
        draw.ellipse([cx - 15, cy + 5, cx + 15, cy + 35], outline=(255, 255, 255), width=3)
    else:
        # Default elegant eco container
        draw.rounded_rectangle([cx - 60, cy - 60, cx + 60, cy + 60], radius=16, fill=accent)
        draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=highlight)

def generate_product_image(product, output_path):
    width, height = 800, 600
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    mat = product["material"]
    theme = MATERIAL_THEMES.get(mat, MATERIAL_THEMES["Bamboo"])

    # Gradient background
    draw_gradient(draw, width, height, theme["bg_top"], theme["bg_bottom"])

    # Inner decorative border frame
    draw.rounded_rectangle([25, 25, width - 25, height - 25], radius=24, outline=(220, 230, 225), width=3)

    # Top-Left Material Badge
    mat_text = mat.upper()
    font_badge = get_font(22, bold=True)
    draw.rounded_rectangle([45, 45, 45 + len(mat_text) * 15 + 30, 95], radius=12, fill=theme["badge_bg"], outline=theme["badge_fg"], width=2)
    draw.text((60, 58), f"🌱 {mat_text}", fill=theme["badge_fg"], font=font_badge)

    # Top-Right Eco Score Badge
    score = product.get("eco_score", 80)
    grade = "A" if score >= 85 else ("B" if score >= 75 else ("C" if score >= 60 else "D"))
    score_text = f"SCORE {score} • GRADE {grade}"
    font_score = get_font(20, bold=True)
    score_box_w = 260
    draw.rounded_rectangle([width - 45 - score_box_w, 45, width - 45, 95], radius=12, fill=(255, 255, 255), outline=theme["accent"], width=2)
    draw.text((width - 45 - score_box_w + 18, 58), score_text, fill=theme["accent"], font=font_score)

    # Center Illustration
    draw_illustration(draw, product["id"], cx=400, cy=285, accent=theme["accent"], highlight=theme["highlight"])

    # Bottom Product Name Panel
    draw.rounded_rectangle([45, 475, width - 45, 555], radius=18, fill=(255, 255, 255), outline=(210, 220, 215), width=2)
    font_title = get_font(30, bold=True)
    title = product["name"]
    # Center text
    bbox = draw.textbbox((0, 0), title, font=font_title)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    draw.text((text_x, 498), title, fill=(35, 45, 40), font=font_title)

    # Resize with high quality antialiasing to target size (600x450)
    final_img = img.resize((600, 450), Image.Resampling.LANCZOS)
    final_img.save(output_path, "JPEG", quality=95)

if __name__ == "__main__":
    from app import products
    out_dir = os.path.join("static", "images")
    os.makedirs(out_dir, exist_ok=True)
    for p in products:
        path = os.path.join(out_dir, f"product{p['id']}.jpg")
        generate_product_image(p, path)
        print(f"Generated {path}")
    print("All 30 product images successfully created!")
