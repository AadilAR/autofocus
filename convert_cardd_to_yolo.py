from __future__ import annotations

import json
import random
import shutil
from pathlib import Path

from tqdm import tqdm

CLASS_MAP = {
    "dent": 0,
    "scratch": 1,
    "crack": 2,
    "glass shatter": 3,
    "lamp broken": 4,
    "tire flat": 5,
}

RATIOS = {"train": 0.8, "val": 0.1, "test": 0.1}

DATA_YAML = """path: {base}

train: images/train
val: images/val
test: images/test

names:
  0: dent
  1: scratch
  2: crack
  3: glass shatter
  4: lamp broken
  5: tire flat
"""


def find_samples_json(root: Path) -> Path:
    candidates = [
        root / "datasets" / "CarDD" / "samples.json",
        root / "autofocus" / "datasets" / "CarDD" / "samples.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    raise FileNotFoundError(
        "Could not find datasets/CarDD/samples.json. Please place the script in the workspace root or update the dataset path."
    )


def create_output_structure(output_root: Path) -> None:
    for category in ("images", "labels"):
        for split in ("train", "val", "test"):
            (output_root / category / split).mkdir(parents=True, exist_ok=True)


def yolo_label_line(label: str, bbox: list[float]) -> str:
    class_id = CLASS_MAP[label]
    x, y, width, height = bbox
    x_center = x + width / 2.0
    y_center = y + height / 2.0
    return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"


def write_label_file(label_path: Path, detections: list[dict]) -> None:
    lines = []
    for detection in detections:
        label = detection.get("label")
        bbox = detection.get("bounding_box")
        if label is None or bbox is None:
            continue
        if label not in CLASS_MAP:
            continue
        lines.append(yolo_label_line(label, bbox))

    label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def split_samples(samples: list[dict]) -> dict[str, list[dict]]:
    random.seed(42)
    shuffled = samples.copy()
    random.shuffle(shuffled)

    total = len(shuffled)
    train_end = int(total * RATIOS["train"])
    val_end = train_end + int(total * RATIOS["val"])

    return {
        "train": shuffled[:train_end],
        "val": shuffled[train_end:val_end],
        "test": shuffled[val_end:],
    }


def main() -> None:
    root = Path(__file__).resolve().parent
    samples_path = find_samples_json(root)
    dataset_root = samples_path.parent
    output_root = dataset_root.parent / "car_damage"

    with samples_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    samples = data.get("samples", [])
    if not samples:
        raise ValueError(f"No samples found in {samples_path}")

    create_output_structure(output_root)
    splits = split_samples(samples)

    total_images = 0
    split_counts = {"train": 0, "val": 0, "test": 0}

    for split_name, split_data in splits.items():
        for sample in tqdm(split_data, desc=f"Copying {split_name}", unit="image"):
            filepath = sample.get("filepath")
            if not filepath:
                continue

            src_image = dataset_root / filepath
            if not src_image.exists():
                raise FileNotFoundError(f"Image file not found: {src_image}")

            dest_image = output_root / "images" / split_name / src_image.name
            shutil.copy2(src_image, dest_image)

            detections = []
            detections_field = sample.get("detections")
            if isinstance(detections_field, dict):
                detections = detections_field.get("detections", [])

            label_path = output_root / "labels" / split_name / f"{src_image.stem}.txt"
            write_label_file(label_path, detections)

            total_images += 1
            split_counts[split_name] += 1

    data_yaml_path = output_root / "data.yaml"
    data_yaml_path.write_text(DATA_YAML.format(base=str(output_root.as_posix())), encoding="utf-8")

    print(f"Total images: {total_images}")
    print(f"Training images: {split_counts['train']}")
    print(f"Validation images: {split_counts['val']}")
    print(f"Test images: {split_counts['test']}")


if __name__ == "__main__":
    main()
