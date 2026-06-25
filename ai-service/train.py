from ultralytics import YOLO
import torch

def main():
    # Load pretrained YOLO11 model
    model = YOLO("yolo11n.pt")
    if torch.cuda.is_available():
        model.to("cuda")
        print("Using GPU: cuda")
    else:
        print("CUDA unavailable, using CPU")

    # Train the model
    model.train(
        data="../datasets/car_damage/data.yaml",
        epochs=100,
        imgsz=640,
        batch=8,
        workers=2,
        project="runs",
        name="autofocus_damage_model"
    )

if __name__ == "__main__":
    main()