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
        95.6
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <script src="script.js"></script>
</head>
<body>
<div class="container">
    <div class="center">
        <div class="text-center">
            <span class="start">
                {start}
            </span>
        </div>
        <div class="text-center">
            <span class="current">
                <b>{weight}</b> <span style="color: {color};">({diff:.1f})</span>
            </span>
        </div>
        <div class="text-center">
            <span class="goal">
                {goal}
            </span>
        </div>
    </div>
</div>
</body>
</html>
"""

START = 97.0
GOAL = 75.0



def get_weight_float(with_kg):
    result = with_kg.split(' ')[0]
    result = float(result.replace(',', '.'))
    return result


with session() as c:
    c.post(login_url, data=payload)
    response = c.get(measurements_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    rows = soup.find_all('tr')[2:]
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    current_weight_kg = data[0][2]
    prev_weight_kg = data[1][2]

    current_weight_kg = get_weight_float(current_weight_kg)
    prev_weight_kg = get_weight_float(prev_weight_kg)

    print(prev_weight_kg, current_weight_kg)

    diff = current_weight_kg-prev_weight_kg
    if diff < 0:
        color = "green"
    else:
        color = "red"

    html_page = html_page.format(
        weight=current_weight_kg, start=START, goal=GOAL, color=color, diff=diff)
    open(OUTPUT_HTML_FILE, 'w').write(html_page)


