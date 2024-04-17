# Craftrice

## Before you get any further
This project is highly outdated and might not work perfectly. This project was made 1 year ago for a computer science tournament. The socket library provided by mojang was highly outdated, we still took the risk of using it and it was working somewhat fine. Now that Minecraft has received at least 2 major updates since the project, I can't promise that the project still works as intended. Minecraft could at any time, completly drop support for the sockets to work.

## How does it work ?
The project is divided into 3 pieces, the MCSocket that actually sends and receive data, the Flask which is a library to make websites using Python and the Minecraft Map. You get into Minecraft Bedrock Edition, you import the map and play on it, you start the MCSockets python file, then you type /connect IP:PORT (IP:PORT are provided by the MCSocket file). **IMPORTANT**: NEVER INSTALL PYTHON ON MICROSOFT STORE, it lacks a lot of features and blocks Python from doing anything out of the ordinary, including websockets...
Once it's connected, wait for it to calculate the result and once it's done, it will be in the output of the console.

## Why are we not using the Flask part ?
Because I did not have any solution to actually make it work back when I created the project. If I ever want to finish the project completly, I should be able to use it as I have a good idea to make it work!
