
# Project README

## Overview

This project demonstrates two architectural styles for processing messages in a distributed system: **Event-Driven System** using a **Message Broker (RabbitMQ)** and **Pipes-and-Filters** architecture. The system processes messages submitted by a user, applies filters, converts the message to uppercase, and sends an email notification using RabbitMQ for the event-driven approach, and separate processes for the pipes-and-filters approach.

### Architecture:
1. **Event-Driven System (Broker Topology)**:
   - The message flow uses **RabbitMQ** to pass messages between various services: an API service, a message filtering service, a transformation service (SCREAMING), and a publish service.
   - Services communicate through message queues in RabbitMQ.
   
2. **Pipes-and-Filters**:
   - Each service is deployed as a separate process where they directly interact through pipes or inter-process communication, without a message broker. This allows for a different method of orchestration.

## Running the System

To run the system in its **Event-Driven** architecture using RabbitMQ, simply execute the following script:

### 1. **Run the Event-Driven System**:

To start all the services in the event-driven setup (API server, filter service, screaming service, and publish service) with RabbitMQ as the message broker, execute:

```bash
python start_system.py
```

This will start all the necessary services concurrently in separate processes.

### 2. **Run Single App (Pipes-and-Filters)**:

If you want to run the system in **Pipes-and-Filters** architecture, where each service works independently without using RabbitMQ, you can run individual services. For instance:

- To start the API server:
  ```bash
  python app/app.py
  ```

### 3. **Send a Test Message**:

To test the system, you can send a sample message using the `test_system.py` script. This will trigger the API service to receive a POST request and pass the message through the system:

```bash
python test_system.py
```

This will simulate sending a test message with the alias "professor" and a message "Hello, this is a test message!", which will then go through the filtering, transformation, and publishing stages depending on the chosen architecture.

## Notes
- Make sure RabbitMQ is running locally for the event-driven architecture.
- For the pipes-and-filters architecture, each service should be run separately.
- The system handles processing for stop-words, message transformations (SCREAMING), and email notifications.

Make sure to install all required dependencies using:

```bash
pip install -r requirements.txt
```
