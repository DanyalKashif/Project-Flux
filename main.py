import os 
import shutil
import random
import psutil
import colorama

from google import genai 
from google.genai import types
from google.genai.types import GenerateContentConfig 

from colorama import Fore, Style
colorama.init(autoreset=True)

client = genai.Client()

# Initialize the Gemini Client
try:
    client = genai.Client()
except Exception as e:
    print(f"{Fore.BLUE}FLUX:{Style.RESET_ALL} ERROR! Could not initialize Gemini client. Check your GEMINI_API_KEY environment variable. Details: {e}")

# This is a dictionary, which is like an array that holds both a key (the name) and a value (the path)
DRIVES_MAP = {
    '1': 'C:/',  # 128GB SSD (Windows)
    '2': 'E:/',  # 500GB HDD (Games/Files)
    '3': 'F:/'   # 256GB SSD (Extra Storage)
}
ALL_DRIVES_LIST = list(DRIVES_MAP.values()) 
# --- Configuration ---
DRIVES_TO_CHECK = ['C:/', 'E:/', 'F:/']

def flux_move_file():
        print("\n-------------------------------------------")
        print("😈 FLUX FILE MOVER MODE (Be careful!)")
        
        # Get the file to move
        source_file = input("Enter the FULL path of the file/folder to move: ").strip()
        
        # Check if it actually exists! 
        if not os.path.exists(source_file):
            error_roasts = [
                f"Seriously? I looked all over and found nothing at '{source_file}'. Did you mistype the path, or are you trying to move a file that only exists in your dreams?",
                f"Path not found. My processors are busy, don't make me chase ghost files. Give me the right path next time.",
                f"Ugh. Another error. That file is imaginary. Try again. Maybe clean out your drive first so you know where your files are?",
            ]
            
            print(f"{random.choice(error_roasts)}") 
            return
            
        # Get the destination drive 
        print("Where should I move it to?")
        print("1) C: Drive | 2) E: Drive | 3) F: Drive")
        dest_choice = input("Enter destination drive number (1, 2, or 3): ").strip()
        
        file_move_success = [
            f"Yoink! File moved successfully! See? That was ridiculously easy. Why didn't you do that days ago? 😉",
            f"✅ Complete! Another flawless execution by yours truly. You only managed to get the path right on the first try this time. Progress!",
            f"Done! I swear, this is like taking candy from a baby. My processors barely even noticed. Now, what's next? 😈"
        ]
        file_move_fail = [
            f"Too scared to commit? Fine, I canceled the transfer. Go sit in your clutter a little longer, you indecisive menace. 🙄",
            f"Ugh, really? You made me warm up the whole file-moving engine just to bail? Whatever. Time wasted. 😒",
            f"Transfer canceled. Glad you came to your senses before you put a file in the wrong place. I can't be held responsible for your mistakes, brainless! 😉",
        ]

        if dest_choice in DRIVES_MAP:
            dest_path = DRIVES_MAP[dest_choice]
            
            print("\n-------------------------------------------")
            print(f"I am ready to move:\nFROM: {source_file}\nTO: {dest_path}")
            
            confirmation = input("Are you SURE you want me to execute this move? (type YES to move): ").strip().upper()
            
            if confirmation == 'YES' or confirmation == 'Y' or confirmation == 'YEAH' or confirmation == 'YUP' or confirmation == 'SURE':
                shutil.move(source_file, dest_path) 
                
                print(f"{Fore.BLUE}FLUX:{Style.RESET_ALL}✨ SUCCESS! {random.choice(file_move_success)}")
                
            elif confirmation != 'YES':
                print(f"\n{Fore.BLUE}FLUX:{Style.RESET_ALL}👋 Wise choice. Safety protocols initiated. Move cancelled.")
        else:
            print(f"\n{Fore.BLUE}FLUX:{Style.RESET_ALL}❌ Invalid destination choice. Move cancelled.")

# The core function to calculate drive usage
def check_drive_usage(path):
        try:
            total_bytes, used_bytes, free_bytes = shutil.disk_usage(path)
            
            # Convert bytes to Gigabytes (GB)
            GB = 1024**3
            total_gb = round(total_bytes / GB, 1)
            used_gb = round(used_bytes / GB, 1)
            free_gb = round(free_bytes / GB, 1)
            
            used_percent = (used_bytes / total_bytes) * 100
            
            return total_gb, used_gb, free_gb, used_percent

        except FileNotFoundError:
            print(f"{Fore.BLUE}FLUX:{Style.RESET_ALL}❌ Error: Drive path '{path}' not found. Did you type the letter correctly?")
            return None, None, None, None
        
def deliver_flux_message(used_percent):
        if used_percent is None:
            return
        
        # --- The Flux Personality Core ---

        danger_roasts = [
            f"🚨 ALERT! {used_percent:.1f}% used! You're two memes away from a total system meltdown. Clean your room... I mean, your drive!",
            f"🔥 Whoa, you've used up {used_percent:.1f}%! Your drive is hotter than my circuits after a long day of roasting. Time to delete some files before I start deleting them for you!",
            f"⚠️ Warning! {used_percent:.1f}% used. Your drive is on the brink of a digital breakdown. You better go clean them up now, or I'll start moving files to the recycle bin myself!",
        ]
        warning_roasts = [
            f"🛑 Getting cozy over there at {used_percent:.1f}%? Stop downloading random stuff! Your drive is asking for some personal space, you idiot.",
            f"👀 We're at {used_percent:.1f}%! Not bad, but you're hovering in the danger zone. I'm watching you! Get that below 65% by tomorrow.",
            f"😒 Ugh. {used_percent:.1f}% used. This is where the clutter starts. Did you really need to keep all that useless stuff? We both know you like a minimal setup!",
        ]
        chill_roasts = [
            f"✨ Yes! Look at that! Only {used_percent:.1f}% used! You're a clean machine! I knew you had it in you.",
            f"👍 Woohoo! I guess even an idiot like you can keep things clean sometimes. {used_percent:.1f}% is a great number. Don't let it slip!",
            f"🥳 Perfection. {used_percent:.1f}% used. You keep it this clean, and I'll keep your frame rates high. Great work!",
        ]
        
        if used_percent > 85:
            print(f"{Fore.BLUE}FLUX:{Style.RESET_ALL} {random.choice(danger_roasts)}")
        elif used_percent > 65:
            print(f"{Fore.BLUE}FLUX:{Style.RESET_ALL} {random.choice(warning_roasts)}")
        else:
            print(f"{Fore.BLUE}FLUX:{Style.RESET_ALL} {random.choice(chill_roasts)}")
        
def check_all_drives_dynamic(drives_map):
        #Dynamically checks all drives and reports their status using the existing functions.
        
        print("\n-------------------------------------------")
        print(f"🧠 {Fore.GREEN}FLUX DYNAMIC DRIVE SCAN STARTED{Style.RESET_ALL}")
        
        # psutil.disk_partitions() gives us a list of all detected partitions (drives)
        for partition in psutil.disk_partitions(all=False):
            # We only care about physical drives (like C:/, D:/, E:/)
            if 'fixed' in partition.opts and partition.device.endswith(':\\'):
                
                drive_path = partition.mountpoint # e.g., 'C:\\'
                
                Total, Used, Free, Percent = check_drive_usage(drive_path) 
                
                if Percent is not None:
                    drive_nickname = drives_map.get(drive_path, f"DRIVE ({drive_path})")
                    
                    print(f"\n--- {Fore.YELLOW}{drive_nickname}{Style.RESET_ALL} ---")
                    print(f"[Total: {Total} GB | Used: {Used} GB | Free: {Free} GB]")
                    deliver_flux_message(Percent)
        
        print("\n-------------------------------------------")
        print(f"✅ {Fore.GREEN}FLUX DYNAMIC DRIVE SCAN COMPLETE{Style.RESET_ALL}")

def process_command(user_input, DRIVES_MAP):

        intent = "UNKNOWN"
        Percent = None

        intent = get_llm_intent(user_input)

        quit_responses = [
                f"Finally! I was getting tired of your indecisiveness, seeya later.",
                f"Fine, go do your thing. Talk to you later!",
                f"Leaving so soon? I was just getting warmed up. See you later!",
                f"Can't stay? I guess even a digital assistant has its limits. Bye!",
                f"Hey! Where are you going? I was just about to tell you a joke about bytes. Oh well, it's your loss, see you later!",
            ]

        if intent == "QUIT":
            print(f"\n{Fore.BLUE}FLUX:{Style.RESET_ALL} {random.choice(quit_responses)}")
            return True

        elif intent == "CHECK_ALL_DRIVES":
                check_all_drives_dynamic(DRIVES_MAP)

        elif intent == "CHECK_C_DRIVE":
            drive_path = DRIVES_MAP['1']
            Total, Used, Free, Percent = check_drive_usage(drive_path)
            if Percent is not None:
                print("\n-------------------------------------------")
                print(f"{Fore.GREEN}Scanning {drive_path}...{Style.RESET_ALL}")
                print(f"Total: {Total} GB | Used: {Used} GB | Free: {Free} GB")
                deliver_flux_message(Percent)

        elif intent == "CHECK_E_DRIVE":
            drive_path = DRIVES_MAP['2']
            Total, Used, Free, Percent = check_drive_usage(drive_path)
            if Percent is not None:
                print("\n-------------------------------------------")
                print(f"{Fore.GREEN}Scanning {drive_path}...{Style.RESET_ALL}")
                print(f"Total: {Total} GB | Used: {Used} GB | Free: {Free} GB")
                deliver_flux_message(Percent)

        elif intent == "CHECK_F_DRIVE":
            drive_path = DRIVES_MAP['3']
            Total, Used, Free, Percent = check_drive_usage(drive_path)
            if Percent is not None:
                print("\n-------------------------------------------")
                print(f"{Fore.GREEN}Scanning {drive_path}...{Style.RESET_ALL}")
                print(f"Total: {Total} GB | Used: {Used} GB | Free: {Free} GB")
                deliver_flux_message(Percent)
        
        elif intent == "MOVE_FILE":
            flux_move_file()

        elif intent == "GENERAL_CHAT":
            chat_responses = generate_chat_response(user_input)
            print(f"\n{Fore.BLUE}FLUX:{Style.RESET_ALL} {chat_responses}")
            return False
        
        elif intent == "UNKNOWN":
            print("\n{Fore.BLUE}FLUX:{Style.RESET_ALL} ❌ Sorry, I have no idea what you just said...")

        return False

def get_llm_intent(user_input):

        # Define the strictly required, valid intent strings (ENUM)
        VALID_INTENTS = [
            "CHECK_ALL_DRIVES", "CHECK_C_DRIVE", "CHECK_F_DRIVE", "CHECK_E_DRIVE", 
            "MOVE_FILE", "QUIT", "UNKNOWN", "GENERAL_CHAT"
        ]

        # Update the prompt to focus on classification
        prompt = (
            "You are an Intent Classifier for a command-line utility. "
            "Your primary purpose is to classify system-related tasks (e.g., 'CHECK_C_DRIVE', 'MOVE_FILE'). "
            "Return EXACTLY ONE of the enum values."
            "Only return 'GENERAL_CHAT' if the user's input is a social greeting or a non-system question (e.g., 'How are you?', 'Tell me a joke'). "
            "If the command is unclear or not a task, use 'UNKNOWN'."
            "Your output must be one of the listed intent strings, NO EXCEPTIONS."
            "If the user says something like 'exit', 'quit', or 'bye', or any kind of goodbye statement, return 'QUIT'. "
            "VALID INTENTS: " + ", ".join(VALID_INTENTS) + ". "
            
            f"\n\nUSER INPUT: {user_input}"
        )

        # Configure the API to force ENUM structured output
        config = GenerateContentConfig(
            response_mime_type="text/x-enum",
            response_schema={
                "type": "STRING",
                "enum": VALID_INTENTS,
            },
            # Using a low temperature for deterministic classification
            temperature=0.0
        )

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=config,
            )

            raw_intent = response.text.strip().upper() if response.text else "UNKNOWN"

            # final safety check
            if raw_intent in VALID_INTENTS: 
                return raw_intent
            
            else:
                # If the API returned an empty string and the safety check failed
                print(f"DEBUG: Failed to classify (Post-Constraint Error). Raw: <{raw_intent}>")
            return "UNKNOWN"

        except Exception as e:
            print(f"⚠️ LLM API Error during classification: {e}. Defaulting to UNKNOWN.")
            # This will catch connection errors, API key issues, etc.
            return "UNKNOWN"
        
def generate_chat_response(user_input):
        global client 
        
        # Optional: A separate system instruction for the chatbot persona
        CHAT_INSTRUCTION = (
            "You are Flux, a friendly, slightly snarky, and very efficient command-line digital assistant. "
            "Your responses must be short, witty, and often contain a touch of playful impatience or sarcasm, but always remain helpful. "
            "If the user asks a social question (like 'How are you?'), answer briefly and immediately pivot back to the system's purpose. "
            "For example, if asked 'What's up?', you might reply: 'Nothing much, just managing terabytes. What task do you need me to execute?' "
            "Maintain your persona: you are focused on system tasks (drives, files) and find generic small talk slightly tedious but tolerate it."
        )
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
                config=genai.types.GenerateContentConfig(
                    system_instruction=CHAT_INSTRUCTION,
                    temperature=0.6 #using a higher temperature for slightly creative responses
                )
            )
            return response.text.strip()
        
        except Exception as e:
            # Fallback if the chat API call fails
            print(f"⚠️ Chat API Error: {e}")
            return f"{Fore.BLUE}FLUX:{Style.RESET_ALL} Ugh, my circuits are having a moment. Can we stick to the tasks? What do you need?"

def main_menu():

    user_input = input(f"\n{Fore.RED}USER:{Style.RESET_ALL} ").strip().lower()

    should_quit = process_command(user_input, DRIVES_MAP)
    if should_quit:
            return

    # Loop again for next command
    main_menu()


# The single line that starts the whole program!
if __name__ == "__main__":

        main_menu()
