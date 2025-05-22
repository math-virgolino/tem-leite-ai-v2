from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User, Doacao, Mensagem
from math import radians, sin, cos, sqrt, atan2
import requests
from datetime import datetime

def init_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            print(f"Tentativa de login: email={email}, password={password}")  # Depuração

            user = User.query.filter_by(email=email).first()
            if user:
                print(f"Usuário encontrado: {user.email}, tipo={user.tipo}")  # Depuração
                if user.password == password:
                    login_user(user)
                    print("Login bem-sucedido!")  # Depuração
                    if user.tipo == 'doador':
                        return redirect(url_for('dashboard_doador'))
                    else:
                        return redirect(url_for('dashboard_receptor'))
                else:
                    print("Senha incorreta!")  # Depuração
                    flash('Senha incorreta.', 'danger')
            else:
                print("Usuário não encontrado!")  # Depuração
                flash('E-mail não encontrado.', 'danger')

        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    def obter_coordenadas(endereco):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': endereco,
            'format': 'json'
        }
        headers = {
            'User-Agent': 'TemLeiteAi/1.0'  # Adicione um User-Agent para evitar bloqueios
        }
        response = requests.get(url, params=params, headers=headers).json()
        if response:
            latitude = float(response[0]['lat'])
            longitude = float(response[0]['lon'])
            return latitude, longitude
        return None, None

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            tipo = request.form.get('tipo')  # 'doador' ou 'receptor'
            endereco = request.form.get('endereco')
            cidade = request.form.get('cidade')
            estado = request.form.get('estado')
            cep = request.form.get('cep')

            # Obter latitude e longitude a partir do endereço
            latitude, longitude = obter_coordenadas(f"{endereco}, {cidade}, {estado}, {cep}")
            if latitude is None or longitude is None:
                flash('Endereço não encontrado. Verifique os dados e tente novamente.', 'danger')
                return redirect(url_for('register'))

            # Cria o usuário com os novos campos
            user = User(
                username=username,
                email=email,
                password=password,
                tipo=tipo,
                endereco=endereco,
                cidade=cidade,
                estado=estado,
                cep=cep,
                latitude=latitude,
                longitude=longitude
            )

            try:
                db.session.add(user)
                db.session.commit()
                flash('Conta criada com sucesso!', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao criar a conta. Tente novamente.', 'danger')
                print(f"Erro ao criar usuário: {e}")  # Log do erro
                return redirect(url_for('register'))

        return render_template('register.html')

    @app.route('/dashboard_doador')  # Rota do dashboard do doador
    @login_required
    def dashboard_doador():
        if current_user.tipo != 'doador':
            return redirect(url_for('index'))
        return render_template('dashboard_doador.html')

    @app.route('/dashboard_receptor')  # Rota do dashboard do receptor
    @login_required
    def dashboard_receptor():
        if current_user.tipo != 'receptor':
            return redirect(url_for('index'))
        return render_template('dashboard_receptor.html')

    def calcular_distancia(lat1, lon1, lat2, lon2):
        # Raio da Terra em quilômetros
        R = 6371.0

        # Converte graus para radianos
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        # Diferença das coordenadas
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        # Fórmula de Haversine
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Distância em quilômetros
        distancia = R * c
        return distancia

    # @app.route('/buscar_doadores', methods=['GET', 'POST'])
    # @login_required
    # def buscar_doadores():
    #     if current_user.tipo != 'receptor':
    #         return redirect(url_for('index'))

    #     if request.method == 'POST':
    #         # Obter a localização do receptor
    #         receptor_lat = current_user.latitude
    #         receptor_lon = current_user.longitude

    #         # Buscar todos os doadores que fizeram pelo menos uma doação
    #         doadores = User.query.filter_by(tipo='doador').join(Doacao).distinct().all()

    #         # Calcular a distância de cada doador
    #         doadores_proximos = []
    #         for doador in doadores:
    #             distancia = calcular_distancia(receptor_lat, receptor_lon, doador.latitude, doador.longitude)
    #             if distancia <= 50:  # Exemplo: 50 km de distância máxima
    #                 doadores_proximos.append((doador, distancia))

    #         # Ordenar por distância
    #         doadores_proximos.sort(key=lambda x: x[1])

    #         return render_template('buscar_doadores.html', doadores=doadores_proximos)

    #     return render_template('buscar_doadores.html')
    
    @app.route('/cadastrar_doacao', methods=['GET', 'POST'])
    @login_required
    def cadastrar_doacao():
        if current_user.tipo != 'doador':
            return redirect(url_for('index'))

        if request.method == 'POST':
            quantidade = request.form.get('quantidade')

            if not quantidade:
                flash('Por favor, insira a quantidade de leite doada.', 'danger')
                return redirect(url_for('cadastrar_doacao'))

            try:
                quantidade = float(quantidade)
                if quantidade <= 0:
                    flash('A quantidade deve ser maior que zero.', 'danger')
                    return redirect(url_for('cadastrar_doacao'))
            except ValueError:
                flash('Quantidade inválida. Insira um número válido.', 'danger')
                return redirect(url_for('cadastrar_doacao'))

            # Cria a nova doação
            nova_doacao = Doacao(
                doador_id=current_user.id,
                quantidade=quantidade
            )

            try:
                db.session.add(nova_doacao)
                db.session.commit()
                flash('Doação cadastrada com sucesso!', 'success')
                return redirect(url_for('dashboard_doador'))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao cadastrar a doação. Tente novamente.', 'danger')
                print(f"Erro ao cadastrar doação: {e}")  # Log do erro
                return redirect(url_for('cadastrar_doacao'))

        return render_template('cadastrar_doacao.html')
    
    
    @app.route('/enviar_mensagem/<int:destinatario_id>', methods=['GET', 'POST'])
    @login_required
    def enviar_mensagem(destinatario_id):
        destinatario = User.query.get_or_404(destinatario_id)
        
        if request.method == 'POST':
            conteudo = request.form.get('conteudo')
            if not conteudo:
                flash('A mensagem não pode estar vazia.', 'danger')
                return redirect(url_for('enviar_mensagem', destinatario_id=destinatario_id))

            mensagem = Mensagem(
                remetente_id=current_user.id, 
                destinatario_id=destinatario_id, 
                conteudo=conteudo
            )
            
            try:
                db.session.add(mensagem)
                db.session.commit()
                flash('Mensagem enviada com sucesso!', 'success')
                return redirect(url_for('chat', destinatario_id=destinatario_id))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao enviar mensagem.', 'danger')
                print(f"Erro ao enviar mensagem: {e}")
        
        return render_template('enviar_mensagem.html', destinatario=destinatario)

    # Adicione a rota que está faltando para enviar mensagem sobre doação específica
    @app.route('/enviar_mensagem_doacao/<int:doacao_id>/<int:destinatario_id>', methods=['GET', 'POST'])
    @login_required
    def enviar_mensagem_doacao(doacao_id, destinatario_id):
        destinatario = User.query.get_or_404(destinatario_id)
        doacao = Doacao.query.get_or_404(doacao_id)
        
        # Preparar mensagem pré-preenchida sobre a doação
        mensagem_pre_preenchida = f"Olá! Estou interessado(a) na sua doação de {doacao.quantidade} litros de leite materno. Podemos conversar sobre isso?"
        
        if request.method == 'POST':
            conteudo = request.form.get('conteudo')
            if not conteudo:
                flash('A mensagem não pode estar vazia.', 'danger')
                return redirect(url_for('enviar_mensagem_doacao', doacao_id=doacao_id, destinatario_id=destinatario_id))

            mensagem = Mensagem(
                remetente_id=current_user.id, 
                destinatario_id=destinatario_id, 
                conteudo=conteudo
            )
            
            try:
                db.session.add(mensagem)
                db.session.commit()
                flash('Mensagem enviada com sucesso!', 'success')
                return redirect(url_for('chat', destinatario_id=destinatario_id))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao enviar mensagem.', 'danger')
                print(f"Erro ao enviar mensagem: {e}")
        
        return render_template('enviar_mensagem_doacao.html', 
                              destinatario=destinatario, 
                              doacao=doacao, 
                              mensagem_pre_preenchida=mensagem_pre_preenchida)

    # Adicione esta nova rota para o chat
    @app.route('/chat/<int:destinatario_id>')
    @login_required
    def chat(destinatario_id):
        destinatario = User.query.get_or_404(destinatario_id)
        
        # Verificar se é uma conversa entre doador e receptor
        if current_user.tipo == destinatario.tipo:
            flash('Você só pode conversar com usuários do tipo oposto ao seu.', 'danger')
            return redirect(url_for('caixa_de_entrada'))
        
        # Marcar mensagens como lidas
        Mensagem.query.filter_by(
            destinatario_id=current_user.id,
            remetente_id=destinatario_id,
            lida=False
        ).update({'lida': True})
        db.session.commit()
        
        # Buscar todas as mensagens entre os dois usuários
        mensagens = Mensagem.query.filter(
            ((Mensagem.remetente_id == current_user.id) & (Mensagem.destinatario_id == destinatario_id)) |
            ((Mensagem.remetente_id == destinatario_id) & (Mensagem.destinatario_id == current_user.id))
        ).order_by(Mensagem.timestamp.asc()).all()
        
        return render_template('chat.html', 
                            destinatario=destinatario, 
                            mensagens=mensagens)

    # Modifique a caixa de entrada para mostrar conversas
    @app.route('/caixa_de_entrada')
    @login_required
    def caixa_de_entrada():
        mensagens = Mensagem.query.filter(
            (Mensagem.remetente_id == current_user.id) |
            (Mensagem.destinatario_id == current_user.id)
        ).order_by(Mensagem.timestamp.desc()).all()

        conversas_dict = {}
        for msg in mensagens:
            id1 = msg.remetente_id
            id2 = msg.destinatario_id
            outro_id = id2 if id1 == current_user.id else id1
            chave = tuple(sorted([id1, id2]))  # garante unicidade da conversa

            if chave not in conversas_dict:
                outro_user = User.query.get(outro_id)
                nao_lidas = Mensagem.query.filter_by(
                    remetente_id=outro_id,
                    destinatario_id=current_user.id,
                    lida=False
                ).count()

                conversas_dict[chave] = {
                    'user': outro_user,
                    'ultima_msg': msg,
                    'nao_lidas': nao_lidas
                }

        conversas = list(conversas_dict.values())
        return render_template('caixa_de_entrada.html', conversas=conversas)
    
    @app.route('/reservar_doacao/<int:doacao_id>')
    @login_required
    def reservar_doacao(doacao_id):
        if current_user.tipo != 'receptor':
            return redirect(url_for('index'))
        
        doacao = Doacao.query.get_or_404(doacao_id)
        
        if not doacao.disponivel:
            flash('Esta doação já foi reservada por outra pessoa.', 'warning')
            return redirect(url_for('buscar_doadores'))
        
        try:
            doacao.disponivel = False
            doacao.receptor_id = current_user.id
            db.session.commit()
            
            # Enviar mensagem automática ao doador
            mensagem = Mensagem(
                remetente_id=current_user.id,
                destinatario_id=doacao.doador_id,
                conteudo=f"Olá! Eu reservei sua doação de {doacao.quantidade} litros. Vamos combinar os detalhes?"
            )
            db.session.add(mensagem)
            db.session.commit()
            
            flash('Doação reservada com sucesso! Uma mensagem foi enviada ao doador.', 'success')
            return redirect(url_for('chat', destinatario_id=doacao.doador_id))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao reservar doação.', 'danger')
            print(f"Erro ao reservar doação: {e}")
            return redirect(url_for('buscar_doadores'))
        
    @app.route('/buscar_doadores', methods=['GET', 'POST'])
    @login_required
    def buscar_doadores():
        if current_user.tipo != 'receptor':
            return redirect(url_for('index'))

        if request.method == 'POST':
            receptor_lat = current_user.latitude
            receptor_lon = current_user.longitude

            # Buscar doações disponíveis com seus doadores
            doacoes_disponiveis = Doacao.query.filter_by(disponivel=True).join(User, Doacao.doador).all()

            doadores_proximos = []
            for doacao in doacoes_disponiveis:
                doador = doacao.doador
                distancia = calcular_distancia(receptor_lat, receptor_lon, doador.latitude, doador.longitude)
                if distancia <= 50:
                    doadores_proximos.append({
                        'doador': doador,
                        'distancia': distancia,
                        'doacao': doacao
                    })

            # Ordenar por distância
            doadores_proximos.sort(key=lambda x: x['distancia'])

            return render_template('buscar_doadores.html', doadores=doadores_proximos)

        return render_template('buscar_doadores.html')
    
    # Adicione a rota para confirmar reserva
    @app.route('/confirmar_reserva/<int:doacao_id>')
    @login_required
    def confirmar_reserva(doacao_id):
        if current_user.tipo != 'receptor':
            return redirect(url_for('index'))
        
        doacao = Doacao.query.get_or_404(doacao_id)
        doador = User.query.get_or_404(doacao.doador_id)
        
        if not doacao.disponivel:
            flash('Esta doação já foi reservada por outra pessoa.', 'warning')
            return redirect(url_for('buscar_doadores'))
        
        return render_template('confirmar_reserva.html', doacao=doacao, doador=doador)
    
    @app.route('/marcar_como_lida/<int:mensagem_id>')
    @login_required
    def marcar_como_lida(mensagem_id):
        mensagem = Mensagem.query.filter_by(id=mensagem_id, destinatario_id=current_user.id).first_or_404()
        try:
            mensagem.lida = True
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return '', 500
