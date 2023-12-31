# UFRPE_CG
Projeto de conclusão da disciplina Computação Gráfica Básica.
![](static/animation.gif)
## Especificação
Carregar na memória uma malha de triângulos referente a um objeto 3D armazenada em
arquivo de texto e desenhar seus vértices na tela. O arquivo utilizado para armazenar uma
malha com n vértices e k triângulos possui o seguinte formato:
```
<no de vértices> <no de triângulos>
<coordenada x do vértice 1> <coordenada y do vértice 1> <coordenada z do vértice 1>
<coordenada x do vértice 2> <coordenada y do vértice 2> <coordenada z do vértice 2>
...
<coordenada x do vértice n> <coordenada y do vértice n> <coordenada z do vértice n>
<índice do vértice 1 do triângulo 1> <índice do vértice 2 do triângulo 1> <índice do vértice 3 do triângulo 1>
<índice do vértice 1 do triângulo 2> <índice do vértice 2 do triângulo 2> <índice do vértice 3 do triângulo 2>
...
<índice do vértice 1 do triângulo k> <índice do vértice 2 do triângulo k> <índice do vértice 3 do triângulo k>
```
Exemplo de arquivo:
```
4 4
1 1 1
1 30 1
30 30 1
1 1 30
1 2 3
1 2 4
2 3 4
1 3 4
```

Uma vez que a malha foi carregada na memória, deve-se obter a projeção em perspectiva de seus vértices.  
A aplicação lê os parâmetros da câmera virtual do arquivo `cam.properties`.
### cam.properties
| propriedade | tipo | descrição |
| :---: | :---: | :--- |
| Nx | numérico | Componente x do vetor N da base.
| Ny | numérico | Componente y do vetor N da base.
| Nz | numérico | Componente z do vetor N da base.
| Vx | numérico | Componente x do vetor V da base.
| Vy | numérico | Componente y do vetor V da base.
| Vz | numérico | Componente z do vetor V da base.
| Cx | numérico | Componente x do ponto focal.
| Cy | numérico | Componente y do ponto focal.
| Cz | numérico | Componente z do ponto focal.
| d  | numérico | Distância do plano de vista.
| hx | numérico | Largura do retângulo de vista.
| hy | numérico | Altura do retângulo de vista.

## Instalação
Desenvolvido em Python 3.10.12  
pygame 2.5.2
```bash
$ pip install -r requirements.txt
```
```bash
python main.py <1>
```
O argumento <1> é o nome do arquivo contendo a malha triangular que deve estar contido em ./data
Por exemplo:
```bash
python main.py 'calice2.byu'
```

## Funcionamento
Uma vez que a malha foi carregada e a aplicação está rodando existem alguns comandos para visualizar diferentes tipos de renderização.  
| comando | descrição |
| :---: | :--- |
1 | Apenas os pontos em coordenadas de tela
2 | Linhas do algoritmo de Bresenham
3 | Sólido sem iluminação pelo Scanline
