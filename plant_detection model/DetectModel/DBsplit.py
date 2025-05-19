import os
import shutil
import random

def split_dataset(source_dir, target_dir, valid_split=0.2):
    """Splits dataset into train and validation sets."""
    
    # Ensure target directories exist
    train_dir = os.path.join(target_dir, "train")
    valid_dir = os.path.join(target_dir, "valid")
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(valid_dir, exist_ok=True)
    
    # Get all class folders
    classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    
    for c in classes:
        class_path = os.path.join(source_dir, c)
        train_class_path = os.path.join(train_dir, c)
        valid_class_path = os.path.join(valid_dir, c)
        os.makedirs(train_class_path, exist_ok=True)
        os.makedirs(valid_class_path, exist_ok=True)
        
        images = os.listdir(class_path)
        random.shuffle(images)
        
        split_idx = int(len(images) * (1 - valid_split))
        
        for img in images[:split_idx]:
            shutil.copy(os.path.join(class_path, img), os.path.join(train_class_path, img))
        
        for img in images[split_idx:]:
            shutil.copy(os.path.join(class_path, img), os.path.join(valid_class_path, img))
    
    print(f"Dataset split into train and valid sets and saved in {target_dir}")

# Example usage:
source_directory = "PlantVillage"
target_directory = r"C:\000000000000000\Demo\Model\plant_detection model\PlantVillageReduced"
split_dataset(source_directory, target_directory)
