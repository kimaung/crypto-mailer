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
  
# Membuat konten HTML dengan CSS inline  
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
            color: #333;  
        }  
        .container {  
            max-width: 1200px;  
            margin: 0 auto;  
        }  
        h1 {  
            text-align: center;  
            margin-bottom: 20px;  
        }  
        .table-responsive {  
            width: 100%;  
            overflow-x: auto;  
            margin-bottom: 20px;  
        }  
        table {  
            width: 100%;  
            border-collapse: collapse;  
            margin: 20px 0;  
            box-shadow: 0 2px 3px rgba(0,0,0,0.1);  
        }  
        th, td {  
            padding: 12px;  
            text-align: left;  
            border-bottom: 1px solid #ddd;  
        }  
        th {  
            background-color: #6200ea;  
            color: white;  
        }  
        tr:hover {  
            background-color: #f1f1f1;  
        }  
        @media screen and (max-width: 600px) {  
            table, thead, tbody, th, td, tr {  
                display: block;  
            }  
            thead tr {  
                position: absolute;  
                top: -9999px;  
                left: -9999px;  
            }  
            tr {  
                border: 1px solid #ccc;  
                margin-bottom: 10px;  
                display: block;  
            }  
            td {  
                border: none;  
                border-bottom: 1px solid #eee;  
                position: relative;  
                padding-left: 50%;  
            }  
            td:before {  
                position: absolute;  
                top: 6px;  
                left: 6px;  
                width: 45%;  
                padding-right: 10px;  
                white-space: nowrap;  
                content: attr(data-label);  
            }  
        }  
    </style>  
</head>  
<body>  
    <div class="container">  
        <h1>Crypto Data Update</h1>  
        <div class="table-responsive">  
            <table>  
                <thead>  
                    <tr>  
                        <th style="background-color: #6200ea; color: white; padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Symbol</th>  
                        <th style="background-color: #6200ea; color: white; padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Name</th>  
                        <th style="background-color: #6200ea; color: white; padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Price (USD)</th>  
                        <th style="background-color: #6200ea; color: white; padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Volume 24h (USD)</th>  
                        <th style="background-color: #6200ea; color: white; padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Market Cap (USD)</th>  
                        <th style="background-color: #6200ea; color: white; padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">24h Change (%)</th>  
                        <th style="background-color: #6200ea; color: white; padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Circulating Supply</th>  
                    </tr>  
                </thead>  
                <tbody>  
"""  
  
for crypto in cryptocurrencies:  
    html_content += f"""  
        <tr>  
            <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="Symbol">{crypto['symbol']}</td>  
            <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="Name">{crypto['name']}</td>  
            <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="Price (USD)">${crypto['price']:,.2f}</td>  
            <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="Volume 24h (USD)">${crypto['volume_24h']:,.2f}</td>  
            <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="Market Cap (USD)">${crypto['market_cap']:,.2f}</td>  
            <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="24h Change (%)">{crypto['percent_change_24h']:.2f}%</td>  
            <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="Circulating Supply">{crypto['circulating_supply']:,}</td>  
        </tr>  
    """  
  
html_content += """  
                </tbody>  
            </table>  
        </div>  
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
