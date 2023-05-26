import multiprocessing
import tttkinter
import get_hand_gesture

if __name__ == "__main__":
    # Create two processes for running the two Python files
    process1 = multiprocessing.Process(target=)
    process2 = multiprocessing.Process(target=)

    # Start the processes
    process1.start()
    process2.start()

    # Wait for the processes to finish
    process1.join()
    process2.join()

    print("Main process: Child processes have finished.")
