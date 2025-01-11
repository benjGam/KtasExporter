class SensitiveDataMasker:
    """Handles masking of sensitive data for security purposes."""
    
    @staticmethod
    def mask_password(password: str, visible_chars: int = 2) -> str:
        """
        Mask password, showing only first and last n characters.
        
        Args:
            password: Password to mask
            visible_chars: Number of visible characters at start and end
            
        Returns:
            Masked password
        """
        if not password:
            return ""
            
        if len(password) <= visible_chars * 2:
            return "*" * len(password)
            
        return (
            password[:visible_chars] +
            "*" * (len(password) - (visible_chars * 2)) +
            password[-visible_chars:]
        )
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        Mask email address, showing only first 2 and last 2 characters of local part.
        
        Args:
            email: Email address to mask
            
        Returns:
            Masked email address
        """
        if not email or "@" not in email:
            return ""
            
        local, domain = email.split("@")
        
        if len(local) <= 4:
            masked_local = "*" * len(local)
        else:
            masked_local = local[:2] + "*" * (len(local) - 4) + local[-2:]
            
        return f"{masked_local}@{domain}"
    
    @staticmethod
    def mask_credentials(email: str, password: str) -> tuple[str, str]:
        """
        Mask both email and password.
        
        Args:
            email: Email address to mask
            password: Password to mask
            
        Returns:
            Tuple of masked email and password
        """
        return (
            SensitiveDataMasker.mask_email(email),
            SensitiveDataMasker.mask_password(password)
        ) 