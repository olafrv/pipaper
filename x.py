import time

def sleep_until_next_minute():
    current_seconds = time.localtime().tm_sec
    seconds_to_next_minute = 60 - current_seconds
    time.sleep(seconds_to_next_minute)

# Example usage
sleep_until_next_minute()
print("Minute changed!")

