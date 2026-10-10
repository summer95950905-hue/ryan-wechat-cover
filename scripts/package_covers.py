#!/usr/bin/env python3
"""Package finished wide/square cover designs; no network or publishing."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps


def open_rgb(path):
    with Image.open(path) as source:
        rgba = ImageOps.exif_transpose(source).convert("RGBA")
    background = Image.new("RGBA", rgba.size, "#060606")
    return Image.alpha_composite(background, rgba).convert("RGB")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wide", type=Path, required=True)
    parser.add_argument("--square", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--height", type=int, default=800)
    args = parser.parse_args()
    if args.height <= 0 or args.height % 20:
        parser.error("--height must be a positive multiple of 20")
    wide, square = open_rgb(args.wide), open_rgb(args.square)
    if abs(wide.width / wide.height - 2.35) > 0.01:
        parser.error("--wide must be approximately 2.35:1; compose it before packaging")
    if square.width != square.height:
        parser.error("--square must be square; choose its framing before packaging")

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    resize = Image.Resampling.LANCZOS
    for w, h in [(900, 383), (1800, 766)]:
        wide.resize((w, h), resize).save(out / f"cover-wide-{w}x{h}.png")
    for size in sorted({args.height, 200, 120}):
        square.resize((size, size), resize).save(out / f"cover-square-{size}x{size}.png")

    height = args.height
    wide_width = height * 47 // 20
    total_width = wide_width + height
    left = wide.resize((wide_width, height), resize)
    right = square.resize((height, height), resize)
    master = Image.new("RGB", (total_width, height), "#060606")
    master.paste(left, (0, 0))
    master.paste(right, (wide_width, 0))
    master.save(out / f"cover-upload-master-{total_width}x{height}.png")

    split = f"{wide_width / total_width:.6f}".rstrip("0").rstrip(".")
    fields = {"pic_crop_235_1": f"0_0_{split}_1", "pic_crop_1_1": f"{split}_0_1_1"}
    (out / "crop-fields.json").write_text(json.dumps(fields, indent=2) + "\n", encoding="utf-8")
    for name, key, expected, image in [
        ("wide", "pic_crop_235_1", (0, 0, wide_width, height), left),
        ("square", "pic_crop_1_1", (wide_width, 0, total_width, height), right),
    ]:
        x1, y1, x2, y2 = map(float, fields[key].split("_"))
        box = (round(x1 * total_width), round(y1 * height), round(x2 * total_width), round(y2 * height))
        if box != expected:
            raise ValueError("Crop coordinates do not round-trip to the intended pixel bounds")
        crop = master.crop(box)
        if ImageChops.difference(crop, image).getbbox():
            raise ValueError("Crop pixels differ from the intended cover")
        crop.save(out / f"crop-check-{name}.png")

    preview = Image.new("RGB", (960, 730), "#E8E7E2")
    preview.paste(wide.resize((900, 383), resize), (30, 30))
    preview.paste(square.resize((200, 200), resize), (30, 490))
    preview.paste(square.resize((120, 120), resize), (310, 490))
    labels = ImageDraw.Draw(preview)
    labels.text((30, 454), "SQUARE 200 x 200", fill="#242422")
    labels.text((310, 454), "SQUARE 120 x 120", fill="#242422")
    labels.text((520, 500), "LOCAL PREVIEW / NOT A WECHAT SCREENSHOT", fill="#242422")
    preview.save(out / "cover-preview.png")
    print(json.dumps({"output": str(out.resolve()), "master_size": [total_width, height],
                      "crop_fields": fields, "crop_round_trip": True,
                      "status": "local_only"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
