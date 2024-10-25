import os

class PageviewDumpParser:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        # Open the file and get an iterator to read it line by line
        self.file = open(file_path, 'r')
        self.line_iterator = iter(self.file)
    
    def get_next_line(self) -> str | None:
        """
        Get the next line from the file that starts with en.wikipedia

        Returns:
            str: The next line from the file.
        """
        try:
            while True:
                line = next(self.line_iterator)
                if line.startswith('en.wikipedia'):
                    return line
        except StopIteration:
            return None


# Example usage
file_path = '~/Downloads/pageviews-20241024-user'
absolute_file_path = os.path.abspath(os.path.expanduser(file_path))
parser = PageviewDumpParser(absolute_file_path)

import time
# Get the first line
start_time = time.time()
line = parser.get_next_line()
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
for _ in range(10000):
    line = parser.get_next_line()
    if line is None:
        break

print("--- %s seconds ---" % (time.time() - start_time))