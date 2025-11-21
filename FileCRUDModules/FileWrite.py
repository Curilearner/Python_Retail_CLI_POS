def FileWriter(filename, latestinventory):
    try:
        with open(filename, 'w') as file: 
            for item in latestinventory:
                file.write(f"{item.sn},{item.name},{item.price},{item.quantity}\n")

        return True
    except Exception as e:
        print(f"✗ Error writing to file: {e}")
        return False
    