# API de Geração de Certificados

Este projeto é uma API desenvolvida com FastAPI para gerar certificados personalizados em formato PDF. A API utiliza modelos de certificados pré-definidos e permite adicionar o nome do destinatário e um número de série único em cada certificado.

## Funcionalidades

- Geração de certificados com nome personalizado.
- Adição de número de série único no verso do certificado.
- Retentativas automáticas em caso de falhas, utilizando a biblioteca Tenacity.
- Retorno do certificado em formato PDF para download.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **FastAPI**: Framework para construção da API.
- **Pillow**: Biblioteca para manipulação de imagens.
- **FPDF**: Biblioteca para geração de arquivos PDF.
- **Tenacity**: Biblioteca para implementar retentativas automáticas.

## Como Executar o Projeto

1. Clone o repositório:

   ```bash
   git clone https://github.com/daviiisousa/api-certificado.git
   cd api-certificado
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

### POST `/gerar-certificado`

Gera um certificado personalizado.

#### Parâmetros:

- **nome** (string): Nome do destinatário do certificado.

#### Exemplo de Requisição:

```json
{
  "nome": "João da Silva"
}
```

#### Resposta:

- Retorna um arquivo PDF com o certificado gerado.

## Estrutura do Projeto

- `main.py`: Código principal da API.
- `modelo_certificado_frente.png`: Modelo da frente do certificado.
- `modelo_certificado_verso.png`: Modelo do verso do certificado.
- `Montserrat-Bold.ttf`: Fonte utilizada nos certificados.
- `requirements.txt`: Arquivo com as dependências do projeto.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT.
