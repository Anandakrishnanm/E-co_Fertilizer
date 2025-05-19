import os
import shutil
import random

def reduce_dataset(source_dir, target_dir, max_samples=5000):
    """Reduces dataset to a specified number of images while keeping class balance."""
    
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Get all class folders
    classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    
    total_images = sum(len(os.listdir(os.path.join(source_dir, c))) for c in classes)
    images_per_class = max_samples // len(classes)
    
    print(f"Total images in dataset: {total_images}")
    print(f"Allocating approximately {images_per_class} images per class.")
    
    for c in classes:
        class_path = os.path.join(source_dir, c)
        target_class_path = os.path.join(target_dir, c)
        os.makedirs(target_class_path, exist_ok=True)
        
        images = os.listdir(class_path)
        random.shuffle(images)
        
        for img in images[:images_per_class]:
            shutil.copy(os.path.join(class_path, img), os.path.join(target_class_path, img))
    
    print(f"Dataset reduced and saved in {target_dir}")

# Example usage:
source_directory = r"C:\Users\manan\Downloads\archive (3)\PlantVillage\PlantVillage"
target_directory = r"C:\000000000000000\Demo\Model\plant_detection model"
reduce_dataset(source_directory, target_directory)
