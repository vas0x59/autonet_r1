<br>OCR with a whitelist for numbers works ONLY with tesseract version >= 4.1</br>
<br>So you need to follow this instruction:</br>
<br><code>sudo apt-get install apt-transport-https</code></br>
<br>To /etc/apt/sources.list</br>
<br>Ubuntu</br>
<br>Add this line for Bionic: <code>deb https://notesalexp.org/tesseract-ocr-dev/bionic/ bionic main</code></br>
<br>Add this line for Cosmic: <code>deb https://notesalexp.org/tesseract-ocr-dev/cosmic/ cosmic main</code></br>
<br>Add this line for Disco: <code>deb https://notesalexp.org/tesseract-ocr-dev/disco/ disco main</code></br>
<br>Raspian</br>
<br>Add this line for Stretch: <code>deb https://notesalexp.org/tesseract-ocr-dev/raspbian/stretch/ stretch main</code></br>
<br>Add this line for Buster: <code>deb https://notesalexp.org/tesseract-ocr-dev/raspbian/buster/ buster main</code></br>
<br>Then</br>
<br><code>wget -O - https://notesalexp.org/debian/alexp_key.asc | sudo apt-key add -</code></br>
<br><code>sudo apt-get update</code></br>
<br><code>sudo apt-get install tesseract-ocr</code></br>
<br><code>pip3 install pytesseract</code></br>
