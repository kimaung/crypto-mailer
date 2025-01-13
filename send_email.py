import os  
import requests  
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
  
# Mengambil API key dari variabel lingkungan  
api_key = os.getenv('CMC_API_KEY')  
url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'  
parameters = {  
    'symbol': 'BTC,ETH,XRP,BNB,SOL',  
    'convert': 'USD'  
}  
headers = {  
    'Accepts': 'application/json',  
    'X-CMC_PRO_API_KEY': api_key,  
}  
  
# Mengambil data dari CoinMarketCap  
response = requests.get(url, headers=headers, params=parameters)  
data = response.json()  
  
# Memformat data menjadi JSON yang diinginkan  
cryptocurrencies = []  
for symbol, entries in data['data'].items():  
    # Ambil entri pertama untuk setiap simbol  
    entry = entries[0]  
    crypto = {  
        'symbol': entry['symbol'],  
        'name': entry['name'],  
        'price': entry['quote']['USD']['price'],  
        'volume_24h': entry['quote']['USD']['volume_24h'],  
        'market_cap': entry['quote']['USD']['market_cap'],  
        'percent_change_24h': entry['quote']['USD']['percent_change_24h'],  
        'circulating_supply': entry.get('circulating_supply', None)  
    }  
    cryptocurrencies.append(crypto)  
  
# Membuat konten HTML  
html_content = """  
<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Crypto Data Update</title>  
    <style>  
        body {  
            font-family: Arial, sans-serif;  
            background-color: #f4f4f9;  
            margin: 0;  
            padding: 20px;  
        }  
        .container {  
            max-width: 100%;  
            margin: 0 auto;  
            padding: 20px;  
            background-color: #fff;  
            box-shadow: 0 2px 3px rgba(0,0,0,0.1);  
        }  
        h2 {  
            text-align: center;  
            color: #333;  
        }  
        .table-responsive-stack {  
            width: 100%;  
            border-collapse: collapse;  
            margin: 20px 0;  
            box-shadow: 0 2px 3px rgba(0,0,0,0.1);  
        }  
        .table-responsive-stack tr {  
            display: -webkit-box;  
            display: -ms-flexbox;  
            display: flex;  
            -webkit-box-orient: horizontal;  
            -webkit-box-direction: normal;  
                -ms-flex-direction: row;  
                    flex-direction: row;  
        }  
        .table-responsive-stack th,  
        .table-responsive-stack td {  
            display: block;  
            flex-grow: 1;  
            flex-shrink: 1;  
            flex-basis: 100%;  
            padding: 12px;  
            text-align: left;  
            border-bottom: 1px solid #ddd;  
        }  
        .table-responsive-stack th {  
            background-color: #4CAF50;  
            color: white;  
        }  
        .table-responsive-stack tr:hover {  
            background-color: #f1f1f1;  
        }  
        .table-responsive-stack-thead {  
            font-weight: bold;  
        }  
        @media screen and (max-width: 768px) {  
            .table-responsive-stack tr {  
                -webkit-box-orient: vertical;  
                -webkit-box-direction: normal;  
                    -ms-flex-direction: column;  
                        flex-direction: column;  
                border-bottom: 3px solid #ccc;  
                display: block;  
            }  
            .table-responsive-stack td {  
                float: left\9;  
                width: 100%;  
            }  
        }  
    </style>  
</head>  
<body>  
    <div class="container">  
        <h2>Crypto Data Update</h2>  
        <table class="table-responsive-stack" id="tableOne">  
            <thead class="thead-dark">  
                <tr>  
                    <th>Symbol</th>  
                    <th>Name</th>  
                    <th>Price (USD)</th>  
                    <th>Volume 24h (USD)</th>  
                    <th>Market Cap (USD)</th>  
                    <th>24h Change (%)</th>  
                    <th>Circulating Supply</th>  
                </tr>  
            </thead>  
            <tbody>  
"""  
  
for crypto in cryptocurrencies:  
    html_content += f"""  
                <tr>  
                    <td data-label="Symbol">{crypto['symbol']}</td>  
                    <td data-label="Name">{crypto['name']}</td>  
                    <td data-label="Price (USD)">${crypto['price']:,.2f}</td>  
                    <td data-label="Volume 24h (USD)">${crypto['volume_24h']:,.2f}</td>  
                    <td data-label="Market Cap (USD)">${crypto['market_cap']:,.2f}</td>  
                    <td data-label="24h Change (%)">{crypto['percent_change_24h']:.2f}%</td>  
                    <td data-label="Circulating Supply">{crypto['circulating_supply']:,}</td>  
                </tr>  
    """  
  
html_content += """  
            </tbody>  
        </table>  
    </div>  
</body>  
</html>  
"""  
  
# Mengirim email  
email_user = os.getenv('EMAIL_USER')  
email_pass = os.getenv('EMAIL_PASS')  
email_to = os.getenv('EMAIL_TO')  
  
if not email_to:  
    raise ValueError("EMAIL_TO environment variable is not set or is empty")  
  
subject = 'Crypto Data Update'  
msg = MIMEMultipart()  
msg['From'] = email_user  
msg['To'] = email_to  
msg['Subject'] = subject  
  
# Menambahkan konten HTML ke email  
msg.attach(MIMEText(html_content, 'html'))  
  
server = smtplib.SMTP('mail.aes.my.id', 587)  
server.starttls()  
server.login(email_user, email_pass)  
text = msg.as_string()  
server.sendmail(email_user, email_to, text)  
server.quit()  
