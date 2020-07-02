from requests import session
from bs4 import BeautifulSoup
import environ

env = environ.Env()
env.read_env()

USERNAME = env('FUT33V_USERNAME')
PASSWORD = env('FUT33V_PASSWORD')
OUTPUT_HTML_FILE = env('FUT33V_OUTPUT')

login_url = "https://www.myfitnesspal.com/ru/account/login"
measurements_url = "https://www.myfitnesspal.com/ru/measurements/edit"

payload = {
    'username': USERNAME,
    'password': PASSWORD
}

html_page = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>
            {weight}
        </title>
        <link rel="stylesheet" type="text/css" href="style.css">
        <script src="script.js"></script>
    </head>

    <body>
        <div class="weight">
            {weight}
        </div>
    </body>
</html>
"""

with session() as c:
    c.post(login_url, data=payload)
    response = c.get(measurements_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    weight_with_kg = soup.tbody.find_all('td')[2].get_text()
    weight = weight_with_kg.split(' ')[0]
    weight = float(weight.replace(',', '.'))
    print(weight)
    html_page = html_page.format(weight=weight)
    open(OUTPUT_HTML_FILE, 'w').write(html_page)


