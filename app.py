import os
import models
import torch
import numpy as np
import pandas as pd
from PIL import Image
from torchvision import transforms
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = models.model(pretrained=False, requires_grad=False).to(device)

checkpoint = torch.load('outputs/model.pth', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

train_csv = pd.read_csv('Multi_Label_dataset/train.csv')
genres = train_csv.columns.values[2:]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

@app.route('/')
def index():
    return render_template('intex.html')


@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    input_image = Image.open(file).convert('RGB')
    input_image = transform(input_image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(input_image)
        outputs = torch.sigmoid(outputs)
        sorted_indices = np.argsort(outputs[0].cpu().numpy())
        best = sorted_indices[-3:]

    predicted_genres = [genres[i] for i in best]
    return jsonify(predicted_genres)
from flask import send_file



if __name__ == '__main__':
    app.run(debug=True)
