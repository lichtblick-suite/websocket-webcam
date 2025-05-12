# Webcam Script 📸

A simple Python script that uses OpenCV to access your webcam.

## 🚀 Setup Instructions

Follow these steps to set up and run the script in a virtual environment.

### 1️⃣ Clone the Repository

Open a terminal and run:

```
git clone git@github.com:Lichtblick-Suite/websocket-webcam.git
cd websocket-webcam
```

### 2️⃣ Create and Activate a Virtual Environment

On macOS/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

On Windows (PowerShell):

```
python -m venv venv
venv\Scripts\Activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run the Script

```
python main.py
```

##🛑 Deactivating the Virtual Environment

When you're done, you can deactivate the virtual environment by running:

deactivate

## 📝 Dependencies

This script requires the following dependencies:

opencv-python for webcam access
foxglove-schemas (if needed for message formats)
These are installed automatically when you run pip install -r requirements.txt.

## 🛠️ Troubleshooting

OpenCV Installation Issues
If you encounter issues with OpenCV, try installing the headless version:

```
pip install opencv-python-headless
```

Virtual Environment Not Activating?
If source venv/bin/activate doesn’t work on macOS/Linux, you may need to allow execution permissions:

```
chmod +x venv/bin/activate
source venv/bin/activate
```

On Windows, if you see a script execution error, run PowerShell as administrator and allow scripts:

```
Set-ExecutionPolicy Unrestricted -Scope Process
```

## 📜 License

This project is open-source and available under the MIT License.
