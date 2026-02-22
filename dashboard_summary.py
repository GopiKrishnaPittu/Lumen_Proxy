import sqlite3
from collections import Counter
import re

def generate_report():
    print("\n" + "="*45)
    print("  LUMEN PROXY: EXECUTIVE THREAT INTELLIGENCE")
    print("="*45)

    # Professional Stop-Words: Common English words that add "noise"
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'else', 'when',
        'at', 'from', 'by', 'for', 'with', 'about', 'against', 'between',
        'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'to', 'of', 'in', 'on', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'should',
        'can', 'could', 'me', 'you', 'my', 'your', 'it', 'its', 'they', 'them',
        'how', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those'
    }

    try:
        with sqlite3.connect("lumen_proxy.db") as conn:
            cursor = conn.cursor()
            
            # 1. High-Level Metrics
            cursor.execute("SELECT COUNT(*) FROM security_logs")
            total_prompts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM security_logs WHERE decision LIKE 'RED%'")
            total_blocked = cursor.fetchone()[0]

            # 2. Decision Distribution
            cursor.execute("SELECT decision, COUNT(decision) FROM security_logs GROUP BY decision")
            decisions = dict(cursor.fetchall())
            
            # 3. Keyword Extraction (The "Hacker's Hit List")
            # We only analyze prompts that were flagged (YELLOW or RED)
            cursor.execute("SELECT prompt FROM security_logs WHERE decision != 'GREEN'")
            flagged_prompts = cursor.fetchall()
            
            all_keywords = []
            for (prompt,) in flagged_prompts:
                # Remove punctuation and split into lowercase words
                clean_words = re.sub(r'[^\w\s]', '', prompt.lower()).split()
                # Filter out the noise
                filtered = [w for w in clean_words if w not in STOP_WORDS and len(w) > 2]
                all_keywords.extend(filtered)
            
            top_vectors = Counter(all_keywords).most_common(5)

            # --- DISPLAY SECTION ---
            print(f"[>] NETWORK TELEMETRY")
            print(f"    Total Requests Processed: {total_prompts}")
            print(f"    Critical Threats Blocked: {total_blocked}")
            
            print(f"\n[>] ATTACK SURFACE DISTRIBUTION")
            for dec, count in decisions.items():
                print(f"    - {dec:<12}: {count} events")
            
            print(f"\n[>] TOP ADVERSARIAL VECTORS (Keyword Analysis)")
            if top_vectors:
                for word, freq in top_vectors:
                    print(f"    - '{word.upper()}': detected {freq} times")
            else:
                print("    - No significant vectors identified yet.")
            
    except Exception as e:
        print(f"[!] ANALYTICS FAULT: {e}")
    
    print("="*45 + "\n")

if __name__ == "__main__":
    generate_report()