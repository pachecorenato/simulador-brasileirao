# Preditor Analítico do Brasileirão

##  Visão Geral
Este projeto é um sistema Full-Stack orientado a dados projetado para coletar, armazenar e processar históricos do Campeonato Brasileiro, fornecendo simulações estatísticas de probabilidade de vitória em confrontos diretos. O objetivo central é demonstrar o ciclo de vida completo do dado: desde a extração automatizada na web (ETL) até a entrega de valor visual e interativa para o usuário final.

##  Arquitetura do Sistema e Stack Tecnológica
O ecossistema da aplicação foi rigorosamente dividido em camadas para garantir a separação de responsabilidades (Separation of Concerns):

*   **Extração de Dados (Web Scraping):** Implementado com **BeautifulSoup** para a navegação, extração estruturada e higienização dos dados diretamente da web.
*   **Persistência (Banco de Dados):** Utiliza **SQLite** acoplado ao ORM **SQLAlchemy**, garantindo operações seguras, *upserts* inteligentes e modelagem relacional limpa.
*   **Motor Analítico (Data Science):** O cérebro matemático da aplicação é gerido pelo **Pandas**, responsável por cruzar as informações do banco e calcular a força probabilística das equipes de forma vetorizada e ágil.
*   **Backend (API RESTful):** Desenvolvido em **Flask** para expor os cálculos matemáticos em endpoints dinâmicos, devolvendo estruturas organizadas em JSON.
*   **Frontend (Interface do Usuário):** Construído com **HTML5, CSS moderno e JavaScript vanilla**, consumindo a API de forma assíncrona para uma experiência de usuário responsiva e livre de recarregamentos (Single Page Application behavior).

##  Como rodar localmente

Siga os passos abaixo para configurar e executar todo o ecossistema na sua máquina:

1. Clone este repositório para o seu ambiente local:
   
git clone (https://github.com/pachecorenato/simulador-brasileirao.git) 


##  Inteligência Artificial e Pair Programming
Este projeto foi desenvolvido utilizando conceitos de IA assistida (AI-Assisted Development). Ferramentas de Inteligência Artificial foram utilizadas estrategicamente atuando como "Pair Programming" para:

* **Refatoração:** Auxílio na estruturação do código seguindo boas práticas de POO e Modularização.
* **Troubleshooting:** Depuração ágil de erros de sintaxe e dependências de bibliotecas.
* **Estilização:** Geração eficiente de paletas de cores e propriedades do CSS (Vanilla) para a interface.
* **Documentação:** Estruturação de Docstrings e formatação inicial deste arquivo README.

Vale ressaltar que toda a arquitetura de software, lógica de negócios, regras de integração de dados e engenharia de prompt foram concebidas, orquestradas e validadas por mim.

## Conclusão e Boas Práticas Técnicas
A arquitetura deste software foi desenhada focando estritamente em padrões de mercado, com forte ênfase em Orientação a Objetos (POO) e Modularização.

Ao isolar a inteligência de coleta, o esquema do banco de dados, o motor analítico e o servidor Flask em módulos independentes, o sistema evita o anti-padrão de "código espaguete". Essa abordagem garante uma base de código escalável, testável e de fácil manutenção, qualidades fundamentais para a engenharia de software de nível de produção.
