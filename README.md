# Coding excercise for Apple

### Running

Uses Phython 2.7
Install "matplotlib"
**Usage: python apple_coding.py <root_dir> "<keyword>"**
  e.g. python apple_coding.py test_dir-1 "^[a-zA-Z]+_TESTResult.*"
  
### Testing

There are 8 test directories in the project root directory.
Check out test case explanations in test.py
**Run: python test.py**

##### WAYS TO BREAK THE ROUTINE

- Root directory may be relative path or absolute path. The code handles both types.
- Root directory may NOT exist.
- Keyword may NOT be a valid regular expression.
- Root directory may be empty.
- Code walks thorugh root directory recursively. It may cause stack overflow error for deep root directories. Iterative way can be used in order to avoid stack overflow issue.
- Files may be too large to fit into the memory. Memory mapped file object is used to solve the possible memory issue.
- A file may be a link to another file in the file system. Code keeps track of the visited files by their real paths with search result of the keyword in the file.
- A directory may be a link to parent directory in the file system and may lead to infiniti loop. The code detects loops between directories and breaks the recursion for that directory. 
- Root directory path may be a link to another dir in the file system or link may be broken.
- A link may be broken.