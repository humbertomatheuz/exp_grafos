# 🚀 Comparador de Algoritmos de Rota (BFS, Dijkstra, A\*)

Este projeto é um script em Python que implementa e compara o desempenho dos algoritmos de busca **BFS**, **Dijkstra** e **A**\* para encontrar a rota mais curta em uma malha viária real.

O script utiliza a biblioteca `osmnx` para baixar o mapa da cidade de **Recife, Pernambuco**, e o `networkx` para executar os algoritmos.

## 📦 Instalação (Requisitos)

Este projeto usa Python 3. Você precisará instalar as bibliotecas principais para que o script funcione.

Abra seu terminal e execute o seguinte comando para instalar todas as dependências necessárias de uma vez:

```bash
pip install osmnx networkx matplotlib scikit-learn
```
## ⚙️ Como Usar

1.  **Execute o Script:**
    Abra um terminal na pasta do projeto e execute o arquivo principal:

    ```bash
    python main.py
    ```
2.  **Cache do Mapa (Primeira Execução):**

      * Na primeira vez que você rodar, o script irá baixar o mapa completo de Recife. Isso pode demorar 1 ou 2 minutos.
      * Ele salvará o mapa em um arquivo (ex: `recife.graphml`) na mesma pasta.
      * Nas próximas vezes, o script carregará o mapa desse arquivo em poucos segundos.

3.  **Insira o Ponto A (Origem):**

      * O terminal pedirá o `>> Ponto A (Origem):`.
      * Vá ao Google Maps, clique com o botão direito no local de partida e copie as coordenadas.
      * Cole no terminal (ex: `-8.106842945601155, -34.91479963932876`) e pressione Enter.

4.  **Insira o Ponto B (Destino):**

      * Repita o processo para o `>> Ponto B (Destino):`.

-----

## 🗺️ O que esperar (Saída)

Após inserir os dois pontos, o script irá:

1.  **Exibir uma Tabela:** Mostrará no terminal uma tabela comparando os três algoritmos (Tempo, Nós na Rota, Distância).

    ```
    =================================================================
    Algoritmo       | Tempo (s)    | Nós na Rota  | Distância (m)
    -----------------------------------------------------------------
    BFS             | 0.13812      | 149          | 12479.8
    Dijkstra        | 0.47310      | 178          | 11023.1
    A*              | 0.22152      | 178          | 11023.1
    =================================================================
    ```

2.  **Abrir um Mapa:** Uma nova janela será aberta (usando Matplotlib) mostrando o mapa de Recife, a rota calculada (em ciano), o ponto A (verde) e o ponto B (vermelho).