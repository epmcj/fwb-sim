Para simular as transmissões de dados nas redes, utilizamos um modelo físico em baseado no SINR (Signal-to-Noise-plus-Interference Ratio).
Assim, um pacote transmitido pode ser decodificado se o SINR no receptor for maior do que \Beta

    SINR  =  Pu / d(u,v)^\alpha / (N + \sum {w \in V \\ {u}} (Pw / d(w, v)^\alpha)) >= \Beta

sendo,

    Pu          := potencia de transmissão do no u

    d(u,v)      := distância entre nos u e v mínima entre um nó pai e um filho

    \alpha      := expoente de path-loss

    \Beta       := SIN mínimo

    N           := ruido

    \sum [...]  := interferência

---

Para as simulações, utilizou-se:

\Beta  = 1

\alpha = 3

N      = P / (2 * \Beta * (2 * Rtx)**\alpha) [baseado em "Local Broadcasting in the Physical Interference Model"]

Parâmetros baseados no rádio CC2420:
    Rtx := Alcance de transmissão dos nos (= 30 m)
    P := Potência de transmissão (= 0 dBm)
    Taxa de transmissão = 250 kbps

---
Para simular diferentes larguras de banda, associamos a taxa de transmissão de 250 kbps à menor delas e aumentamos essa taxa de forma proporcional ao aumento da largura de banda.
Por exemplo, 
-  2 MHz => 250 kbps
-  4 MHz => 500 kbps
-  8 MHz =>   1 Mbps
- 16 MHz =>   2 Mbps

FWBI utiliza um UDG para representar a interferência na rede e assim distribuir os timeslots. 
O alcance de interferência (Ri) é dado por

    Ri = Rx * i

sendo
    i := coeficiente de interferência

Geração de Redes para Testes:
- Árvores Binárias Balanceadas de altura $l$ foram geradas da forma descrita a seguir.
  Primeiro, atribuiu-se uma posição inicial para o nó sorvedouro.
  Em seguida, as posições de seus dois nós filhos foram determinadas a partir de pares (\theta_1, d_1) e (\theta_2, d_2) tal que
    0 <= \theta_1 <= \pi / 2,
    0 >= \theta_2 >= -\pi / 2 e
    d_{min} <= d_1, d_2 <= d_{max},
  sendo 
  d_{min} := distância mínima entre um nó pai e um nó filho (=  2 m)
  d_{max} := distância máxima entre um nó pai e um nó filho (= 20 m)
  As posições dos nós filhos são utilizadas recursivamente como base para gerar a posição dos próximos nós filhos até que uma árvore de altura $l$ seja obtida.

- Árvores Aleatórias com $n$ nós são geradas através do seguinte procedimento.
  Determina-se primeiramente uma posição inicial para o nó sorvedouro.
  Então, os nós do nível (i+1) são gerados com base nos nós do nível (i) da seguinte forma:
    Para cada nó do nível $i$, escolhe-se um número aleatório de filhos para ele entre c_{min} e c_{max} (e obdecendo o máximo de $n$ nós na rede).
    Em seguida, escolhe-se um par aleatório (\theta, d) para cada um dos filhos, tal que 
      \pi / 2 >= \theta >= -\pi / 2 e
      d_{min} <= d <= d_{max},

- Árvores Binárias Degeneradas de altura $l$ são geradas a partir de árvores binárias balanceadas de altura $l-1$.
  Adiciona-se um novo nó sorvedouro a elas e o conecta ao antigo sorvedouro, criando assim um enlace gargalo na rede.
  A posição deste novo nó é determinada através do par aleatório (\theta, d), com as seguintes restrições
    \pi / 2 <= \theta <= 3 * \pi / 2 e
    d_{min} <= d <= d_{max},