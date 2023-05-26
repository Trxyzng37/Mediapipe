import multiprocessing
import subprocess

if __name__ == "__main__":
    # Create two queues for inter-process communication
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()

    # Create two processes for running the scripts
    print("Start GUI.......")
    process1 = multiprocessing.Process(target=subprocess.Popen, args=(["python", "tttkinter.py"],))
    print("Start hand.......")
    process2 = multiprocessing.Process(target=subprocess.Popen, args=(["python", "get_hand_gesture.py"],))

    # Start both processes
    process1.start()
    process2.start()

    # Wait for the GUI process to finish
    process1.join()

    # Terminate the hand gesture process
    process2.terminate()

    # Clean up the queue
    queue2.close()
    queue2.join_thread()

    print("GUI process finished")
