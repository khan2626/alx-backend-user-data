#!/usr/bin/env python3
"""It manages API authentication
"""

from flask import request
from typing import List, Typevar


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required
        """
        
        if path is None:
            return None
        if excluded_paths is None or []:
            return True
        if path in excluded_paths:
            return False
        for ex_path in excluded_paths:
            if ex_path.startswith(path):
                return False
            if path.startswith(ex_path):
                return False
            elif ex_path[-1] == '*':
                if path.startswith(ex_path[:-1]):
                    return False

        
    
    def authorization_header(self, request=None) -> str:
        """Gets authorization header from request
        """
        return None
    
    def authorization_header(self, request=None) -> str:
        """Returns current user
        """

        return False
    

