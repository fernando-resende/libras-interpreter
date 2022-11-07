# Interpretador de Libras - Linguagem Brasileira de Sinais

## Sobre

Interpretador, em tempo real, do alfabeto em libras.

Até o momento, apenas caracteres de gestos estáticos são interpreatados, portanto caracteres como J, X e Z não são reconhecidos.

Referência da execução dos gestos do alfabeto manual em libras: [http://www.spreadthesign.com/pt.br/alphabet/11/](http://www.spreadthesign.com/pt.br/alphabet/11/)

Representação do alfabeto manual:

![Alfabeto manual de libras](https://s1.static.brasilescola.uol.com.br/img/2019/09/alfabeto.png)

**Fonte:** [https://brasilescola.uol.com.br/educacao/lingua-brasileira-sinais-libras.htm](https://brasilescola.uol.com.br/educacao/lingua-brasileira-sinais-libras.htm)

## Como executar

Caso queira utilizar a versão simplificada, direto via navegador, acesse o [projeto no Colab](https://colab.research.google.com/github/fernando-resende/libras-interpreter/blob/main/LibrasInterpreter.ipynb). Essa versão detecta e interpreta a letra correspondente ao sinal feito com a mão.

Para executar em sua máquina, no diretório desejado, utilize o comando `git clone https://github.com/fernando-resende/libras-interpreter.git` ou realize o [download](https://github.com/fernando-resende/libras-interpreter/archive/refs/heads/main.zip) do projeto na branch principal e descompacte onde preferir.

Para instalar as dependências necessárias, execute via console o comando `git install -r requirements.txt` no local onde foi clonado ou descompactado o projeto.

Finalizadas as intalações das dependências execute o arquivo *librasinterpreter.py*.

## Como utilizar

O [projeto no Colab](https://colab.research.google.com/github/fernando-resende/libras-interpreter/blob/main/LibrasInterpreter.ipynb) detecta e interpreta a letra correspondente ao sinal feito com a mão apresentando no vídeo a letra que o modelo de machine learning julga ser a correta.

Já a versão que executa na máquina tem, além da detecção e interpretação a possibilidade de gerar datasets para novos treinamentos. Pressione *Tab* a qualquer momento da execução para alternar entre os modos de Detecção (*Detection*) e de base de dados (*Dataset*). No modo *Dataset* prepare o sinal manual e pressione no teclado a tecla correspondente para iniciar a captura de *x* imagens.

Durante a geração de *dataset* a sugestão é inclinar, afastar, aproximar e girar a mão durante a coleta de imagens para generalizar as amotras e, consequentemente, aumentar as chances de produção de modelos mais eficientes

Caso seja pressionada a tecla *ESC* o sistema será encerrado.

## Proposta de evolução futura

Implementar identificação dos caracteres que exigem movimento e, porteriormente, gestos  que significam palavras inteiras.