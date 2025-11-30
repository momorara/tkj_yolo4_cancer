# -*- coding: utf-8 -*-
"""
画像から簡易的にラベルを作ります。

本来はしっかりアノテーションして作るべきものですが、
対象画像がほぼアノテーション結果で切り取られているものとして処理します。

python -m pip install pillow

ddata_cnを対象にラベルをつくり　同じディレクトリにlabelsフォルダを作ります

data_l/
├── images/
│   ├── train/*.jpg
│   ├── test/*.jpg
│   └── valid/*.jpg
└── labels/
    ├── train/*.txt
    └── valid/*.txt

"""
import os
from PIL import Image

SRC_ROOT = "data_cn"     # 入力元
DST_ROOT = "data_l"      # 生成先

splits = ["train", "test", "valid"]

# クラス名 → クラスID
class_ids = {
    "adeno": 0,
    "largecell": 1,
    "squamouscell": 2,
    "normal": 3,
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_yolo_label(label_path, class_id):
    """YOLOラベルを書き出す（画像の95%をカバー）"""
    xc = 0.5
    yc = 0.5
    w = 0.90
    h = 0.90
    with open(label_path, "w") as f:
        f.write(f"{class_id} {xc} {yc} {w} {h}\n")


# ===== 変換メイン処理 =====
for split in splits:
    src_dir = os.path.join(SRC_ROOT, split)
    dst_img_dir = os.path.join(DST_ROOT, "images", split)
    dst_label_dir = os.path.join(DST_ROOT, "labels", split)

    # test のみ labels は作らない
    if split != "test":
        ensure_dir(dst_label_dir)

    ensure_dir(dst_img_dir)

    files = sorted(os.listdir(src_dir))

    for fname in files:
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        src_file = os.path.join(src_dir, fname)
        dst_img_file = os.path.join(dst_img_dir, fname)

        # 画像コピー（RGB + JPEG 化）
        img = Image.open(src_file)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(dst_img_file, "JPEG")

        # ファイル名からクラス名を取得
        cls_name = fname.split("_")[0]
        if cls_name not in class_ids:
            print(f"警告: 不明なクラス → {fname}")
            continue

        class_id = class_ids[cls_name]

        # test split はアノテーション不要
        if split == "test":
            continue

        # ラベルの保存
        base_name = os.path.splitext(fname)[0]
        label_path = os.path.join(dst_label_dir, base_name + ".txt")

        create_yolo_label(label_path, class_id)

print("✔ data_l/images & data_l/labels の生成が完了しました！")
