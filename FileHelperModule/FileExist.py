def FileExist(filename:str)-> bool:
    try:
        with open(filename, 'r'):
            print(f" File '{filename}' exists and is readable")
            return True
    except FileNotFoundError:
        print(f"✗ File '{filename}' does not exist")
        return False
    except PermissionError:
        print(f" Permission denied for file '{filename}'")
        return False
    except Exception as e:
        print(f" Error accessing file: {e}")
        return False
    