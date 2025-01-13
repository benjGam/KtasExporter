"""Module for managing kata file operations."""

import os
from typing import Set
import logging
from gvars import app_state
from path_validator import validate_path, validate_file_path, PathValidationError

logger = logging.getLogger(__name__)

def validate_paths(repo_path: str, file_name: str) -> None:
    """
    Validate all required paths at startup.
    
    Args:
        repo_path: Path to the repository
        file_name: Name of the kata file
        
    Raises:
        PathValidationError: If path validation fails
    """
    logger.info("Validating paths...")
    validate_path(repo_path)
    validate_file_path(os.path.join(repo_path, file_name), create_if_missing=True)
    logger.info("Path validation completed successfully")

def add_kata_in_file(repo_path: str, file_name: str, content: str) -> None:
    """
    Append a kata to the specified file using buffered write.
    
    Args:
        repo_path: Path to the repository
        file_name: Name of the file to write to
        content: Content to write
        
    Raises:
        IOError: If there is an error writing to the file
    """
    file_path = os.path.join(repo_path, file_name)
    try:
        with open(file_path, "a", buffering=8192) as f:
            f.write(content)
    except IOError as e:
        logger.error(f"Error writing to file {file_path}: {str(e)}")
        raise

def read_kata_file(repo_path: str, file_name: str) -> None:
    """
    Read and process the kata file to populate already_pushed_katas.
    Uses a set for faster lookups and memory efficiency.
    
    Args:
        repo_path: Path to the repository
        file_name: Name of the file to read
        
    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there is an error reading the file
    """
    file_path = os.path.join(repo_path, file_name)
    kata_set: Set[str] = set()
    
    try:
        with open(file_path, 'r', buffering=8192) as f:
            for line in f:
                if line.startswith('#') and "kyu" in line.lower():
                    kata_title = line[1:line.rfind('#')].strip().split("[")[0].strip()
                    kata_set.add(kata_title)
        
        for kata_name in kata_set:
            app_state.add_pushed_kata(kata_name)
            
    except FileNotFoundError:
        logger.warning(f"File {file_path} not found. Creating a new file.")
        open(file_path, 'a').close()
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        raise