
1. Clone tesstrain:
git clone https://github.com/tesseract-ocr/tesstrain.git

2. Install tesseract build dependencies:
apt-get install automake ca-certificates g++ git libtool libleptonica-dev make pkg-config libpango1.0-dev libicu-dev libcairo2-dev bc libgif-dev libjpeg-dev libpng-dev libtiff-dev zlib1g zlib1g-dev

3. Make (if build fails with cryptic error, might need to append "CORES=1"):
make leptonica tesseract

4. Install Python requirements:
python3 -m pip install -r requirements.txt

5. Download Hebrew trained data
cd ./tesstrain/usr/share/tessdata/ && wget https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/master/heb.traineddata