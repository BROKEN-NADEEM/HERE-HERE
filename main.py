import requests
import os
import re
import time
import random
import sys
from requests.exceptions import RequestException

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# Animation functions
def typing_animation(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(duration=2):
    animation = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", 
                 "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]",
                 "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", 
                 "[■■■■■■■■■■]"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Colors.BRIGHT_CYAN}Loading {animation[i % len(animation)]}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print()

def progress_bar(current, total, bar_length=40):
    percent = float(current) * 100 / total
    arrow = '-' * int(percent/100 * bar_length - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f"\r{Colors.BRIGHT_GREEN}Progress: [{arrow}{spaces}] {percent:.2f}%{Colors.RESET}")
    sys.stdout.flush()

# Function to clear screen with animation
def clear_screen():
    print(f"{Colors.BRIGHT_YELLOW}Clearing screen", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    time.sleep(0.3)
    os.system("clear")

# Function to display stylish header
def display_header():
    clear_screen()
    header = f"""
{Colors.BRIGHT_GREEN}╔══════════════════════════════════════════════════════════════════╗
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_YELLOW}  ██████╗ ██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗{Colors.BRIGHT_GREEN}      ║
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_YELLOW}  ██╔══██╗██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║{Colors.BRIGHT_GREEN}      ║
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_YELLOW}  ██████╔╝██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║{Colors.BRIGHT_GREEN}      ║
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_YELLOW}  ██╔══██╗██╔══██╗██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║{Colors.BRIGHT_GREEN}      ║
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_YELLOW}  ██████╔╝██║  ██║╚██████╔╝██║  ██╗███████╗██║ ╚████║{Colors.BRIGHT_GREEN}      ║
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_YELLOW}  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝{Colors.BRIGHT_GREEN}      ║
{Colors.BRIGHT_GREEN}╠══════════════════════════════════════════════════════════════════╣
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_CYAN}  OWNER     : {Colors.BRIGHT_WHITE}BROKEN NADEEM{Colors.BRIGHT_GREEN}                                        ║
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_CYAN}  GITHUB     : {Colors.BRIGHT_WHITE}BROKEN NADEEM{Colors.BRIGHT_GREEN}                                        ║
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_CYAN}  RULEX      : {Colors.BRIGHT_WHITE}COOKIES POST{Colors.BRIGHT_GREEN}                                         ║
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_CYAN}  FACEBOOK   : {Colors.BRIGHT_WHITE}PARDHAN KIING{Colors.BRIGHT_GREEN}                                        ║
{Colors.BRIGHT_GREEN}╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(header)
    typing_animation(f"{Colors.BRIGHT_GREEN}System initialized successfully!{Colors.RESET}", 0.02)
    print(f"{Colors.BRIGHT_YELLOW}Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}══════════════════════════════════════════════════════════════════{Colors.RESET}\n")

# Function to display cookie selection menu
def cookie_selection_menu():
    print(f"\n{Colors.BRIGHT_MAGENTA}╔════════════════════════════════════════╗")
    print(f"║     COOKIE SELECTION OPTIONS        ║")
    print(f"╠════════════════════════════════════════╣")
    print(f"║  {Colors.BRIGHT_GREEN}[1]{Colors.BRIGHT_WHITE} Single Cookie                      {Colors.BRIGHT_MAGENTA}║")
    print(f"║  {Colors.BRIGHT_GREEN}[2]{Colors.BRIGHT_WHITE} Cookie File (Multiple Cookies)     {Colors.BRIGHT_MAGENTA}║")
    print(f"╚════════════════════════════════════════╝{Colors.RESET}")
    
    while True:
        try:
            choice = input(f"\n{Colors.BRIGHT_YELLOW}┌─[{Colors.BRIGHT_GREEN}SELECT OPTION{Colors.BRIGHT_YELLOW}]─[{Colors.BRIGHT_CYAN}1-2{Colors.BRIGHT_YELLOW}]\n└──╼ {Colors.BRIGHT_GREEN}")
            if choice in ['1', '2']:
                return choice
            else:
                print(f"{Colors.BRIGHT_RED}[!] Invalid option! Please select 1 or 2{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.BRIGHT_RED}[!] Operation cancelled by user{Colors.RESET}")
            sys.exit(0)

# Function to get cookies based on selection
def get_cookies(choice):
    cookies_list = []
    
    if choice == '1':
        print(f"\n{Colors.BRIGHT_CYAN}╔════════════════════════════════════════╗")
        print(f"║     SINGLE COOKIE INPUT MODE         ║")
        print(f"╚════════════════════════════════════════╝{Colors.RESET}")
        cookie = input(f"\n{Colors.BRIGHT_YELLOW}┌─[{Colors.BRIGHT_GREEN}ENTER COOKIE{Colors.BRIGHT_YELLOW}]\n└──╼ {Colors.BRIGHT_GREEN}")
        cookies_list.append(cookie)
        typing_animation(f"{Colors.BRIGHT_GREEN}[✓] Cookie saved successfully!{Colors.RESET}")
        
    else:
        print(f"\n{Colors.BRIGHT_CYAN}╔════════════════════════════════════════╗")
        print(f"║     COOKIE FILE INPUT MODE           ║")
        print(f"╚════════════════════════════════════════╝{Colors.RESET}")
        file_path = input(f"\n{Colors.BRIGHT_YELLOW}┌─[{Colors.BRIGHT_GREEN}ENTER COOKIE FILE PATH{Colors.BRIGHT_YELLOW}]\n└──╼ {Colors.BRIGHT_GREEN}")
        
        try:
            with open(file_path, 'r') as file:
                cookies = file.readlines()
                cookies_list = [cookie.strip() for cookie in cookies if cookie.strip()]
                print(f"\n{Colors.BRIGHT_GREEN}[✓] Loaded {len(cookies_list)} cookies from file{Colors.RESET}")
                loading_animation(1)
        except FileNotFoundError:
            print(f"{Colors.BRIGHT_RED}[!] File not found! Switching to single cookie mode.{Colors.RESET}")
            cookie = input(f"\n{Colors.BRIGHT_YELLOW}┌─[{Colors.BRIGHT_GREEN}ENTER COOKIE MANUALLY{Colors.BRIGHT_YELLOW}]\n└──╼ {Colors.BRIGHT_GREEN}")
            cookies_list.append(cookie)
    
    return cookies_list

# Stylish input function
def stylish_input(prompt, color=Colors.BRIGHT_GREEN):
    print(f"\n{Colors.BRIGHT_CYAN}╔════════════════════════════════════════╗")
    print(f"║{color}{prompt:^38}{Colors.BRIGHT_CYAN}║")
    print(f"╚════════════════════════════════════════╝{Colors.RESET}")
    return input(f"{Colors.BRIGHT_YELLOW}└──╼ {color}")

# Main function
def main():
    display_header()
    
    # Cookie selection
    cookie_choice = cookie_selection_menu()
    cookies_list = get_cookies(cookie_choice)
    
    if not cookies_list:
        print(f"{Colors.BRIGHT_RED}[!] No cookies available. Exiting...{Colors.RESET}")
        return
    
    print(f"\n{Colors.BRIGHT_GREEN}[✓] Total cookies loaded: {len(cookies_list)}{Colors.RESET}")
    
    # Get required inputs with stylish formatting
    id_post = int(stylish_input("ENTER POST ID", Colors.BRIGHT_YELLOW))
    commenter_name = stylish_input("ENTER NAME", Colors.BRIGHT_MAGENTA)
    delay = int(stylish_input("ENTER DELAY (SECONDS)", Colors.BRIGHT_CYAN))
    comment_file_path = stylish_input("ENTER COMMENT FILE PATH", Colors.BRIGHT_BLUE)
    
    # Reading comments
    try:
        print(f"\n{Colors.BRIGHT_YELLOW}[*] Loading comments...{Colors.RESET}")
        with open(comment_file_path, 'r') as file:
            comments = [line.strip() for line in file.readlines() if line.strip()]
        print(f"{Colors.BRIGHT_GREEN}[✓] Loaded {len(comments)} comments{Colors.RESET}")
        loading_animation(1)
    except FileNotFoundError:
        print(f"{Colors.BRIGHT_RED}[!] Comment file not found!{Colors.RESET}")
        return
    
    # Main loop
    comment_index = 0
    cookie_index = 0
    success_count = 0
    fail_count = 0
    
    print(f"\n{Colors.BRIGHT_GREEN}╔════════════════════════════════════════╗")
    print(f"║     STARTING COMMENT POSTING         ║")
    print(f"╚════════════════════════════════════════╝{Colors.RESET}\n")
    
    while True:
        try:
            current_cookie = cookies_list[cookie_index % len(cookies_list)]
            
            # Get token
            response = make_request('https://business.facebook.com/business_locations', 
                                  headers={'Cookie': current_cookie,
                                          'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2144 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/375.1.0.28.111;]'},
                                  cookies={'Cookie': current_cookie})
            
            if response is None:
                cookie_index += 1
                continue
                
            token_eaag = re.search('(EAAG\w+)', str(response))
            if not token_eaag:
                print(f"{Colors.BRIGHT_RED}[!] Invalid cookie! Skipping...{Colors.RESET}")
                cookie_index += 1
                continue
                
            token_eaag = token_eaag.group(1)
            
            # Prepare and post comment
            comment_text = comments[comment_index % len(comments)]
            full_comment = f"{commenter_name}: {comment_text}"
            
            data = {
                'message': full_comment,
                'access_token': token_eaag
            }
            
            response2 = requests.post(f'https://graph.facebook.com/{id_post}/comments/', 
                                    data=data, 
                                    cookies={'Cookie': current_cookie}).json()
            
            # Display result with stylish formatting
            print(f"{Colors.BRIGHT_WHITE}┌─[{Colors.BRIGHT_CYAN}{time.strftime('%H:%M:%S')}{Colors.BRIGHT_WHITE}]─[{Colors.BRIGHT_GREEN}RESULT{Colors.BRIGHT_WHITE}]")
            
            if 'id' in str(response2):
                success_count += 1
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_GREEN}STATUS  : SUCCESS")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_YELLOW}POST ID : {id_post}")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_MAGENTA}NAME    : {commenter_name}")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_CYAN}COMMENT : {comment_text[:50]}{'...' if len(comment_text) > 50 else ''}")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_BLUE}COOKIE  : {cookie_index + 1}/{len(cookies_list)}")
                print(f"{Colors.BRIGHT_WHITE}└─ {Colors.BRIGHT_GREEN}SUCCESS : {success_count} | FAIL : {fail_count}")
                comment_index += 1
            else:
                fail_count += 1
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_RED}STATUS  : FAILED")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_YELLOW}POST ID : {id_post}")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_MAGENTA}NAME    : {commenter_name}")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_CYAN}COMMENT : {comment_text[:50]}{'...' if len(comment_text) > 50 else ''}")
                print(f"{Colors.BRIGHT_WHITE}└─ {Colors.BRIGHT_RED}SUCCESS : {success_count} | FAIL : {fail_count}")
                cookie_index += 1
            
            print(f"{Colors.BRIGHT_CYAN}{'═' * 50}{Colors.RESET}")
            
            # Progress bar
            total_comments = len(comments) * 2  # Arbitrary total for demo
            progress_bar(success_count + fail_count, total_comments)
            
            time.sleep(delay)
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_YELLOW}[!] Operation stopped by user{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}Final Stats - Success: {success_count}, Failed: {fail_count}{Colors.RESET}")
            break
        except Exception as e:
            print(f"{Colors.BRIGHT_RED}[!] Error: {str(e)[:50]}{Colors.RESET}")
            cookie_index += 1
            time.sleep(2)
            continue

def make_request(url, headers, cookies):
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        return response.text
    except RequestException as e:
        print(f"{Colors.BRIGHT_RED}[!] Request error: {e}{Colors.RESET}")
        return None

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}[!] Program terminated by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}[!] Fatal error: {e}{Colors.RESET}")
