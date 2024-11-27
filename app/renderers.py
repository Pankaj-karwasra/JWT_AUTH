from rest_framework import renderers  # Import the renderers module from DRF
import json  # Import the json module for custom JSON handling

# Define a custom renderer that inherits from DRF's JSONRenderer
class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'  # Set the charset for the response to UTF-8 (default for JSON)
    
    # Override the render method to customize how the response data is rendered
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''  # Initialize the response variable to an empty string
        
        # Check if the response contains an 'ErrorDetail' (commonly used for DRF validation errors)
        if 'ErrorDetail' in str(data):  # If the response contains an error message
            # If so, format the response as a JSON object with an 'error' key
            response = json.dumps({'error': data})
        else:
            # Otherwise, just return the data as JSON (the typical response for successful requests)
            response = json.dumps(data)
        
        return response  # Return the final JSON response

