# whoshome
Python script to tell me who is currently home. Uses an ASUS router's web interface to determine active wireless devices.

## Setup
1. Set the username, password, and gateway IP address in `whoshome.py`.  
    eg.  
    ```python
    USERNAME = "admin"
    PASSWORD = "password"
    GATEWAY = "192.168.1.1"
    ```
2. Set the list of users you want to track.  
    eg.
    ```python
    USERS = {
        'Me': ['5C:F9:38:8E:0B:E6', '60:9A:C1:12:9A:13'],
        'Dad': ['D0:33:11:5F:01:0E'],
        'Mom': ['D0:A6:37:7F:8F:99'],
    }
    ```

## Credits
Brandon Asuncion // me@brandonasuncion.tech

## License
[MIT License](https://choosealicense.com/licenses/mit/)