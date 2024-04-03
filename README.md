# Front-End Project for AfyaChat

1. 4 Online forms for collecting basic patient information. 
2. Utilised Flask and Python for creating an SQLite database server and storing the informaation in it.
3. Selectively querying information to display for the user.

## How to Run Locally
1. Run app.py and follow the link of the localhost server that the app is running on.
2. The control flow of the app: Basic Patient Info - > if over 18: confirmation and thank you, -> if not over 18: Guradian Info: confirmation and thank you.

## Security Measures 
1. Input Sanitization: Instead of using simple SQL statments to enter data, parameterized queries are used to avoid falsified code to be inserted in the databse, hence preventing SQL injection.
