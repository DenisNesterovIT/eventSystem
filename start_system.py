import multiprocessing
import os
import subprocess

def run_api_service():
    # Replace with the actual command to run the Flask API service
    print(f"Running API Service in process {os.getpid()}")
    subprocess.run(["python", "./event_system/api_service/app.py"])

def run_filter_service():
    # Replace with the actual command to run the filter service
    print(f"Running Filter Service in process {os.getpid()}")
    subprocess.run(["python", "./event_system/filter_service/filter.py"])

def run_screaming_service():
    # Replace with the actual command to run the screaming service
    print(f"Running Screaming Service in process {os.getpid()}")
    subprocess.run(["python", "./event_system/screaming_service/screaming.py"])

def run_publish_service():
    # Replace with the actual command to run the publish service
    print(f"Running Publish Service in process {os.getpid()}")
    subprocess.run(["python", "./event_system/publish_service/publish.py"])

def main():
    # Create processes for each service
    processes = []

    # Start the API service
    p_api = multiprocessing.Process(target=run_api_service)
    processes.append(p_api)
    p_api.start()

    # Start the filter service
    p_filter = multiprocessing.Process(target=run_filter_service)
    processes.append(p_filter)
    p_filter.start()

    # Start the screaming service
    p_screaming = multiprocessing.Process(target=run_screaming_service)
    processes.append(p_screaming)
    p_screaming.start()

    # Start the publish service
    p_publish = multiprocessing.Process(target=run_publish_service)
    processes.append(p_publish)
    p_publish.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    print("All services are now running.")

if __name__ == "__main__":
    main()
