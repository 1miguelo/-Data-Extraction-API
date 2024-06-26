# Rick and Morty Character Explorer

This Python program uses the tkinter library to create a graphical user interface (GUI) that allows users to explore information about characters from the TV series "Rick and Morty" via the Rick and Morty API.

## Prerequisites

- Python 3.x
- Libraries: tkinter, PIL, requests

## Dependency Installation

```bash
pip install pillow requests
```

## Configuration

1. Ensure you have an active internet connection to fetch character information from the Rick and Morty API.
2. Place an image of Rick and Morty named "RickAndMorty.jpg" in the same folder as the main script (optional as the image is included in the .zip).

## Usage

1. Run the script, and a login window will open.
2. Enter your credentials (any of the two in the `users.txt` file) and click "Log In".
3. A window will appear where you can enter the number of characters you want to see (between 1 and 32).
4. Click "Log In" to view the character information in the main window.

## Additional Features

- The application displays an image of Rick and Morty on the login screen.
- Character data is fetched from the Rick and Morty API and displayed in the main window, including their name, species, gender, and an image.

## Notes

- The maximum number of characters that can be requested from the API is 32, for easy screen visualization.
