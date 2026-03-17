import requests

def main():
    resp = requests.get("https://peps.python.org/api/peps.json")
    data = resp.json()
    print(data)

if __name__ == "__main__":
    main()
