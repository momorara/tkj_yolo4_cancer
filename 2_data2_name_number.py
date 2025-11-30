# -*- coding: utf-8 -*-
"""
dataset_jをyolowで処理しやすいように

ファィル名を　クラス+数字にする

現在のデータセットは
data_tvt/test/
├── adeno/
├── largecell/
├── squamouscell/
└── normal

datadata_tvt_j/train/
├── adeno/
├── largecell/
├── squamouscell/
└── normal

data_tvt/valid/
├── adeno/
├── largecell/
├── squamouscell/
└── normal

これを

data_cn/test/
├── adeno_001.jpg
├── largecell_001.jpg
├── squamouscell_001.jpg
└── normal_001.jpg

data_cn/train/
├── adeno_001.jpg
├── largecell_001.jpg
├── squamouscell_001.jpg
└── normal_001.jpg

data_cn/valid/
├── adeno_001.jpg
├── largecell_001.jpg
├── squamouscell_001.jpg
└── normal_001.jpg

"""
import os
from PIL import Image

SRC_ROOT = "data_tvt"
DST_ROOT = "data_cn"

splits = ["train", "test", "valid"]
classes = ["adeno", "largecell", "squamouscell", "normal"]


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def process_split(split):
    src_split_dir = os.path.join(SRC_ROOT, split)
    dst_split_dir = os.path.join(DST_ROOT, split)

    ensure_dir(dst_split_dir)

    for cls in classes:
        src_cls_dir = os.path.join(src_split_dir, cls)

        if not os.path.exists(src_cls_dir):
            print(f"警告: {src_cls_dir} が存在しません")
            continue

        files = sorted(os.listdir(src_cls_dir))
        counter = 1

        for fname in files:
            src_file = os.path.join(src_cls_dir, fname)

            if not os.path.isfile(src_file):
                continue

            # 出力ファイル名
            dst_file = os.path.join(
                dst_split_dir,
                f"{cls}_{counter:03d}.jpg"
            )

            # JPEG で保存（元が PNG 等でもOK）
            try:
                img = Image.open(src_file)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(dst_file, "JPEG")
            except Exception as e:
                print(f"エラー: {src_file}: {e}")

            counter += 1


# 全 split を処理
for split in splits:
    process_split(split)

print("✔ 変換完了：data_cn に保存しました")
