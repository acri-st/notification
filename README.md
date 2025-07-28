# Notification

📌 [DESP-AAS Collaborative Services Parent Repository](https://github.com/acri-st/DESP-AAS-Collaborative-Services)

## Table of Contents

- [Introduction](#Introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Development](#development)
- [Contributing](#contributing)

## Introduction

### What is the Notification microservice?

The Notification microservice is a dedicated service responsible for handling all notification-related operations within the system. It provides a centralized solution for sending various types of notifications including emails, SMS, and push notifications.

**Key Features:**
- **Email Notifications**: Sends transactional and marketing emails
- **Queue-based Processing**: Uses RabbitMQ for reliable message handling
- **Scalable Architecture**: Designed to handle high-volume notification requests
- **Template Support**: Supports customizable notification templates
- **Delivery Tracking**: Monitors notification delivery status


The microservice operates independently, ensuring that notification failures don't impact other system components while providing reliable delivery mechanisms for critical communications.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Git** 
- **Docker** Docker is mainly used for the test suite, but can also be used to deploy the project via docker compose
- **RabbitMQ** for listening to a queue giving the mails to send

## Installation

1. Clone the repository:
```bash
git clone https://github.com/acri-st/notification.git notification
cd notification
```

## Development

## Development Mode

### Standard local development

Setup environment
```bash
make setup
```

To clean the project and remove node_modules and other generated files, use:
```bash
make clean
```

## Contributing

Check out the **CONTRIBUTING.md** for more details on how to contribute.
