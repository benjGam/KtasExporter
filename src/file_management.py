"""Module for managing kata file operations."""

import os
from typing import Set
import logging
from gvars import app_state
from path_validator import validate_path, validate_file_path, validate_git_repository, PathValidationError

logger = logging.getLogger(__name__)

class FileManager:
    """Class responsible for managing kata file operations."""
    
    def __init__(self, repo_path: str, file_name: str):
        """
        Initialize the FileManager.
        
        Args:
            repo_path: Path to the repository
            file_name: Name of the kata file
        """
        self.repo_path = repo_path
        self.file_name = file_name
        self.file_path = os.path.join(repo_path, file_name)
        
    def validate_paths(self) -> None:
        """
        Validate all required paths at startup.
        
        Raises:
            PathValidationError: If path validation fails
        """
        logger.info("Validating paths...")
        validate_path(self.repo_path)
        validate_git_repository(self.repo_path)
        validate_file_path(self.file_path, create_if_missing=True)
        logger.info("Path validation completed successfully")
        
    def add_kata(self, content: str) -> None:
        """
        Append a kata to the specified file using buffered write.
        
        Args:
            content: Content to write
            
        Raises:
            IOError: If there is an error writing to the file
        """
        try:
            with open(self.file_path, "a", buffering=8192) as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Error writing to file {self.file_path}: {str(e)}")
            raise
            
    def read_katas(self) -> None:
        """
        Read and process the kata file to populate already_pushed_katas.
        Uses a set for faster lookups and memory efficiency.
        
        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If there is an error reading the file
        """
        kata_set: Set[str] = set()
        
        try:
            with open(self.file_path, 'r', buffering=8192) as f:
                for line in f:
                    if line.startswith('#') and "kyu" in line.lower():
                        kata_title = line[1:line.rfind('#')].strip().split("[")[0].strip()
                        kata_set.add(kata_title)
            
            for kata_name in kata_set:
                app_state.add_pushed_kata(kata_name)
                
        except FileNotFoundError:
            logger.warning(f"File {self.file_path} not found. Creating a new file.")
            open(self.file_path, 'a').close()
        except IOError as e:
            logger.error(f"Error reading file {self.file_path}: {str(e)}")
            raise