"""
Custom exceptions for the Sign Generator application
"""

class SignGeneratorError(Exception):
    """Base exception for all sign generator errors"""
    pass


class STLExportError(SignGeneratorError):
    """Exception raised when STL export fails"""
    def __init__(self, layer, reason, suggestions=None):
        self.layer = layer
        self.reason = reason
        self.suggestions = suggestions or []

        message = f"Failed to export {layer}: {reason}"
        if suggestions:
            message += f"\nSuggestions:\n" + "\n".join(f"  • {s}" for s in suggestions)

        super().__init__(message)


class ValidationError(SignGeneratorError):
    """Exception raised when input validation fails"""
    def __init__(self, field, message, valid_range=None):
        self.field = field
        self.message = message
        self.valid_range = valid_range

        full_message = f"Validation error for {field}: {message}"
        if valid_range:
            full_message += f" (valid range: {valid_range})"

        super().__init__(full_message)


class GeometryError(SignGeneratorError):
    """Exception raised when geometry generation fails"""
    def __init__(self, operation, details):
        self.operation = operation
        self.details = details
        super().__init__(f"Geometry error during {operation}: {details}")


class FontError(SignGeneratorError):
    """Exception raised when font-related operations fail"""
    def __init__(self, font_name, reason):
        self.font_name = font_name
        self.reason = reason
        super().__init__(f"Font error with '{font_name}': {reason}")