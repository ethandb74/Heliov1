# Heliov1
Hand tracking Solar panel module
IDEA/Concept: Robotic Appendage that is idle and tracks sun to get powered. Then there is a Manual Override mode which is controlled by Hand Motions (Inspired by Tony Stark) The inspiration is robotic arms that build and maintain space systems like the CANADARM of the ISS. Because I have a big passion for Space. What I am actually building is a prototype or model of that. I will make a Cad container that will contain two metal servos that Pan and Tilt. at the end their is a solar panel attached. I have a python script (python --> pyfirmata + MP+pysolar ---> arduino) that 1. tracks the location of the sun and points the appendage at it.and 2. has mode switching capabilities to manual ovveride. There is no robotic Gripper as this is v1 proof of concept. 

Below is a preview of the project. 
<img width="1371" height="787" alt="Screenshot 2026-04-11 150502" src="https://github.com/user-attachments/assets/30dbf376-3def-4d6b-b40c-15a29403a645" />

Below is the full cad with the electroninc componants inserted insde. 
<img width="1420" height="914" alt="Screenshot 2026-04-26 221248" src="https://github.com/user-attachments/assets/e608f33e-faa9-468a-a2dd-35da080ddeba" />
<img width="1417" height="855" alt="Screenshot 2026-04-26 221126" src="https://github.com/user-attachments/assets/58edd79a-556f-4bdc-8290-fd8438efc494" />

My electroinc wiring. It is very simple the only issue was getting the right power for the metal servos. They cant be powerd directly from the arduino as the draw too much current. To workaround this I use and external power supply; I used an AC to DC adapter and step down to 5v 5a which is perfect for the servos. (notice the common ground but nothing powerd from ardunio):
<img width="985" height="741" alt="Screenshot 2026-04-28 193325" src="https://github.com/user-attachments/assets/dd8d1de2-c3da-4c7a-8e36-9f186322b58d" />




For the CAD design I did use multiple sorces as reference but the actual desing was made from scratch. Fusion 360:
<img width="1397" height="834" alt="Screenshot 2026-04-11 145942" src="https://github.com/user-attachments/assets/5b2c6f8f-7fbc-4963-9b63-9eb32c3339f4" />


**Firmware**
I used a variety of libraries- OpenCV and MP for the hand tracking. Very simple to work with. For suntracking I used pysolar.
<img width="1004" height="361" alt="Screenshot 2026-04-08 081736" src="https://github.com/user-attachments/assets/681d1aaf-3964-4abd-92f1-9bef26efa01d" />

<img width="909" height="1077" alt="Screenshot 2026-04-07 201716" src="https://github.com/user-attachments/assets/47230069-3e67-4cf3-8cd8-d23d393c04ae" />
Handtracking.





-
Bill of Materials

Componant: Arduino,
Servo MG 9996R,
Jumper Wires,
Stranded core copper wire,
Perfboard

Quantity: 1x, 2x, 6x, 5x, 1x

see full [BOM.md](./BOM.md)
