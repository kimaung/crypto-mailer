import os  
import requests  
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
  
def get_api_key():  
    """Mengambil API key dari variabel lingkungan."""  
    return os.getenv('CMC_API_KEY')  
  
def fetch_crypto_data(api_key):  
    """Mengambil data cryptocurrency dari CoinMarketCap."""  
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'  
    parameters = {  
        'symbol': 'BTC,ETH,XRP,BNB,SOL',  
        'convert': 'USD'  
    }  
    headers = {  
        'Accepts': 'application/json',  
        'X-CMC_PRO_API_KEY': api_key,  
    }  
    response = requests.get(url, headers=headers, params=parameters)  
    response.raise_for_status()
    return response.json()  
  
def format_crypto_data(data):  
    """Memformat data cryptocurrency menjadi list."""  
    cryptocurrencies = []  
    for symbol, entries in data['data'].items():  
        entry = entries[0]  
        crypto = {  
            'name': entry['name'],  
            'price': entry['quote']['USD']['price'],  
            'percent_change_24h': entry['quote']['USD']['percent_change_24h'],  
        }  
        cryptocurrencies.append(crypto)  
    return cryptocurrencies  
  
def generate_html_content(cryptocurrencies):  
    """Menghasilkan konten HTML untuk email."""  
    html_content = """        
    <!DOCTYPE html>        
    <html lang="en">        
    <head>        
        <meta charset="UTF-8">        
        <meta name="viewport" content="width=device-width, initial-scale=1.0">        
        <title>Crypto Price Update 🕵🏻</title>
    </head>        
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; color: #333;">        
        <div style="max-width: 1200px; margin: 0 auto;">        
            <h1 style="text-align: center; margin-bottom: 20px;">Crypto Data Update</h1>        
            <div style="width: 100%; overflow-x: auto; margin-bottom: 20px;">        
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 2px 3px rgba(0,0,0,0.1);">        
                    <thead>        
                        <tr>        
                            <th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd; background-color: #6200ea; color: white;">Name</th>        
                            <th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd; background-color: #6200ea; color: white;">Price (USD)</th>        
                            <th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd; background-color: #6200ea; color: white;">24h Change (%)</th>        
                        </tr>        
                    </thead>        
                    <tbody>        
    """      
      
    for crypto in cryptocurrencies:      
        row_color = '#f1f1f1' if crypto['percent_change_24h'] < 0 else 'transparent'      
        html_content += f"""        
            <tr style="background-color: {row_color};">        
                <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="Name">{crypto['name']}</td>        
                <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="Price (USD)">${crypto['price']:,.2f}</td>        
                <td style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;" data-label="24h Change (%)">{crypto['percent_change_24h']:.2f}%</td>        
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
    return html_content      
  
def send_email(html_content):      
    """Mengirim email dengan konten HTML yang diberikan."""      
    email_user = os.getenv('EMAIL_USER')      
    email_pass = os.getenv('EMAIL_PASS')      
    email_to = os.getenv('EMAIL_TO')      
    smtp_server = os.getenv('SMTP_SERVER')      
    sender_name = 'Crypto Update'      
      
    if not email_to:      
        raise ValueError("EMAIL_TO environment variable is not set or is empty")      
      
    subject = 'Crypto Price Update'      
    msg = MIMEMultipart()      
    msg['From'] = f"{sender_name} <{email_user}>"      
    msg['To'] = email_to      
    msg['Subject'] = subject      
      
    msg.attach(MIMEText(html_content, 'html'))      
      
    try:      
        with smtplib.SMTP(smtp_server, 587) as server:      
            server.starttls()      
            server.login(email_user, email_pass)      
            server.sendmail(email_user, email_to, msg.as_string())      
    except Exception as e:      
        print(f"Error sending email: {e}")      
  
def main():      
    """Fungsi utama untuk menjalankan alur program."""      
    try:      
        api_key = get_api_key()      
        data = fetch_crypto_data(api_key)      
        cryptocurrencies = format_crypto_data(data)      
        html_content = generate_html_content(cryptocurrencies)      
        send_email(html_content)      
    except Exception as e:      
        print(f"An error occurred: {e}")      
      
if __name__ == "__main__":      
    main()      
