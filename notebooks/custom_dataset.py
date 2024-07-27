import os
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset

class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.transform = transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = self.img_labels.iloc[idx, 1]
        if not os.path.isfile(img_path):
            print(f"File not found: {img_path}")  # Debug statement
            raise FileNotFoundError(f"File not found: {img_path}")
        image = Image.open(img_path).convert("RGB")
        label = self.img_labels.iloc[idx, 2]
        top = self.img_labels.iloc[idx, 3]
        left = self.img_labels.iloc[idx, 4]
        height = self.img_labels.iloc[idx, 5]
        width = self.img_labels.iloc[idx, 6]
        bbox = torch.tensor([top, left, height, width], dtype=torch.float32)  # Convert to float32

        if self.transform:
            image = self.transform(image)

        return image, bbox