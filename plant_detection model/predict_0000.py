# import torch
# import torch.nn as nn
# import torchvision.transforms as transforms
# from torchvision import models
# from PIL import Image
# import os

# # Set device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Define transformations (must match training preprocessing)
# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
# ])

# # Load class labels
# class_names = [
# # "Pepper,_bell___Bacterial_spot"
#     "Pepper,_bell___healthy", "Potato___Early_blight",
#     "Potato___Late_blight", "Potato___healthy",
#     "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
#     "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite",
#     "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus",
#     "Tomato___healthy"
# ]

# # Load model
# def load_model(model_path):
#     model = models.resnet18(pretrained=False)
#     num_ftrs = model.fc.in_features
#     model.fc = nn.Linear(num_ftrs, len(class_names))  # Adjust output layer
#     model.load_state_dict(torch.load(model_path, map_location=device))
#     model.to(device)
#     model.eval()
#     return model

# # Predict function
# def predict(image_path, model):
#     image = Image.open(image_path).convert('RGB')
#     image = transform(image).unsqueeze(0).to(device)  # Preprocess and add batch dimension
    
#     with torch.no_grad():
#         output = model(image)
#         _, predicted = torch.max(output, 1)
    
#     return class_names[predicted.item()]

# # Load model and test on an image
# if __name__ == "__main__":
#     model_path = r"C:\000000000000000\Demo\Model\plant_detection model\plant_disease_model.pth"  # Update with actual model path
#     image_path = r"C:\000000000000000\Demo\Model\plant_detection model\test\test3.JPG"  # Update with the test image path
    
#     if not os.path.exists(image_path):
#         print(f"Error: Image '{image_path}' not found!")
#     else:
#         model = load_model(model_path)
#         prediction = predict(image_path, model)
#         print(f"Predicted Disease: {prediction}")
