"""Module for path validation operations."""

import os
import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)

class PathValidationError(Exception):
    """Exception raised for path validation errors."""
    pass

def validate_git_repository(path: str) -> None:
    """
    Validate if a directory is a Git repository.
    
    Args:
        path: Path to validate
        
    Raises:
        PathValidationError: If path is not a Git repository
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip() != 'true':
            logger.error(f"Invalid repository: {path} is not a Git repository")
            raise PathValidationError(f"Path is not a Git repository: {path}")
        logger.info("Git repository validation successful")
    except subprocess.CalledProcessError:
        logger.error(f"Invalid repository: {path} is not a Git repository")
        raise PathValidationError(f"Path is not a Git repository: {path}")
    except Exception as e:
        logger.error(f"Failed to validate Git repository: {e}")
        raise PathValidationError(f"Failed to validate Git repository: {e}")

def validate_path(path: str, require_write: bool = True) -> None:
    """
    Validate a path for existence and permissions.
    
    Args:
        path: Path to validate
        require_write: Whether write permissions are required
        
    Raises:
        PathValidationError: If path validation fails
    """
    if not os.path.exists(path):
        logger.error(f"Invalid path: {path} does not exist")
        raise PathValidationError(f"Path does not exist: {path}")
        
    if not os.path.isdir(path):
        logger.error(f"Invalid path: {path} is not a directory")
        raise PathValidationError(f"Path is not a directory: {path}")
        
    if require_write and not os.access(path, os.W_OK):
        logger.error(f"Invalid path: no write permission for {path}")
        raise PathValidationError(f"No write permission for path: {path}")
        
    logger.info("Path validation successful")

def validate_file_path(file_path: str, create_if_missing: bool = False) -> None:
    """
    Validate a file path and optionally create parent directories.
    
    Args:
        file_path: Path to the file
        create_if_missing: Whether to create parent directories if they don't exist
        
    Raises:
        PathValidationError: If file path validation fails
    """
    directory = os.path.dirname(file_path)
    
    if not os.path.exists(directory):
        if create_if_missing:
            try:
                os.makedirs(directory, exist_ok=True)
                logger.info(f"Created directory structure: {directory}")
            except OSError as e:
                logger.error(f"Failed to create directory structure: {e}")
                raise PathValidationError(f"Failed to create directory structure: {e}")
        else:
            logger.error(f"Invalid file path: parent directory {directory} does not exist")
            raise PathValidationError(f"Parent directory does not exist: {directory}")
            
    if not os.access(directory, os.W_OK):
        logger.error(f"Invalid file path: no write permission for {directory}")
        raise PathValidationError(f"No write permission for directory: {directory}")
        
    if os.path.exists(file_path) and not os.access(file_path, os.W_OK):
        logger.error(f"Invalid file path: no write permission for {file_path}")
        raise PathValidationError(f"No write permission for file: {file_path}")
        
    logger.info("File path validation successful") 