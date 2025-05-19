from flask_cors import CORS
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
import sqlite3
import os
from flask import Flask, request, render_template
from PIL import Image
from flask import jsonify


# Initialize Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Updated class labels
class_names = [
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
]

# Load Model
def load_model(model_path):
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(class_names))
    
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict, strict=False)
    
    model.to(device)
    model.eval()
    return model

model = load_model("plant_disease_model.pth")


def get_treatment(disease_name):
    conn = sqlite3.connect("plant_treatment.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM treatments WHERE disease_name = ?", (disease_name,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "Disease Name": result[0],
            "Symptoms": result[1],
            "Causes": result[2],
            "Recommended Medicine/Fertilizer/Vitamins": result[3],
            "Dosage & Duration": result[4],
            "Preventive Measures": result[5],
            "Recommended Pesticides": result[6],
            "Pesticide Usage Measures": result[7]
        }
    return None



# Prediction Function
def predict(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
    
    return class_names[predicted.item()]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def handle_prediction():
    file = request.files['image']
    if file.filename == '':
        return render_template('index.html', error="No file uploaded")
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    disease_name = predict(filepath)
    treatment = get_treatment(disease_name)
    
    return render_template('result.html', disease=disease_name, treatment=treatment, image_path=filepath)

CORS(app)
@app.route('/api/predict', methods=['POST'])
def api_predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Invalid file type'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    disease_name = predict(filepath)
    treatment = get_treatment(disease_name)

    return jsonify({
        'disease': disease_name,
        'treatment': treatment,
        'image_url': f'/static/uploads/{file.filename}'
    })


if __name__ == '__main__':
    app.run(debug=True)
