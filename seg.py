#imports
import os
import time
import numpy as np

try:
    from PIL import Image
except:
    os.system("pip install Pillow==9.4.0")
    from PIL import Image

try:
    import torch
except:
    os.system("pip install torch")
    import torch

try:
    from torchvision import transforms, models
except:
    os.system("pip install torchvision==0.11.3")
    from torchvision import transforms, models

try:
    from matplotlib import pyplot as plt
    from matplotlib import image as mpimg
except:
    os.system("pip install matplotlib==3.7.1")
    from matplotlib import pyplot as plt
    from matplotlib import image as mpimg

try:
    from flask import Flask, render_template, request, redirect
    from werkzeug.utils import secure_filename
except:
	os.system("pip install flask")
	os.system("pip install werkzeug ")
	from flask import Flask, render_template
	from werkzeug.utils import secure_filename



app = Flask(__name__)

# Function to process image and predict segmentation using DeepLabV3 model
def process_image_and_predict(file_path: str) -> Image.Image:
    model = models.segmentation.deeplabv3_resnet101(pretrained=True)
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((223, 223)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image = Image.open(file_path).convert("RGB")
    image = transform(image)
    image = image.unsqueeze(0)

    with torch.no_grad():
        output = model(image)["out"]

    mask = torch.argmax(output.squeeze(), dim=0).detach().cpu().numpy()
    rng = np.random.default_rng(12345)
    values = np.unique(mask)
    color_map = {value: rng.integers(0, 256, size=3) for value in values}
    colored_mask = np.zeros((*mask.shape, 3), dtype=np.uint8)
    for value, color in color_map.items():
        colored_mask[mask == value] = color

    return Image.fromarray(colored_mask)

@app.route('/uploader', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    files = request.files.getlist("file")
    segmentations = []

    # Process and predict segmentation for each file
    for file in files:
        if file.filename == '':
            return 'No selected file'

        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'Invalid file type'

        seg = process_image_and_predict(file)
        segmentations.append(seg)

    # Iterate for each file in the files list, and save them
    #for file, seg in zip(files, segmentations):
        #seg.save(file.filename)

        # Display segmented images in a window
    fig, axs = plt.subplots(1, len(files))
    fig.suptitle("Segmented Images")
    if not isinstance(axs, np.ndarray):
        axs = np.array([axs])  # Convert axs to numpy array if it's not already

    for ax, seg in zip(axs.flatten(), segmentations):
        ax.imshow(seg)
        ax.axis("off")

    plt.show()

    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

def main():
    start_time = time.time()
    app.run(debug=True)
    delta_time = time.time() - start_time
    m, s = divmod(delta_time, 60)
    h, m = divmod(m, 60)
    print("--- Program Finished (Took %d:%02d:%02d) ---" % (h, m, s))

if __name__ == '__main__':
    main()