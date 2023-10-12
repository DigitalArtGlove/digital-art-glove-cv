# digital-art-glove-cv

Hi welcome to the cv side of the digital art glove!

To get the CV up and started just run `python cv_input.py` in this folder.
To get the ESP32 connect, run `python serial_input.py` in this folder.

This should start the CV script and send the position data to a websocket that the UI can read from.

Note: if you need to use a virtual environment to run mediapipe hands or openCV make sure to enter your virtual environment before running the above command. To do so, enter:
`.\venv\Scripts\activate`
and to terminate the virtual environment run `deactivate`.

Please disregard the test.py file in this folder. It was used as an intermediary file to better understand the CV but is now depricated and is only being kept to track history.

Happy art-glove-ing!
