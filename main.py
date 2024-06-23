import discord
from discord.ext import commands
import asyncio
import threading
import tkinter as tk
from cryptography.fernet import Fernet
from tkinter import scrolledtext


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  # Ensure the bot can read message history
bot = commands.Bot(command_prefix='!', intents=intents)
global tokenl
class DiscordBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EncryptedCord")
        self.root.configure(bg="black")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="black", fg="lime", font=("Courier", 10))
        self.text_area.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.text_area.tag_configure("mention", background="yellow", foreground="black")
        self.text_area.tag_configure("everyone", background="red", foreground="white")
        self.command_entry = tk.Entry(root, bg="black", fg="lime", insertbackground='lime', font=("Courier", 10))
        self.command_entry.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        self.command_entry.bind('<Return>', self.process_command)
        self.entry = tk.Text(root, height=5, bg="black", fg="lime", insertbackground='lime', font=("Courier", 10))
        self.entry.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        self.entry.bind('<Shift-Return>', self.add_new_line)
        self.entry.bind('<Return>', self.send_message)
        self.entry.config(state='disabled')
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.channel_id = None
        self.bot_thread = None
        self.write_to_text_area("If the screen has nothing or is frozen, this means that you entered the wrong commands so you need to restart the app\n")
        self.key = b'your-generated-key-here' #<<<<<< put the key here
    
    def add_new_line(self, event):
        self.entry.insert(tk.END, '\n')
        return 'break'
    def process_command(self, event):
        command = self.command_entry.get().strip()
        self.command_entry.delete(0, tk.END)
        if command.startswith("/channel "):
            try:
                self.channel_id = int(command.split()[1])
                self.write_to_text_area(f"Channel ID set to {self.channel_id}\n")
            except ValueError:
                self.write_to_text_area("Invalid channel ID.\n")
        elif command.startswith("/token "):
            try:
                self.tokenl = str(command.split()[1])
                self.write_to_text_area(f"Token set to {self.tokenl}\n")
            except ValueError as e:
                self.write_to_text_area(e)           
        elif command == "/runE":
            if self.channel_id and self.tokenl:
                self.command_entry.config(state='disabled')
                self.entry.config(state='normal')
                try:
                    self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
                    self.bot_thread.start()
                except:
                    print("Invalid token or Invalid Channel ID")
            else:
                self.write_to_text_area("Please set a channel ID or token before running the bot.\n")
    def run_bot(self):
        @bot.event
        async def on_ready():
            self.write_to_text_area(f'Logged in as {bot.user.display_name}\n------\n')
            channel = bot.get_channel(self.channel_id)
            if channel:
                await load_history(channel)
            else:
                self.write_to_text_area(f"Channel with ID {self.channel_id} not found.\n")
        async def load_history(channel):
            messages = []
            cipher_suite = Fernet(self.key)
            async for message in channel.history(limit=4500):
                try:
                    decrypted_content = cipher_suite.decrypt(message.content.encode()).decode()
                    messages.append(f"{message.author}: {decrypted_content}")
                except Exception as e:
                    print(f"Failed to decrypt message from {message.author}: {str(e)}")
            for message in reversed(messages):
                self.write_to_text_area(f"{message}\n")
        @bot.event
        async def on_message(message):
            cipher_suite = Fernet(self.key)
            decrypted_message = cipher_suite.decrypt(message.content.encode()).decode()
            self.write_to_text_area(f'{message.author}: {decrypted_message}\n')
            await bot.process_commands(message)
        bot.run(self.tokenl)
    def write_to_text_area(self, message):
        self.text_area.config(state='normal')
        start_index = self.text_area.index(tk.END)
        self.text_area.insert(tk.END, message)
        bot_user_name = bot.user.name if bot.user else None
        if bot_user_name:
            mention = f"@{bot_user_name}"
            start_pos = message.find(mention)
            while start_pos != -1:
                end_pos = start_pos + len(mention)
                start_index = f"{int(self.text_area.index('end-1c').split('.')[0]) - 1}.{start_pos}"
                end_index = f"{int(self.text_area.index('end-1c').split('.')[0]) - 1}.{end_pos}"
                self.text_area.tag_add("mention", start_index, end_index)
                start_pos = message.find(mention, end_pos)
        everyone_pos = message.find("@everyone")
        while everyone_pos != -1:
            end_pos = everyone_pos + len("@everyone")
            start_index = f"{int(self.text_area.index('end-1c').split('.')[0]) - 1}.{everyone_pos}"
            end_index = f"{int(self.text_area.index('end-1c').split('.')[0]) - 1}.{end_pos}"
            self.text_area.tag_add("everyone", start_index, end_index)
            everyone_pos = message.find("@everyone", end_pos)
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')
    def send_message(self, event):
        message = self.entry.get("1.0", tk.END).strip()
        if message and self.channel_id:
            cipher_suite = Fernet(self.key)
            encrypted_message = cipher_suite.encrypt(message.encode())
            asyncio.run_coroutine_threadsafe(bot.get_channel(self.channel_id).send(encrypted_message.decode()), bot.loop)
            self.entry.delete("1.0", tk.END)
        return 'break'
if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordBotApp(root)
    root.mainloop()
