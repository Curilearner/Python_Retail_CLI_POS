import os
def GetSerialNumber(filename);
    try:
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            return 1

        with open(filename , 'r') as file:
            for line in file:
                number, text = line.strip().split(",", 1)
                return number+1

    except Exception as e:
        print("Error")