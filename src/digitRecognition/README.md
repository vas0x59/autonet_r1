<br>OCR with a whitelist for numbers works ONLY with tesseract version >= 4.1</br>
<br>So you need to follow this instruction:</br>
<br><code>sudo apt-get install apt-transport-https</code></br>
<br>Add to /etc/apt/sources.list</br>
<br>Add this line for Bionic: <code>deb https://notesalexp.org/tesseract-ocr-dev/bionic/ bionic main</code></br>
<br>Add this line for Cosmic: <code>deb https://notesalexp.org/tesseract-ocr-dev/cosmic/ cosmic main</code></br>
<br>Add this line for Disco: <code>deb https://notesalexp.org/tesseract-ocr-dev/disco/ disco main</code></br>
