from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

# Inicializando o app Flask
app = Flask(__name__)
CORS(app)  # Permite requisições de outras origens (para integração com Vue.js, por exemplo)

# Carregando o CSV das operadoras
try:
    df = pd.read_excel(r"C:\Users\USUARIO\Desktop\Testes_Estagio\Teste_de_API\Relatorio_cadop.xlsx")
    df['razao_social'] = df['Razao_Social'].fillna('')  # Evita erros com NaN
except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")
    df = pd.DataFrame()  # Cria um DataFrame vazio para evitar falhas

@app.route('/buscar-operadora', methods=['GET'])
def buscar_operadora():
    query = request.args.get('q', '').strip()  # Obtém o parâmetro de consulta
    
    if df.empty:
        return jsonify({"erro": "Arquivo de dados não carregado"}), 500
    
    if query:
        results = df[df['Razao_Social'].str.contains(query, case=False, na=False)]
    else:
        results = df

    return jsonify(results.to_dict(orient='records'))  # Retorna os resultados como JSON

if __name__ == '__main__':
    app.run(debug=True)
