# Introduction
#### This is a chat that allows clients to connect with each other either in group
#### chat or private with each other.
When client connects to server he/she have to write his/her nickname,and after it choose with 
whom he/she wants to connect or enter to the group chat.

##### If client wants to change the room he/she has to write in console "CHANGE ROOM"
##### command.


# Table of Content
* [System Requirements](#system-requirements)
* [Installation](#installation)
* [How To Run](#how-to-run)
​
# System Requirements:
 - python3 
 - pip3
​
# Installation
  - Clone the latest version from https://github.com/DavtyanDaniel/websocket_chat_ver_1.0 
  - Install the dependencies (It is highly recommended to create isolated environment!)
  ```sh
  python3 -m venv my_env
  source my_env/bin/activate
  pip3 install -r requirements.txt
  ```

# How to run
 ```sh
$ python3 server.py
$ python3 client.py
 ```

