A wireless home security system made using a webcam, Alexa, Intel Edison, and Python.

1. Captures photos of all incoming people at the door of the house and verifies their identity against a pre-populated database of recognized individuals using the Microsoft Cognitive Services API. If verified, the name is added to the Initial State database with the following keys: Name, Status (inside or outside), Recognized (yes or no), Time of entry, Number of people in the house. It also has the ability to add the recognized image to the database to further train itself and become 'smarter'. If the individual at the door is not recognized, a text message with an image of the unidentified individual is sent to the owner via Twilio.

2. Tracks the total number of people inside the house at any given point of time by tracking both incoming and outgoing traffic.

3. Once a person is granted entry into the house, he/she is greeted (by name) by Alexa and asked for choice of music to play.

4. The owner can monitor all said data in real time on his/her Initial State dashboard.

5. The entire program runs on Intel-Edison i.e. the Edison works as the main computer for the execution.
