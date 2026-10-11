# T-Pad
- The T-Pad is a basic telemetry module that will track different metrics using 4 main sensors and then send those metrics to a web dashboard. I made this project as an intro into sensors to use as reference to future projects with sensors and data being fed back to a main dashboard.

# How it works
- The board's brain is a RP2040 Zero that will then send info back to the computer via USB. The board features the following:
  -   A BME280 to track temperature and humidity
  -   A RP2040 as the brain
  -   An INA 219 to track voltage supply
  -   BH1750 to track light intensity
  -   A BMI 270 as a gyroscope and accelerometer

# The code
- The code is a basic python script that collects the data and dumps it as a JSON file
- The code also uses a modified BMI270 driver adapted by both AI and I to work with CircuitPython
- The javascript attached to the website then interprets the JSON
- This info is then sent to the dashboard
NOTE: the data in the site is example data

# Photos
Schematic:
<img width="2191" height="1225" alt="image" src="https://github.com/user-attachments/assets/36f65ffd-ce72-48c6-93a3-255ff315f49b" />

PCB:
<img width="941" height="615" alt="image" src="https://github.com/user-attachments/assets/8bff5954-e3d1-4da2-9cec-07dbab2783e8" />

