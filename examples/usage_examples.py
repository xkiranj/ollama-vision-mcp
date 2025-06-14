"""
Example usage of Ollama Vision MCP tools
This demonstrates how the MCP tools work when integrated with a client
"""

# Example 1: Basic image description
"""
User: "Can you describe what's in the image at C:/Users/Photos/sunset.jpg?"

Assistant uses tool: analyze_image
Arguments: {
    "image_path": "C:/Users/Photos/sunset.jpg"
}

Response: "This image shows a beautiful sunset over the ocean. The sky is painted 
with vibrant oranges, pinks, and purples. The sun is partially visible on the 
horizon, creating a golden reflection on the calm water. In the foreground, there 
are silhouettes of palm trees swaying gently in the breeze."
"""

# Example 2: Object identification
"""
User: "What objects can you identify in my desktop screenshot?"

Assistant uses tool: identify_objects
Arguments: {
    "image_path": "C:/Users/Screenshots/desktop.png"
}

Response: 
"I can identify the following objects in the image:
• Computer monitor
• Keyboard
• Mouse
• Coffee mug
• Notebook and pen
• Desk lamp
• Several application windows
• Desktop icons
• Taskbar
• Clock widget"
"""

# Example 3: Text extraction
"""
User: "Can you read the text from this receipt image?"

Assistant uses tool: read_text
Arguments: {
    "image_path": "C:/Users/Documents/receipt.jpg"
}

Response:
"STORE NAME: TechMart
Date: 2024-01-15
Time: 14:32

Items:
- USB Cable 3.0 ......... $12.99
- Wireless Mouse ........ $24.99
- Screen Cleaner ........ $8.50

Subtotal: $46.48
Tax: $3.72
Total: $50.20

Thank you for shopping!"
"""

# Example 4: Custom analysis with specific prompt
"""
User: "Analyze this architecture diagram and explain the data flow"

Assistant uses tool: analyze_image
Arguments: {
    "image_path": "C:/Projects/architecture.png",
    "prompt": "Analyze this software architecture diagram and explain the data flow between components"
}

Response: "This architecture diagram shows a microservices-based system with the 
following data flow:

1. Client requests enter through the API Gateway
2. The Gateway routes requests to appropriate microservices
3. User Service handles authentication and user management
4. Order Service processes orders and communicates with Inventory Service
5. All services connect to their respective databases
6. A Message Queue (appears to be RabbitMQ) handles asynchronous communication
7. The Notification Service subscribes to events and sends emails/SMS

The architecture follows a typical event-driven pattern with clear separation 
of concerns between services."
"""

# Example 5: Analyzing image from URL
"""
User: "What's in this image? https://example.com/photos/mountain-landscape.jpg"

Assistant uses tool: describe_image
Arguments: {
    "image_path": "https://example.com/photos/mountain-landscape.jpg"
}

Response: "This breathtaking landscape photograph captures a majestic mountain 
range during golden hour. Snow-capped peaks rise dramatically against a clear 
blue sky, with the setting sun casting warm light on the mountain faces. In 
the foreground, there's a pristine alpine lake reflecting the mountains like 
a mirror. Pine trees line the lake's shore, and wildflowers in various colors 
dot the meadow. The composition suggests this was taken in late summer or 
early fall."
"""

# Example 6: Using different models
"""
User: "Use the most detailed model to analyze this complex technical diagram"

Assistant uses tool: analyze_image
Arguments: {
    "image_path": "C:/Work/circuit-diagram.png",
    "prompt": "Provide a detailed technical analysis of this circuit diagram",
    "model": "llava:13b"
}

Response: "This is a complex mixed-signal circuit diagram featuring:

Power Supply Section:
- Input voltage regulation using LM7805
- Filtering capacitors (100µF, 0.1µF)
- Protection diode (1N4007)

Microcontroller Section:
- ATmega328P microcontroller
- 16MHz crystal oscillator with 22pF load capacitors
- Reset circuit with pull-up resistor
- ISP programming header

Sensor Interface:
- Multiple analog inputs with RC filtering
- I2C pull-up resistors (4.7kΩ)
- SPI connections to external modules

Output Stage:
- Motor driver circuit using L293D
- LED indicators with current-limiting resistors
- Relay control with flyback diodes

The circuit appears designed for a sensor-based control system with both 
analog and digital I/O capabilities."
"""
