FROM python:3.9-slim

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your code and image
COPY blobImg.png ./Project/blobImg.png
COPY BlobDetection.py .

CMD ["python", "BlobDetection.py"]
