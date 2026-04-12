# 📝 ProntNote: Prontuário do Paciente de Fácil Acesso

O **ProntNote** é um sistema web intuitivo desenhado para devolver ao paciente o controle total sobre o seu acompanhamento médico. 

Com a nossa plataforma, o paciente centraliza todas as suas informações de saúde em um único histórico (como exames, prescrições e anotações) e pode conceder acesso temporário e seguro para que os médicos visualizem esses dados.

---

### ⚙️ Como configurar a API (Passo a Passo)

Siga os passos abaixo para configurar o ambiente de desenvolvimento e rodar a aplicação na sua máquina.

**1. Criação do Ambiente Virtual (Virtual Environment)**
É altamente recomendável criar um ambiente virtual. Ele funciona como uma "bolha" que isola as ferramentas deste projeto, evitando conflitos com outros projetos no seu computador.
No terminal, execute o comando:
```bash
python -m venv venv
```

**2. Ativação do Ambiente Virtual**
Para "entrar" nessa bolha que acabamos de criar, ative o ambiente virtual:

* **Mac/Linux:**
```bash
source venv/bin/activate
```
* **Windows:**
```bash
venv\Scripts\activate
```

**3. Instalação das Dependências**
Com o ambiente ativado, vamos instalar as bibliotecas necessárias para o projeto funcionar (elas estão listadas no arquivo `requirements.txt`):
```bash
pip install -r requirements.txt
```

**4. Execução do Sistema**
Pronto, o ambiente está preparado! Certifique-se de que você está na pasta raiz do projeto (`prontnote-back`) e inicie a aplicação:
```bash
python app.py
```
> **💡 O que acontece nos bastidores?** > Esse único comando é inteligente: ele configura todo o ambiente, cria as tabelas do banco de dados (schema), insere alguns dados de teste (seed) e coloca a API no ar!
---

Utilize os seguintes dados cadastrais para testes:

email: paciente@teste.com

senha: 12345

---

**5. Visualização da Documentação (Swagger)**
Com o servidor rodando, você pode testar as rotas de forma visual e interativa. Basta abrir o seu navegador e acessar o link abaixo:

👉 [http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)
