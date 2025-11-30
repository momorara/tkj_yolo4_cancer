# -*- coding: utf-8 -*-
"""
data_j/test/
├── adeno/
├── largecell/
├── squamouscell/
└── normal

data_j/train/
├── adeno/
├── largecell/
├── squamouscell/
└── normal

data_j/valid/
├── adeno/
├── largecell/
├── squamouscell/
└── normal
フォルダの画像データの名前を数字のみにする

新しいデータは
data_tvtとする
"""
import os
from PIL import Image

SRC_ROOT = "data_j"
DST_ROOT = "data_tvt"

splits = ["train", "test", "valid"]
classes = ["adeno", "largecell", "squamouscell", "normal"]


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def copy_and_rename_images(src_dir, dst_dir):
    """src_dir 内の画像を連番で dst_dir にコピーする"""

    ensure_dir(dst_dir)

    files = sorted(os.listdir(src_dir))
    counter = 1

    for fname in files:
        src_file = os.path.join(src_dir, fname)

        # ファイル以外は無視
        if not os.path.isfile(src_file):
            continue

        # 画像を開いて jpeg として保存（非 JPEG 対策）
        try:
            img = Image.open(src_file)

            if img.mode != "RGB":
                img = img.convert("RGB")

            dst_file = os.path.join(dst_dir, f"{counter}.jpg")
            img.save(dst_file, "JPEG")

            counter += 1

        except Exception as e:
            print(f"変換エラー: {src_file}: {e}")


for split in splits:
    for cls in classes:
        src_dir = os.path.join(SRC_ROOT, split, cls)
        dst_dir = os.path.join(DST_ROOT, split, cls)

        copy_and_rename_images(src_dir, dst_dir)

print("✔ data_n の生成が完了しました")
