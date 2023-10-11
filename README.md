# GigaChad ToutPT

## Project Overview

## Project Overview

### French Rap Lyrics Generation AI

GigaChad ToutPT AI is a school project that combines Flutter for the frontend and Python for the backend.
This project showcases a Recurrent Neural Network (RNN) text generation AI trained on French rap songs lyrics, featuring renowned rappers. The AI has been trained on a diverse dataset of lyrics scraped from the internet, capturing the unique styles and expressions of these artists. The model has been built using TensorFlow, and users can interact with the AI through the Flutter frontend to generate unique and creative French rap lyrics inspired by Nekfeu, Vald, and Alpha One.

**PS: Still under developement...**

## Features

1. **Text Generation AI:**

   - The core feature is a powerful RNN text generation AI created using TensorFlow, capable of creating French rap lyrics inspired by rappers styles.
2. **Flutter Frontend:**

   - The user-friendly Flutter frontend allows users to input prompts and receive AI-generated rap lyrics.
3. **Python Backend:**

   - The Python backend manages the TensorFlow-based AI model, handling text generation requests from the Flutter frontend.
4. **Scrapped French Rap Lyrics:**

   - The AI has been trained on a diverse dataset of French rap songs lyrics, with a focus on the styles of Nekfeu, Vald, and AlphaOne.

## Technologies Used

- **Flutter:** A UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase.
- **Python:** The backend is developed using Python to manage the TensorFlow-based text generation AI.
- **TensorFlow:** An open-source machine learning library used for creating and training deep learning models.
- **RNN (Recurrent Neural Network):** A type of artificial neural network designed for sequence tasks, such as text generation.

## How to Run the App

### Flutter Frontend

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/LBrzr/giga_chad_tpt.git
   ```
2. **Navigate to the Project Folder:**

   ```bash
   cd front
   ```
3. **Install Dependencies:**

   ```bash
   flutter pub get
   ```
4. **Run the App:**

   ```bash
   flutter run
   ```

### Python Backend

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/LBrzr/giga_chad_tpt.git
   ```
2. **Navigate to the Project Folder:**

   ```bash
   cd api
   ```
3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Backend:**

   ```bash
   python server.py
   ```

## Preview

###### Loading
![Loading](https://github.com/LBrzr/giga_chad_tpt/blob/main/screens/loading.png?raw=true)

###### Responded
![Loading](https://github.com/LBrzr/giga_chad_tpt/blob/main/screens/responded.png?raw=true)

###### Responding
![Loading](https://github.com/LBrzr/giga_chad_tpt/blob/main/screens/responding.png?raw=true)

## Project Structure

- **front:** Contains the Flutter frontend code.
- **api:** Houses the Python backend code for managing the TensorFlow-based text generation AI and socket connection with the front for word-by-word response.
- **lyrics:** Holds the dataset of French rap songs lyrics used for training the AI model.

## Feedback and Contributions

We welcome feedback and contributions to enhance the project. Feel free to open issues, submit pull requests, or provide insights into improving the AI model.

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://github.com/LBrzr/)

Thank you for exploring the world of French rap lyrics with the TensorFlow-based AI Generation project! 🎤📜
