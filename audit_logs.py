import sqlite3

def view_logs():
    print(f"{'ID':<4} | {'Timestamp':<20} | {'Score':<5} | {'Decision':<8} | {'Prompt'}")
    print("-" * 80)
    
    with sqlite3.connect("lumen_proxy.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM security_logs ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        
        for row in rows:
            # row[0]=id, row[1]=timestamp, row[2]=prompt, row[3]=score, row[4]=decision
            print(f"{row[0]:<4} | {row[1]:<20} | {row[3]:<5} | {row[4]:<8} | {row[2]}")

if __name__ == "__main__":
    view_logs()
