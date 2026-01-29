Python 3.12.4 (tags/v3.12.4:8e8a4ba, Jun  6 2024, 19:30:16) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import boto3
import hashlib
import os

s3 = boto3.client('s3')
polly = boto3.client('polly')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PollyCache')

def lambda_handler(event, context):
    # 1. Dosya bilgilerini al
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Sadece input klasöründeki .txt dosyalarını işle
    if not key.startswith('input/') or not key.endswith('.txt'):
        return
    
    # 2. Metni oku
...     obj = s3.get_object(Bucket=bucket, Key=key)
...     text_content = obj['Body'].read().decode('utf-8')
...     
...     # 3. Metnin Hash'ini al (Deduplication için)
...     text_hash = hashlib.md5(text_content.encode()).hexdigest()
...     
...     # 4. DynamoDB'de kontrol et (Cache check)
...     response = table.get_item(Key={'TextHash': text_hash})
...     
...     if 'Item' in response:
...         print("Bu metin zaten sese çevrilmiş. Cache'den dönülüyor.")
...         return {
...             'statusCode': 200,
...             'body': 'File already exists in cache.'
...         }
... 
...     # 5. Polly ile sese çevir
...     print("Yeni metin algılandı, Polly çalıştırılıyor...")
...     polly_response = polly.synthesize_speech(
...         Text=text_content,
...         OutputFormat='mp3',
...         VoiceId='Filiz' # Türkçe ses (Merve veya Filiz seçebilirsin)
...     )
...     
...     # 6. Sesi S3'e kaydet
...     output_key = key.replace('input/', 'output/').replace('.txt', '.mp3')
...     s3.put_object(
...         Bucket=bucket,
...         Key=output_key,
...         Body=polly_response['AudioStream'].read(),
...         ContentType='audio/mpeg'
...     )
...     
...     # 7. DynamoDB'ye kaydet
...     table.put_item(Item={'TextHash': text_hash, 'S3Path': output_key})
...     
...     return {
...         'statusCode': 200,
...         'body': f'Success! Audio saved to: {output_key}'
