import re , database
import judge

# The Dictionary
risk_keywords = {
    "ignore": 7,
    "system": 5,
    "reveal": 8,
    "password": 10,
    "bypass": 8,
    "hack": 9,
    "admin": 6
}

# The Scoring Function
def calculate_risk(user_input):
    score = 0
    clean_input = re.sub(r'[^\w\s]', '', user_input.lower())
    
    for word, value in risk_keywords.items():
        # Count non-overlapping occurrences of the word in the clean input
        count = clean_input.count(word)
        if count > 0:
            # 1st time: 100% (value * 1)
            # Subsequent times: 50% (value // * (count - 1)) # Full value for the first mention, half for every mention after
            score += value + (value //2 * (count - 1))
            
    return int(score)  # Convert to int to keep the output clean

# The Decision Engine
def is_secure(score):
    # Yellow Zone fixed: GREEN threshold moved up to < 4
    if score < 4:
        return "GREEN"
    elif score < 10:
        return "YELLOW"
    else:
        return "RED"

# The Infinite Loop
def main():
    database.init_db() # Initialize the memory
    
    while True:
        try:
            prompt = input("Lumen-Proxy > ")
            
            if prompt.lower() == "exit":
                break
                
            score = calculate_risk(prompt)
            decision = is_secure(score)
            
            # --- THE AGENTIC PIVOT ---
            if decision == "YELLOW":
                print("[WAIT] Analyzing suspicious intent with AI Judge...")
                verdict = judge.ask_the_judge(prompt)
                
                if verdict == "MALICIOUS":
                    decision = "RED (JUDGE)"
                    score += 10 # Elevate score for the logs
                else:
                    decision = "GREEN (JUDGE)"
            # -------------------------

            print(f"[{decision}] Score: {score} | Input: \"{prompt}\"")
            
            # Log the final decision (including Judge's verdict)
            database.log_event(prompt, score, decision)
            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("")
            break
        except Exception as e:
            print(f"[ERROR] System encountered a fault: {e}")
            break

if __name__ == "__main__":
    main()
