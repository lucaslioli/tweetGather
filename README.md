# tweetGather

## Requisitos

Para instalação dos requisitos necessários utilizar um dos comandos:

```
$ pip3 install -r requirements.txt
$ pip2 freeze > requirements.txt
```

Criar conta na plataforma [Twitter Developers](https://developer.twitter.com/en.html) e gerar as chaves e tokens de acesso. Criar um arquivo ```helper/authenticate.py``` com a seguinte estrutura:

```python
def api_tokens(verify):
  keys = {}
  if(verify == "Gather"):
    keys['consumer_key'] 		= "consumer_key"
    keys['consumer_secret'] 	= "consumer_secret"
    keys['access_token'] 		= "access_token"
    keys['access_token_secret'] = "access_token_secret"

    return keys
```

---
### Trabalho de Concolusão de Curso - [PDF](https://github.com/lucaslioli/ufsm-tcc-si-2018/raw/master/tcc-lucas.pdf):
**Título:** Utilização de algoritmos de aprendizado de máquina para prever a popularidade de tuítes

**Orientador:** Sérgio Luís Sardi Mergen

**Instituição:** Universidade Federal de Santa Maria ([UFSM](http://ufsm.br))

**Repositório:** [ufsm-tcc-si-2018](https://github.com/lucaslioli/ufsm-tcc-si-2018)

---
### Artigo publicado no ERBD 2018 - [PDF](http://erbd2018.c3.furg.br/downloads/180198_1.pdf)
**Título:** Análise da Popularidade de Tuítes com Base em Características Extraídas de seu Conteúdo

**Orientador:** Sérgio Luís Sardi Mergen

**Instituição:** Universidade Federal de Santa Maria ([UFSM](http://ufsm.br))

🏆 **Premiação:** Melhor artigo de pesquisa do evento

**Arquitetura do projeto**
![IMG](https://raw.githubusercontent.com/lucaslioli/tweetGather/master/display/assets/arquitetura.png)
