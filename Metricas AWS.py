
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Configurações do S3
    s3_client = boto3.client('s3')
    bucket_name = 'balsas.produtecnicane'
    
    # Obter informações do S3
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    # Verificar se existem objetos no bucket
    if 'Contents' in response:
        objects = response['Contents']
        
        # Calcular o total de gigabytes enviados durante o dia
        total_size_gb = sum(obj['Size'] for obj in objects) / (1024 ** 3)  # Converter para gigabytes
    else:
        # Caso não haja objetos, definir o total_size_gb como zero
        total_size_gb = 0
    
    # Obter a data atual
    current_date = datetime.now().strftime('%d-%m-%Y')
    
    # Enviar email com o relatório
    client = boto3.client("ses")
    subject = f"Relatório diário de uso do S3 - {current_date}"
    body = f'Data: {current_date}\n\n'
    body += f'Quantidade total de gigabytes carregados durante o dia: {total_size_gb:.2f} GB'
    
    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
    response = client.send_email(Source="carloscarreiro021@gmail.com",
                                Destination={"ToAddresses": ["carlos.carreiro@produtecnicane.com.br"]},
                                Message=message)
    
    return response





























"""import json
import boto3

def lambda_handler(event, context):
    # Configurações do S3
    s3_client = boto3.client('s3')
    bucket_name = 'balsas.produtecnicane'
    
    # Obter informações do S3
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    total_size = sum([obj['Size'] for obj in response['Contents']])
    total_size_gb = total_size / (1024 ** 3)  # Converter para gigabytes
    
    # Enviar e-mail com o relatório
    client = boto3.client("ses")
    subject = "Relatório diário de uso do S3"
    body = f'A quantidade total de gigabytes carregados no bucket {bucket_name} é: {total_size_gb:.2f} GB'
    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
    response = client.send_email(Source="carloscarreiro021@gmail.com",
                                Destination={"ToAddresses": ["carlos.carreiro@produtecnicane.com.br"]},
                                Message=message)
    
    return response"""
