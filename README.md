# QWOP AI

This project implements an AI agent to play the QWOP game using a genetic algorithm.

## Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/CABLord/qwop-ai.git
   cd qwop-ai
   ```

2. Install the required Python packages:
   ```
   pip install selenium opencv-python numpy pytesseract webdriver_manager
   ```

3. Install Tesseract OCR:
   - On Ubuntu:
     ```
     sudo apt-get install tesseract-ocr
     ```
   - On macOS:
     ```
     brew install tesseract
     ```
   - On Windows, download the installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

4. Download ChromeDriver:
   - Visit the [ChromeDriver downloads page](https://sites.google.com/a/chromium.org/chromedriver/downloads)
   - Download the version that matches your Chrome browser version
   - Extract the executable and place it in your system PATH or in the same directory as the script

## Usage

Run the script with:

```
python qwop_ai.py
```

The AI will start playing the QWOP game in a Chrome browser window. The evolution process will continue until the AI reaches 100 meters or the maximum number of generations is reached.

## How it works

The AI uses a genetic algorithm to evolve a population of "players". Each player is represented by a chromosome, which is a sequence of key presses and durations. The fitness of each player is determined by how far they manage to run in the game.

The algorithm goes through the following steps:

1. Generate an initial population
2. Evaluate the fitness of each individual
3. Select the best performers
4. Create a new population through crossover and mutation
5. Repeat steps 2-4 for multiple generations

The AI uses Selenium to interact with the game in a Chrome browser and OpenCV with Tesseract OCR to read the distance traveled from the game screen.

