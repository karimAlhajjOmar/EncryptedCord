<h1>EncryptedCord</h1>

EncryptedCord is a Python application built with tkinter and discord.py to create an encrypted Discord bot. It encrypts messages before sending them and decrypts them upon reception, ensuring secure communication over Discord channels. You can call it Encrypted Discord
Features

  <li>  End-to-End Encryption: Messages sent through the bot are encrypted using the Fernet encryption scheme from the cryptography library.</li>
    <li>Channel Interaction: Set a Discord channel ID to send and receive encrypted messages.</li>
    <li>GUI Interface: Built with tkinter for easy interaction and message display.</li>
    <li>Secure Key Management: Includes functionality to generate and securely store encryption keys.</li>

<h1>Requirements</h1>

  <li>Python 3.6 or higher</li>
  <li>discord.py, cryptography, tkinter (usually included in Python installations)</li>

<h1>Installation</h1>

  <li>Clone the repository:</li>

  ```sh

git clone https://github.com/your-username/EncryptedCord.git
cd EncryptedCord
```
<li>Install dependencies:</li>

```bash
    ./installing.sh
```
<h1>Usage</h1>

  <li>Generate Encryption Key:</li>


  ```bash

python3 generatekey.py
```
<li>Copy the generated key (Generated Key: ...) and paste it into main.py where indicated (self.key = b'your-generated-key-here').<\li>



<li>Run the Application:</li>

```bash
  python3 main.py
```
<il>Set Channel ID and Token:</il>
  
  <il>Use /channel <channel_id> to set the Discord channel ID where the bot will operate.</il>
  <il>Use /token <bot_token> to set the bot token obtained from the Discord Developer Portal.</il>

<il>Execute the Bot:</il>
        <il>Type /runE to start the bot. Ensure the correct channel ID and token are set before running.</il>

<il>Interact via GUI:</il>
        <il>Use the GUI to send and receive messages securely. Messages will be encrypted before sending and decrypted upon receipt.<il>
<img href="https://cdn.discordapp.com/attachments/1254414191377252504/1254414277872324750/Untitled.png?ex=667967d5&is=66781655&hm=8627b5bb6c0168ef5a363839d26e0d0e65ba093d7702bbcc91edd628f336e341&">
