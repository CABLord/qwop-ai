
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import cv2
import numpy as np
import pytesseract

# Constants
POPULATION_SIZE = 10
CHROMOSOME_LENGTH = 10
MUTATION_RATE = 0.1
MAX_GENERATIONS = 100

# Gene: (key, duration)
POSSIBLE_KEYS = ['Q', 'W', 'O', 'P', 'SL']  # SL for Sleep/No action

class QwopAI:
    def __init__(self):
        self.driver = webdriver.Chrome()  # You'll need to have ChromeDriver installed
        self.driver.get("http://www.foddy.net/Athletics.html")  # QWOP game URL
        
    def generate_chromosome(self):
        return [(random.choice(POSSIBLE_KEYS), random.uniform(0.1, 3.0)) for _ in range(CHROMOSOME_LENGTH)]
    
    def generate_population(self):
        return [self.generate_chromosome() for _ in range(POPULATION_SIZE)]
    
    def fitness(self, chromosome):
        distance, time_taken = self.play_game(chromosome)
        if time_taken == 0:
            return 0
        return distance / time_taken

    def select_parents(self, population):
        # Tournament selection
        tournament_size = 3
        tournament = random.sample(population, tournament_size)
        return max(tournament, key=self.fitness)

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, CHROMOSOME_LENGTH - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutate(self, chromosome):
        for i in range(len(chromosome)):
            if random.random() < MUTATION_RATE:
                chromosome[i] = (random.choice(POSSIBLE_KEYS), random.uniform(0.1, 3.0))
        return chromosome
    
    def play_game(self, chromosome):
        # Reset the game
        self.driver.refresh()
        time.sleep(2)  # Wait for the game to load

        start_time = time.time()
        for gene in chromosome:
            key, duration = gene
            if key != 'SL':
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(key)
            time.sleep(duration)

        end_time = time.time()
        distance = self.extract_distance()
        return distance, end_time - start_time

    def extract_distance(self):
        # Take a screenshot
        screenshot = self.driver.get_screenshot_as_png()
        nparr = np.frombuffer(screenshot, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Extract the region with the distance text
        height, width = img.shape[:2]
        roi = img[int(height*0.1):int(height*0.2), int(width*0.4):int(width*0.6)]

        # Convert to grayscale and apply threshold
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Extract text using pytesseract
        text = pytesseract.image_to_string(thresh, config='--psm 7 -c tessedit_char_whitelist=0123456789.-')
        
        try:
            distance = float(text.strip())
        except ValueError:
            distance = 0.0

        return distance

    def run_generation(self, population):
        # Evaluate fitness for each individual
        fitness_scores = [(individual, self.fitness(individual)) for individual in population]
        
        # Sort by fitness (descending order)
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select top performers
        top_performers = [individual for individual, _ in fitness_scores[:POPULATION_SIZE//2]]
        
        # Create new population
        new_population = top_performers.copy()
        
        while len(new_population) < POPULATION_SIZE:
            parent1 = self.select_parents(top_performers)
            parent2 = self.select_parents(top_performers)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)
        
        return new_population
    
    def run_evolution(self):
        population = self.generate_population()
        for generation in range(MAX_GENERATIONS):
            print(f"Generation {generation + 1}")
            population = self.run_generation(population)
            # TODO: Check for termination condition
        
    def cleanup(self):
        self.driver.quit()

if __name__ == "__main__":
    ai = QwopAI()
    try:
        ai.run_evolution()
    finally:
        ai.cleanup()
