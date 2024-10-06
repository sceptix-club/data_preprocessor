# PDF to Structured JSON Converter

Welcome to the **PDF to Structured JSON Converter**! This project automates the extraction of information from **PDF files** (such as safety data sheets) and organizes it into a **parent-child structured JSON** format. This README provides all the necessary details to get you started with this project.

---

## Process

The users are required to follow instructions for different platforms (both .py and .ipynb are available)

### 1. Using Google Collab
Use the following link to use the notebook 
https://colab.research.google.com/drive/1zvHS8fMXAR6u1Y5rixeIW830c7V95IO_?usp=sharing


### 2. Using Linux
1. **Fork the Repository:** Click the "Fork" button at the top right of this repository to create a copy in your GitHub account. 🍴
2. **Clone Your Fork:** Clone the forked repository to your local machine using Git. 🖥️

   ```bash
   git clone https://github.com/<your/user/name>/data_preprocessor.git
   ```
   replace <your/user/name> with the actual account name
3. **Install these dependencies:** 
   Open the terminal and run the command
   ```bash
   !apt-get install poppler-utils tesseract-ocr
   ```
4. **Install the required libraries:** Use the following command
   ```bash
   pip install -r requirements.txt
   ```
5. **Note:** Please change the input/output folders depending on the desired location.

### 3. Using Windows
1. **Fork the Repository:** Click the "Fork" button at the top right of this repository to create a copy in your GitHub account. 🍴

2. **Clone Your Fork:** Clone the forked repository to your local machine using Git. 🖥️

   ```bash
   git clone https://github.com/<your/user/name>/data_preprocessor.git
   ```
   replace <your/user/name> with the actual account name

3. **Install ollama from the internet and download mistral:** 
   - Serve and install the LLM (Mistral)

   ``` ollama serve & ollama pull mistral```

   - Run the LLM using this command

   ```ollama run mistral```

4. **Install the required libraries:** Use the following command
   ```bash
   pip install -r requirements.txt
   ```

5. **Note:** Please change the input/output folders depending on the desired location



_Happy Coding_😎