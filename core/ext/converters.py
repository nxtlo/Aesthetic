from datetime import datetime

class convert():
    """Useful number converter"""

    def to_bin(self, bnum) -> int:
        """Convert any decimal number to binary"""
        try:
            return int(bnum, 2)
        except Exception as e:
            raise e


    def to_text(self, text) -> str:
        """Convert text(str) to binary"""
        try:
            return ' '.join(format(x, 'b') for x in bytearray(text, 'utf-8'))
        except Exception as e:
            raise e


    def utc_now(self, time = datetime.now()):
        return time or datetime.utcnow()