from flask import app, jsonify
from database import get_db_connection
from flask import render_template
from flask import Flask
from database import init_db
from database import inserir_leitura
from flask import request
from database import deletar_leitura
from database import atualizar_leitura
from flask import redirect
from database import obter_leitura


app = Flask(__name__) 

init_db()

@app.route('/') 
def index():
    conn = get_db_connection()
   
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('index.html', leituras=leituras)


@app.route('/historico')
def historico():
    conn = get_db_connection()
    leituras = conn.execute('SELECT * FROM leituras ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('historico.html', leituras=leituras)

@app.route('/leituras', methods=['GET', 'POST'])
def gerenciar_leituras():
    if request.method == 'POST':
        # Parte que o serial_reader.py usa para injetar dados
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'JSON inválido'}), 400
        
        id_novo = inserir_leitura(
            dados.get('temperatura'),
            dados.get('umidade'),
            dados.get('pressao')
        )
        return jsonify({'id': id_novo, 'status': 'criado'}), 201

    else:
        # Parte que o navegador usa para listar os dados (GET)
        conn = get_db_connection()
        leituras = [dict(row) for row in conn.execute('SELECT * FROM leituras').fetchall()]
        conn.close()
        return jsonify(leituras)


@app.route('/leituras/<int:id>', methods=['DELETE'])
def deletar(id):
    try:
        deletar_leitura(id)
        return jsonify({'status': 'excluido com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        # Recebe os dados novos do formulário HTML
        temp = request.form['temperatura']
        umid = request.form['umidade']
        pressao = request.form.get('pressao')
        
        try:
            # Salva no banco e redireciona de volta para o histórico
            atualizar_leitura(id, float(temp), float(umid), float(pressao) if pressao else None)
            return redirect('/historico')
        except Exception as e:
            return f"Erro ao atualizar: {e}"
    else:
        # Quando acessa a página (GET), busca os dados e mostra o formulário
        leitura = obter_leitura(id)
        if leitura is None:
            return "Leitura não encontrada", 404
        return render_template('editar.html', leitura=leitura)


if __name__ == '__main__':
    app.run(debug=True, port=5000)