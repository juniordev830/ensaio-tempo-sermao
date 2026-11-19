# Tempo de ensaio do sermão

Estime a duração de cada bloco e descubra quanto precisa ajustar para caber no horário.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Use os textos reais do ensaio, sua velocidade em palavras por minuto e as pausas em segundos. O resultado arredonda cada bloco para cima e informa folga ou excesso.

## Fontes e exemplos

Os exemplos incluem referências bíblicas, perguntas e anotações de demonstração. Consulte o texto e o contexto em uma [tradução publicada pela Sociedade Bíblica do Brasil](https://www.sbb.org.br/traducoes-da-biblia). Para aprofundar, o catálogo da [Nova Bíblia de Estudo Almeida](https://www.sbb.org.br/nova-almeida/biblias-de-estudo/biblia-de-estudo-almeida) e o do [Comentário Bíblico Pentecostal do Novo Testamento, CPAD](https://www.cpad.com.br/comentario-biblico-pentecostal-novo-testamento-/p) ajudam a identificar edições. Registre as páginas verificadas na sua própria consulta.

## Capítulos para uma gravação do ensaio

Gere uma faixa WebVTT com o início e o fim estimados de cada bloco. As pausas
entram na duração do bloco correspondente. Blocos de zero segundos são omitidos.
O exportador usa Perl 5 com o módulo padrão JSON::PP.

```sh
python app.py exemplo.json | perl capitulos.pl > ensaio.vtt
```

Use o arquivo como faixa de capítulos em um player compatível. Os tempos seguem
a estimativa do roteiro e podem diferir da gravação real.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar os tempos de cada bloco do ensaio. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```
