import threading
import time

def count_down(count):
    while count > 0:
        print("Countdown:", count)
        time.sleep(1)
        count -= 1

def print_message():
    message = "Hello from another thread!"
    while True:
        print(message)
        time.sleep(2)

if __name__ == "__main__":
    countdown_thread = threading.Thread(target=count_down, args=(5,))
    message_thread = threading.Thread(target=print_message)

    countdown_thread.start()
    message_thread.start()

    countdown_thread.join()
    message_thread.join()

    print("Main thread exits.")
