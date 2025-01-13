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
  
json_data = {  
    'cryptocurrencies': cryptocurrencies  
}  
  
# Mengirim email  
email_user = os.getenv('EMAIL_USER')  
email_pass = os.getenv('EMAIL_PASS')  
email_to = os.getenv('EMAIL_TO')  
  
subject = 'Crypto Data Update'  
body = str(json_data)  
  
msg = MIMEMultipart()  
msg['From'] = email_user  
msg['To'] = email_to  
msg['Subject'] = subject  
  
msg.attach(MIMEText(body, 'plain'))  
  
server = smtplib.SMTP('mail.aes.my.id', 587)  
server.starttls()  
server.login(email_user, email_pass)  
text = msg.as_string()  
server.sendmail(email_user, email_to, text)  
server.quit()  
