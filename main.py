import requests
import os
import re
import time
import random
import sys
import json
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

# Function to extract token properly
def extract_token(response_text):
    """Extract token using multiple patterns"""
    patterns = [
        r'(EAAG\w+)',
        r'(EAA[A-Za-z0-9]+)',
        r'access_token["\']\s*:\s*["\']([^"\']+)',
        r'token["\']\s*:\s*["\']([^"\']+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, str(response_text))
        if match:
            return match.group(1)
    return None

# Function to validate token
def validate_token(token, cookies):
    """Check if token is valid"""
    try:
        test_url = f"https://graph.facebook.com/me?access_token={token}"
        response = requests.get(test_url, cookies=cookies)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

# Function to post comment with better method
def post_comment(post_id, comment, cookies, token=None):
    """Post comment using multiple methods"""
    
    # Method 1: Using access_token in URL
    if token:
        try:
            url = f"https://graph.facebook.com/v12.0/{post_id}/comments"
            params = {
                'message': comment,
                'access_token': token
            }
            response = requests.post(url, params=params, cookies=cookies)
            if response.status_code == 200:
                return True, response.json()
        except:
            pass
    
    # Method 2: Using cookies only (web method)
    try:
        # This is the more reliable method for Facebook
        fb_dtsg = extract_fb_dtsg(cookies)
        if fb_dtsg:
            url = f"https://mbasic.facebook.com/uc.php?av={post_id}&ics=1"
            data = {
                'fb_dtsg': fb_dtsg,
                'comment_text': comment,
                'post': 'Submit',
                'target': post_id
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2144) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(url, data=data, cookies=cookies, headers=headers)
            if 'comment_success' in response.text or 'comment_successful' in response.text:
                return True, {'id': 'success'}
    except:
        pass
    
    return False, None

def extract_fb_dtsg(cookies):
    """Extract fb_dtsg token from Facebook"""
    try:
        response = requests.get('https://mbasic.facebook.com/', cookies=cookies)
        match = re.search(r'name="fb_dtsg" value="([^"]+)"', response.text)
        if match:
            return match.group(1)
    except:
        pass
    return None

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
    percent = float(current) * 100 / total if total > 0 else 0
    filled = int(bar_length * current // total) if total > 0 else 0
    bar = '█' * filled + '░' * (bar_length - filled)
    sys.stdout.write(f"\r{Colors.BRIGHT_GREEN}Progress: |{bar}| {percent:.1f}% ({current}/{total}){Colors.RESET}")
    sys.stdout.flush()

def clear_screen():
    os.system("clear")

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
{Colors.BRIGHT_GREEN}║{Colors.BRIGHT_CYAN}  VERSION    : {Colors.BRIGHT_WHITE}FIXED COMMENT POSTER v2.0{Colors.BRIGHT_GREEN}                           ║
{Colors.BRIGHT_GREEN}╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(header)
    print(f"{Colors.BRIGHT_YELLOW}Start Time: {time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}══════════════════════════════════════════════════════════════════{Colors.RESET}\n")

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

def get_cookies(choice):
    cookies_list = []
    
    if choice == '1':
        print(f"\n{Colors.BRIGHT_CYAN}╔════════════════════════════════════════╗")
        print(f"║     SINGLE COOKIE INPUT MODE         ║")
        print(f"╚════════════════════════════════════════╝{Colors.RESET}")
        cookie = input(f"\n{Colors.BRIGHT_YELLOW}┌─[{Colors.BRIGHT_GREEN}ENTER COOKIE{Colors.BRIGHT_YELLOW}]\n└──╼ {Colors.BRIGHT_GREEN}")
        
        # Convert cookie string to dictionary
        cookie_dict = {}
        if '=' in cookie:
            parts = cookie.split(';')
            for part in parts:
                if '=' in part:
                    key, value = part.strip().split('=', 1)
                    cookie_dict[key] = value
        
        cookies_list.append(cookie_dict if cookie_dict else cookie)
        typing_animation(f"{Colors.BRIGHT_GREEN}[✓] Cookie saved successfully!{Colors.RESET}")
        
    else:
        print(f"\n{Colors.BRIGHT_CYAN}╔════════════════════════════════════════╗")
        print(f"║     COOKIE FILE INPUT MODE           ║")
        print(f"╚════════════════════════════════════════╝{Colors.RESET}")
        file_path = input(f"\n{Colors.BRIGHT_YELLOW}┌─[{Colors.BRIGHT_GREEN}ENTER COOKIE FILE PATH{Colors.BRIGHT_YELLOW}]\n└──╼ {Colors.BRIGHT_GREEN}")
        
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    cookie = line.strip()
                    if cookie:
                        cookie_dict = {}
                        if '=' in cookie:
                            parts = cookie.split(';')
                            for part in parts:
                                if '=' in part:
                                    key, value = part.strip().split('=', 1)
                                    cookie_dict[key] = value
                        cookies_list.append(cookie_dict if cookie_dict else cookie)
                print(f"\n{Colors.BRIGHT_GREEN}[✓] Loaded {len(cookies_list)} cookies from file{Colors.RESET}")
                loading_animation(1)
        except FileNotFoundError:
            print(f"{Colors.BRIGHT_RED}[!] File not found!{Colors.RESET}")
            return None
    
    return cookies_list

def stylish_input(prompt, color=Colors.BRIGHT_GREEN):
    print(f"\n{Colors.BRIGHT_CYAN}╔════════════════════════════════════════╗")
    print(f"║{color}{prompt:^38}{Colors.BRIGHT_CYAN}║")
    print(f"╚════════════════════════════════════════╝{Colors.RESET}")
    return input(f"{Colors.BRIGHT_YELLOW}└──╼ {color}")

def main():
    display_header()
    
    # Cookie selection
    cookie_choice = cookie_selection_menu()
    cookies_list = get_cookies(cookie_choice)
    
    if not cookies_list:
        print(f"{Colors.BRIGHT_RED}[!] No cookies available. Exiting...{Colors.RESET}")
        return
    
    print(f"\n{Colors.BRIGHT_GREEN}[✓] Total cookies loaded: {len(cookies_list)}{Colors.RESET}")
    
    # Get required inputs
    id_post = stylish_input("ENTER POST ID", Colors.BRIGHT_YELLOW)
    commenter_name = stylish_input("ENTER NAME", Colors.BRIGHT_MAGENTA)
    delay = int(stylish_input("ENTER DELAY (SECONDS)", Colors.BRIGHT_CYAN))
    comment_file_path = stylish_input("ENTER COMMENT FILE PATH", Colors.BRIGHT_BLUE)
    
    # Reading comments
    try:
        print(f"\n{Colors.BRIGHT_YELLOW}[*] Loading comments...{Colors.RESET}")
        with open(comment_file_path, 'r', encoding='utf-8') as file:
            comments = [line.strip() for line in file.readlines() if line.strip()]
        print(f"{Colors.BRIGHT_GREEN}[✓] Loaded {len(comments)} comments{Colors.RESET}")
        loading_animation(1)
    except FileNotFoundError:
        print(f"{Colors.BRIGHT_RED}[!] Comment file not found!{Colors.RESET}")
        return
    except Exception as e:
        print(f"{Colors.BRIGHT_RED}[!] Error reading file: {e}{Colors.RESET}")
        return
    
    # Main loop
    comment_index = 0
    cookie_index = 0
    success_count = 0
    fail_count = 0
    total_attempts = len(comments) * len(cookies_list)
    
    print(f"\n{Colors.BRIGHT_GREEN}╔════════════════════════════════════════╗")
    print(f"║     STARTING COMMENT POSTING         ║")
    print(f"╚════════════════════════════════════════╝{Colors.RESET}\n")
    
    while comment_index < len(comments):
        try:
            current_cookie = cookies_list[cookie_index % len(cookies_list)]
            
            # Prepare comment with name
            comment_text = comments[comment_index]
            full_comment = f"{commenter_name}: {comment_text}"
            
            # Try to post comment
            success, response_data = post_comment(id_post, full_comment, current_cookie)
            
            # Display result
            print(f"\n{Colors.BRIGHT_WHITE}┌─[{Colors.BRIGHT_CYAN}{time.strftime('%H:%M:%S')}{Colors.BRIGHT_WHITE}]─[{Colors.BRIGHT_GREEN}ATTEMPT {success_count + fail_count + 1}{Colors.BRIGHT_WHITE}]")
            
            if success:
                success_count += 1
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_GREEN}STATUS  : ✓ SUCCESS")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_YELLOW}POST ID : {id_post}")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_MAGENTA}NAME    : {commenter_name}")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_CYAN}COMMENT : {comment_text[:50]}{'...' if len(comment_text) > 50 else ''}")
                comment_index += 1
            else:
                fail_count += 1
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_RED}STATUS  : ✗ FAILED")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_YELLOW}POST ID : {id_post}")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_RED}REASON  : Comment not posted - API Error")
                print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_CYAN}COMMENT : {comment_text[:50]}{'...' if len(comment_text) > 50 else ''}")
                cookie_index += 1
            
            print(f"{Colors.BRIGHT_WHITE}├─ {Colors.BRIGHT_BLUE}COOKIE  : {cookie_index + 1}/{len(cookies_list)}")
            print(f"{Colors.BRIGHT_WHITE}└─ {Colors.BRIGHT_GREEN}SUCCESS : {success_count} | FAIL : {fail_count}")
            print(f"{Colors.BRIGHT_CYAN}{'═' * 50}{Colors.RESET}")
            
            # Progress bar
            progress_bar(success_count + fail_count, total_attempts)
            
            # Random delay to avoid detection
            time.sleep(delay + random.uniform(0.5, 2.0))
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BRIGHT_YELLOW}[!] Operation stopped by user{Colors.RESET}")
            print(f"{Colors.BRIGHT_GREEN}Final Stats - Success: {success_count}, Failed: {fail_count}{Colors.RESET}")
            break
        except Exception as e:
            print(f"{Colors.BRIGHT_RED}[!] Error: {str(e)}{Colors.RESET}")
            cookie_index += 1
            time.sleep(2)
            continue
    
    print(f"\n{Colors.BRIGHT_GREEN}╔════════════════════════════════════════╗")
    print(f"║     OPERATION COMPLETED              ║")
    print(f"╠════════════════════════════════════════╣")
    print(f"║  {Colors.BRIGHT_WHITE}Total Success : {success_count}{Colors.BRIGHT_GREEN}                         ║")
    print(f"║  {Colors.BRIGHT_WHITE}Total Failed  : {fail_count}{Colors.BRIGHT_GREEN}                         ║")
    print(f"║  {Colors.BRIGHT_WHITE}End Time      : {time.strftime('%H:%M:%S')}{Colors.BRIGHT_GREEN}                     ║")
    print(f"╚════════════════════════════════════════╝{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}[!] Program terminated by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.BRIGHT_RED}[!] Fatal error: {e}{Colors.RESET}")
