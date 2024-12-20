# Representative Finder Website

Welcome to the Representative Finder Website, an innovative tool designed to help users discover their political representatives quickly and conveniently. This project was created for the **2024 Congressional App Challenge**, aiming to increase political awareness and engagement using modern, accessible technology.

## Features

- **Find Representatives**: Users can input their location or click on a state to retrieve information about their representatives, including senators, governors, and other officials.
- **Real-Time Data**: Information on political figures is generated dynamically using Google Gemini and other APIs.
- **User-Friendly Interface**: A simple and intuitive design ensures accessibility for all users.
- **Additional Resources**: Access news and updates about U.S. politics to stay informed.

## Technologies Used

- **Flask**: Backend framework for handling requests and serving data.
- **Google Gemini**: For generating dynamic descriptions of political figures.
- **GeoLookup**: For location-based data retrieval.
- **Google Civic Information API**: For fetching official details about representatives.
- **HTML/CSS**: Frontend design and user interface.
- **Bing Image Search API**: To fetch images of political figures.

## Screenshots

### Front Page
![Front Page Screenshot 1](https://ibb.co/282Rr2T)
![Front Page Screenshot 2](https://ibb.co/9GLkLzP)

### Input Location or Select State
![Input Location or Select State Screenshot](https://ibb.co/KwHjBc3)

### Representative Information (Example: Florida)
![Florida Representative Info Screenshot](https://ibb.co/MRHB5yq)

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/representative-finder.git
   cd representative-finder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for API keys:
   - `palmApiKey`: Google Gemini API key.
   - `openAiKey`: OpenAI API key.
   - `googleCivicApiKey`: Google Civic Information API key.
   - `flaskSecretKey`: Flask secret key for sessions.

4. Run the server:
   ```bash
   python main.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Contributing

We welcome contributions to enhance the website! Feel free to submit pull requests or report issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For inquiries or feedback, please contact [your-email@example.com](mailto:your-email@example.com).
