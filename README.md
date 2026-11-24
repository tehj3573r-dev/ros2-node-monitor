# ros-node-monitor

A lightweight, terminal-based ROS 2 diagnostic monitor developed as part of the LAMEAN rover project.

## Overview

ROS Monitor provides a live overview of the ROS 2 communication graph. It discovers active nodes and topics, identifies message types, displays publishers and subscribers, and measures message activity across discovered topics.

The aim is to create a simple, readable diagnostic tool for understanding what is happening inside a ROS 2 system without needing a graphical visualisation tool.

## Current Features

- **Node discovery** – lists nodes currently visible in the ROS 2 network.
- **Topic discovery** – dynamically identifies available topics.
- **Message type identification** – displays the ROS 2 message type associated with each topic.
- **Publisher and subscriber information** – shows the number of publishers and subscribers for each topic.
- **Topic subscriptions** – dynamically creates subscriptions using the message type advertised by each discovered topic.
- **Message rate monitoring** – counts incoming messages and calculates an approximate message rate in Hz (messages per second).
- **Topic activity status** – identifies topics as ACTIVE or QUIET based on their observed message rate.
- **Topic details** – provides a breakdown of each topic, including its type, publishers and subscribers.

## Technical Details

- Python
- ROS 2
- `rclpy`
- `rosidl_runtime_py`

The monitor uses ROS 2 graph discovery to identify topics and dynamically loads their message types, allowing it to monitor different message types rather than being restricted to a single message type such as `std_msgs/msg/String`.

Message rates are currently calculated over a two-second monitoring interval.

## Project Status

**Development / Experimental**

The core discovery and monitoring functions are operational. Further development will focus on improving presentation, handling multiple monitor instances, and refining topic activity reporting.

## Project Context

This tool is being developed for LAMEAN, a Raspberry Pi-based tracked rover and robotics development platform.

The longer-term objective is to provide a compact diagnostic display for observing ROS 2 nodes, communications and system activity during rover development.
