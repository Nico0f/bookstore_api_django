from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

class OutOfStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This item is out of stock.'
    default_code = 'out_of_stock'

class InvalidOrderStatusTransition(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid order status transition.'
    default_code = 'invalid_status_transition'

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code
        
        if isinstance(exc, OutOfStockException):
            response.data['error_type'] = 'out_of_stock'
        elif isinstance(exc, InvalidOrderStatusTransition):
            response.data['error_type'] = 'invalid_status_transition'
    
    return response