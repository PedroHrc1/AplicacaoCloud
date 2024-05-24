from flask import Flask, render_template, request
from botocore.exceptions import ClientError
import uuid
import boto3
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configurar boto3 para se conectar ao DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1a')
table = dynamodb.Table('PrjPedroDynamoDBTable')

@app.route('/', methods=['GET', 'POST'])
def form():
    nomeAluno = None
    nota = None
    all_entries = []

    if request.method == 'POST':
        nomeAluno = request.form.get('nomeAluno')
        nota = request.form.get('nota')

        # Gerar um UUID para o item
        item_id = str(uuid.uuid4())

        # Inserir os dados no DynamoDB
        try:
            table.put_item(
                Item={
                    'id': item_id,
                    'nomeAluno': nomeAluno,
                    'nota': nota
                }
            )
            logging.info("Dados inseridos com sucesso no DynamoDB")
        except ClientError as e:
            logging.error(e)
            return "Erro ao inserir dados no DynamoDB", 500

    # Recuperar todos os dados do DynamoDB para exibição
    try:
        response = table.scan()
        all_entries = response.get('Items', [])
    except ClientError as e:
        logging.error(e)
        return "Erro ao recuperar dados do DynamoDB", 500

    return render_template('site.html', nomeAluno=nomeAluno, nota=nota, entries=all_entries)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
