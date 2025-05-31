# Modelo Entidade-Relacionamento

---

## Introdução

De acordo com **Silberschatz (2006, p.13)**, um *Modelo Entidade-Relacionamento (MER)* serve para delinear objetos do mundo real. Esses objetos são denominados *Entidades* e as associações existentes entre esses ojetos são denominadas *Relações*. Dessa forma, o conjunto de entidades é denominado *Conjunto de Entidades* e o conjunto das relações é denominado *Conjunto de Relacionamentos*.  

Cada entidade possui um *atributo* ou um conjunto de atributos que são usados para identificar as características dessa entidade.

Um *Diagrama Entidade-Relacionamento (DER)* é um esquema para representar graficamente um MER. Ele é composto por:  

- **Retângulos**: Representam os conjuntos de entidades;  
- **Elipses**: Representam os atributos;  
- **Losângos**: Representam o conjunto de relacionamento entre as entidades;  
- **Linhas**: Une os atributos às entidades e o conjunto de entidades aos relacionamentos;  
- **Triângulos**: Conjunto de relacionamentos do tipo generalização.

O conjunto de relacionamento pode ser também do tipo *generalização*. A generalização é um relacionamento que liga um conjunto de entidades de nível superior à um conjunto de entidades de nível inferior, que compartilham os atributos das entidades superiores. A generalização pode ser classificada de acordo com o tipo de restrição. Ela pode ser de (**Silberschatz (2006, p.194)**):  

- **Participação Total (T)**: Uma entidade de nível superior deve pertencer a pelo menos uma entidade de nível inferior;  
- **Participação Parcial (P)**: Uma entidade de nível superior pode não pertencer a nenhuma entidade de nível inferior.  

E também:  

- **Exclusivo (E)**: Onde a entidade de nível superior não pode pertence a mais de uma entidade de nível inferior;  
- **Sobreposição (S)**: Onde a entidade de nível superior pode pertence a várias entidades de nível inferior.  

Assim sendo, a generalização pode aparecer de quatro formas:  

- Total Exclusivo (T, E);
- Total Sobreposto (T, S);
- Parcial Exclusivo (P, E);
- Parcial Sobreposto (P, S).

E, por fim, "Agregação é uma abstração por meio da qual os relacionamentos são tratados como entidades de nível superior" **Silberschatz (2006, p.196)**. Ela é representada por uma caixa retangular que envolve os conjuntos de entidades e seus relacionamentos.



## Metodologia

Para o desenvolvimento do Modelo Entidade-Relacionamento (MER) do **Marventura**, foi necessário seguir uma abordagem estruturada que garantisse clareza e organização ao longo do processo. Inicialmente, foi realizado um estudo aprofundado sobre modelagem de dados e, mais especificamente, sobre o modelo entidade-relacionamento. Foram analisados conceitos fundamentais como entidades, relacionamentos, atributos, cardinalidade e normalização. Esse estudo permitiu definir uma base sólida para a construção de um modelo coerente e aderente às boas práticas de design de banco de dados.

Com o embasamento teórico estabelecido, foi iniciada a etapa de definição das características do jogo. Neste ponto, foram tomadas decisões importantes relacionadas ao contexto narrativo e mecânico do jogo, como o gênero, os personagens principais, ambientação e elementos-chave de jogabilidade. Esse direcionamento forneceu um norte para identificar quais entidades e relações seriam relevantes para o sistema do jogo.

Para facilitar tanto a visualização quanto a modelagem do MER, optou-se por dividir o modelo em temas. Essa divisão temática permitiu organizar o projeto em partes menores, cada uma representando um domínio específico do jogo, como personagens, itens, missões, localidades e progressão do jogador. Essa segmentação foi essencial para reduzir a complexidade visual do diagrama completo, além de ajudar a manter uma estrutura lógica e modular, facilitando futuras expansões e manutenções.

Essa abordagem incremental e organizada tornou possível construir um modelo claro, consistente e alinhado com os objetivos do jogo, ao mesmo tempo em que respeita os princípios da boa modelagem de dados.



## Diagrama Entidade-Relacionamento

A **Figura 1** abaixo apresenta o diagrama Entidade-Relacionamento pensado para representar os itens do inventário do jogador, que vão desde os itens equipáveis e não-equipáveis, como moedas (não-equipável) e espadas (equipável), ambos não consumíveis, e itens consumíveis, como os itens de recuperação de vida e energia.

<details open>
  <summary>Figura 1 – Diagrama Entidade-Relacionamento dos Itens do Inventário
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 1 – Diagrama Entidade-Relacionamento dos Itens do Inventário</strong></p>
    <img src="../assets/diagrama-entidade-relacionamento-item-v2.3.png">
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

Os efeitos *Cura* e *Recuperação de energia* são aqueles obtidos através de itens consumíveis e são usados para recuperar os pontos que foram perdidos desses atributos, sem ultrapassar o máximo, enquanto os efeitos *Aumento de vida* e *Aumento de energia* são aplicáveis aos acessórios e servem para aumentar o limite máximo desses atributos. Ademais, *Ataque* e *Sorte* aplicam-se a ambos. Todos esses efeitos possuem três tipos: pequeno, médio e grande, que estão relacionados com as raridades ★, ★★ e ★★★, respectivamente, com excessão de *Sorte* que possui apenas um nível.

---

A **Figura 2** abaixo apresenta o diagrama Entidade-Relacionamento com foco nos personagens que abarca tanto o personagem jogável, que é o próprio jogador, quanto os personagens não-jogáveis, que são os inimigos e os habitantes.

<details open>
  <summary>Figura 2 – Diagrama Entidade-Relacionamento dos Personagens
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 2 – Diagrama Entidade-Relacionamento dos Personagens</strong></p>
    <iframe src="https://viewer.diagrams.net/?lightbox=1&highlight=0000ff&nav=1&title=Diagrama%20de%20personagem.drawio&dark=0#R%3Cmxfile%20pages%3D%222%22%3E%3Cdiagram%20id%3D%227o4wIIwqFHXamwNt6cy-%22%20name%3D%22DER%22%3E7V1Zd6JK1%2F41Wf1%2BF2YxD5eJmTvz0Emfm16oqCQKBjEm%2BfUfKBip2hSIVQV0J6tPTkRA3FPt%2FdQeduT2%2BP3YtybDC69nj3Ykofe%2BIx%2FsSJKhS%2BHv6MDH8oAqycsDA9%2FpLQ%2BJXwfunE87PijER2dOz56mTgw8bxQ4k%2FTBrue6djdIHbN835unT%2Bt7o%2FSnTqyBjR2461oj%2FOij0wuG8deS9K%2FjJ7YzGCafLGrm8p2xlZwcf5Pp0Op587VD8uGO3PY9L1j%2BNX5v26OIdgldltcdZby7ejDfdoMiFzxeiqORr6jPs3H37vny6OhSPmwp8bMFH8kXtnvh949fen4w9Aaea40Ov47u%2B97M7dnRXYXw1dc55543CQ%2BK4cFnOwg%2BYmZas8ALDw2D8Sh%2B1353gqe1v39Ht9qV1PjlwXt868WLj%2BSFG%2FgfT%2Bsvlpepycuvyxavvq7r7UVyEL50PTd6%2Fmlg%2BcGRMxrFZ%2BCEjGk79WZ%2BNyZL72l2cDN5fhf%2Fe3v8T7n4OP3v6q2VCKTlD%2ByAQOVYByLSrn1AzKZj2xvb4ROHJ%2Fj2yAqct7ToWbEED1bnfTE5%2FCPmM8xz0lO%2FWaNZ%2FEnXtj8NOTiwx5g4zIdOYN9NrAUd5qGKp1lpjZyBG%2F7dDWln%2ByRivtl%2BYL8Tv378rinHGhObDFmIX8%2B%2FFFBMjg3XlE8RtqfY6fjl2hVvOvNAnt1oJ7d%2FxKEBUKwStWEoyRIuySTZ4S%2FJP%2F1P6aYXeGoneJAPptZgaLgt7V%2FkCyihKm2%2BLC4Nv5b1sXbCxHPcYLp25%2BvowJrmGmnNVdAlCTlf3%2FZ8TUBkaPnEXxK1%2BurlhUyvcomM17d4kRTJK2T4IrTkTviFI1OMrJpfC%2BXv1DrJf9UsKtNKI2Va1onns5FRsxq7x0q2aEk%2FexnVGimjoky%2BYGshJdGUtFpHTqITBl%2FnVsceXXtTJ3C8yL3seEHgjUOOJifsxX5n4CEOaRhlTaKbjd8HUTy627GmTnfX6s4C%2B0%2FgO5Y7WAj%2FIj5dipc1nSwDx77zHqkDFRdWNXZVzfz6STu0Ou7QKtKuoeEurczKpZUxZrSHdt%2FGOFKB%2F7%2BK%2FRPIwKja%2F1cwYp26ztgZeHUglywhuqxUTS4VI9eZN7B6nr81uWJDGF6r7of%2Fwi%2FQTv%2BnhndtJ%2B9EkEL2m6T39Ow3Rfgd9LOAN7OuJF1Iuk4nXahnXylmXiaSqCYSqCaSqCZCTxL%2BoyL9OgIWVC%2F9eFB6YnWcwApFuA7mQpSrpBjoveLwyoU1sepALNWsEIoCaYU7UYfTYKct7%2ByJGMESX8gfeuPObBrZzzUHOT665jPvV0BhXU1TWDIBCksAhTVm0oiL42lQD2RU1GsnjyK%2B2GOUqgUGlxWtriLZjGg1k23rMSRMmnglqCiIBKI%2BXd9V5LTxNxHBWD5sfCUiGxSACtFsuLjkgRvPs%2FEkeXjL71IXIPhEg4kEbQpDYLCCmsZn8QtUNNTjAeiuNmT%2FErSsGpHTGypyklqByIkFdqr%2BFuxLlCPwSxdWP1Ka3iLusjAEv4jCu8aOW7vrzwIqIAUNGkoCIqU8MTDiGrNGs192ZBJrQrFkL7A%2BFJPwQOJ%2F1xEkIgmH%2F4fRLPyewcK4%2B96L3fZGnv9l8fuhsUcOTUPqOu7g3O5HX0P5OnIbf7PokBfSrz9arB1Dp9ez3cVCFliB1Vl8rJABqYW2AUV9EshmEi59bc8NH9NyFsyyrWkwt6fRs%2Fc9N4jXP1HKDyep2BokIAKtC8B0ZqYlMezrTL%2F%2FZjpNpptoEAxtpzDiuf3idj5%2F%2B%2F7B7OD49ejq4WPePiiysVWzmCblgMaZd9vGwN7x58HxyH8QRH9w134ZmLrWqy5%2FpShDSU%2B9DrK5tj9wcEwyvJkzmdolsDMWrpeGrIEQtKsCmiFR0Ixfz5%2B3k1fjxXvqDF%2BvJ78%2FtfExhOw60%2BkCrpRrsXlmItGAyRNQA0mGy95V3%2FbtLr550AR4VxQRY23wxHdBAuM733td2wlw3W4CfU0lTV6dJ3kvn%2BfTq8fWWHqXXk9%2Bap1L2XtMyFsPcCUP3KWU5gYSAkgO55PmthX7mg7n58FpVPkJnlePtEU0DTEPF1PIONrWsBhIKq1OtoJTSuxWtkJupGxJKDTDQ7YK1Gz8LYirrESAa5rEfFFWkAPfSAhrJETWzV1z%2FUfJFwJGwAhpKVyTgHOrazm1iPwUJA2KK14MWyyhKb4XWL9JLt8stDYe3b6ePl89yw9Gq2UIhzcvwt7Plshm0cM9ICSUUlSE0csnxVIj8OURTchFb0Qvx0J6m19OXC%2F43H%2B%2FFU%2F2ZpePzlPz4MiVV1YQjlyVh9CWP5CcMu6bEfPGmKfxGCj%2BLfKVL9yzuncmuE2nCI0uVtb4zgIF2y%2BaSN7JSmU5AKUkIVvPOQz9lcDph%2B5nz%2FPBBMSNCTxaeEspakZu0ghxf%2F3l993Pco%2FHoS%2B1sBGoe7x6gwmLAGSWK4twZ%2BZmZoUs6lk9HJstyxtM9BvCHK1i5uCw1a3lf7MmYg3g13JlDZ76dO3biy0g3YsySChsqjWbQ0rViw%2BeDfXFobY3nvjfLKp68cGTr3CWYA73GhvS7nyZAK4sbLopg1fgGyI5MBaXH8hkisO643%2FTOhlb%2FafzkempxtFFf3IycFpKvOLXx%2FPXEeAV28UrGqKKqpKxSnCKIfAygP8JS2zwEscGfXvqfK5hdtnmBRWSlTBtKoVL6cJlh6SccQuy%2BEF3VsZgA7uzvID6Th8cxhXBCTa3KZsE5bRsCsL9XJOCcp%2BaTeHfPylDv0VkAZNUGCne2HAIUkbkzAt8wCPl%2F4lLyyE2z3IkOlhf0%2FEudg5OH7zr2UXXPx529Pm53y3UD20Dy1E2eQPsEiMQLU60zXTg%2BCGtl9xKuNgaEbcV1n2F88efP4PT%2BeVja%2F%2Fm0N%2B7v9uXfyYudH1cBQNFs9FNnsIar8ta%2Bk7sNB4UNnyZYqLwS70t7a3iokPSnKbpO459UVF4BPivDPcXLs4Cyb69nP9pP92e7e%2F3g%2BnHaqWhV30Zs64l7Mrhz4YMzNBODVnoNaGsnitSWs%2B1gtsKX3dKTvT6%2FanNxBYA1ebNWP2JatUwawDUNW1lDbYJHDa0IIWsASkte90YkDLeWa%2FvaMc3Q1bLqX3ujViv7tnLe72RAKJqNE2ji2T9FtdovCA9P6Qu48yXTyCIXpVqFgl6CpKJG4etqpxiGQi%2FiZ6seNvai6xsp03thWGqqRspBYHDjVtaol2qVELOKE8XRML3sxrsgiSaX1%2BDFczPH65Oz%2B8fDs8O%2F%2Bs9%2Bvfnrw5tAKJMu1mW9QekuqXaeCBq2hDoZdPl0BuZ7NKZQFkCHJBGbEWQFKNh6oxjulTUeZOAItdBYbyPWbqArawnU9TGcBw3gDsbsrirSF%2BbFkba4qCZ2IV9GKS5CisfBh1XYFDusg3qEg7V1REuHXq%2B8%2Bm5gZV83KbAPMmONMz6FWmJ12BwldTGNB9b5WNotLxdzaKmJfdGjJ0ZoIakGdEJSTMaps9AA1ka7ky5ZC0G%2BGhRha4yAcIUKCm0KGgVazRtgDQr%2BYWwlUkU86ZpJ57tGpWvEEbg%2FYWlqWtikZlHCyX2ZtqHDWpW0UYDRdvP08itbQ%2Bux78CyZp3D4%2FuL147inADzUOk4n9xyGYpZK494%2B7VPR4%2F2O%2Ba5J%2F%2FEgbusLdCMSvqZpFbfKmVRZNUpKETwwbXoDBlW%2Bs6hV%2B44JA0o74WHnxquptZtdPn25F%2F5g2O97ov7oN1NJyfz%2FsfUP4ZrPds2jbn6rOBgrpF9Rm9kc4uUR0UJmC3hwU6zEefa7%2FZMzmXW2eT7u%2F%2Bu9O90PeO3fFYBtbnH2%2B2%2B%2BNf8NNyiquY1kCpCJShAjWeUDcRGn5aZ77%2Fx%2F2lHN8Pbx67J85cOn26guTAt7vfcsBYDrBW5FXLAe5i%2FRhanW85YCwHaKttqGyVqxzgu4Y%2Fnr3BtxywlQNs4F7VYoBveP0YWd%2FLAmMxUNDG%2B1WvCnjU96M7tL%2FFgK0YYLN6OYrB46U4GvmK%2Bjwbd%2B%2BeL4%2BOLuXDjOZEBHT3L%2B9kICB4GM9ORyCDcO8t1emIAaea0e8IYxTHlhMgo3D36pdDo1kL3wkIHBsTgVTEl6VIspbNVbLmIHyRNOkv2%2FNm4UpyuDo%2BtvyBExFT3lgbGiL9HLsWgXzDcb%2FLBbsO3uxR03SAIy2tq8lg9Hb60b23Bz%2BvzobTk%2Ft3YE1uDC3RaYE87QlIS3z5vAzvXHMq4k3JOA6m6fUfT8bm2enTzPsjvD9e%2FpQ%2BREAk70KHu%2B50RDVb5egjgGTEpXFH0kbRctIJ%2FxhEfwDL3fKM8ANXJyXHes5bgUMdn3BS2%2FP80KG0IldFeFr7MPK9U5f9Jl9W7CgiSclS7nrBYmVfxm%2BSUEK0KEiSgdg1sWj3axGtL6cmS7i%2F2fY%2BHTf8cL8WDcNFucqO4XBrbIBkIcEaOivKQGYYaDxnGYH0xUXy1oZnRVUhj2grJp3n7DKQXozahGyYxIqXHy%2BOLA2uRiJ%2Bfi%2F65XnraRYkwWHf5gtpCKiX7vKDGjfsTvTyLECKAY09tsqzyM1yRWBcOP2GJOX1zaIAn7rABHIKVSZ6bplJ8U4AOxvmu5cqgyuq5lWWwaFDKnUpauZXTtEN0dzVvmazC2Lqzopu7ooq9i7lujjU%2BdTTdXG55ys63To6UAbwNPFmFNKQlL9hJsvE6bz1VJJt2oxQHy5JqXsxSDyjKldlK5bjfa5Tu0NZ7vfGME2iXXl7QzmdZTmB40pGqwUOsA%2B8Poo4B%2Bo85BVwDihNcyQhGfnFrVqtdA%2BoNPvR9T6%2FUyhYJ9ahuBLHHArixLVmbf1iWzUc9xjAWouKJmGXnZycZ0YL2UOQEEA4tV0j1W1hExVtmsoO7CARZE2%2FDiOFcEb%2F5MQixUi7N1rVilvxWOo0olKgmWFl8zrbZ1cHe%2B3WvfN6ddD9fTPz3cFn7UrR0Lx1rFEZY2XHkc1oMd0LZhaF5IdEg3NVvQ6BDDo3XOeYTAGyBo82%2F1XWYJkFHNNEQdbgTZHCr2316rETLKI1EEV7GNDYeYM9CqHaNas%2BETlJmnK700hMlqRN8XFRRHpkKDkAOdrEGzl%2Fa4AcFjkALgi17Rsu4FyPybMACxYE4y%2Fzl8vbmaRbd67za9I2NNtxEPZRt%2FeB2GaVoq25Kkd8gN5S%2F6pDiTOHYxY6HG8KGHMak4aOU7Pq0Alog39sA4OC8cTDZS1LTL36ZSGullO0ExWPLEQiULK%2BKRq6KQvZldyuY51bXcvBI6OE9Ev3K1UylOJBFURGs80qD6CkAhOWE4KOHPdlh5QcVbd5AoVbwFUK1KmIjdPR1m2Fe0Yh4ZCOWkHGiJ%2BEgxd1nGmUDrREUJiIulLfdCJ4Pw7YdnkPF6CFId2LDOm%2F6KhhyF%2FVTrSM4wrL3TEr2R4rVxj0y45MtBeeIkQ3ESx%2FbBUuD8Iu7trTaSQ4%2B7LveKVv0%2FXGizirkroiGn4p2u8c8ktXaCn1OqKb1snY6j%2Bdj0xPNY4u%2BpOTATRM5Mif1aNkQ5KM9AiL1YxNHn4PSC28ZGNvoRc1JBbX%2BhaYWDi12p679MRNvGFFE4qusDZ%2Fkswx3oGpjMc7%2BJrc4IEYRNFa98bBSePxDZnnyKAhGqZVGwwWRu6kCbvC%2Bo%2BWvjE97xymNB7pNWPgF1FZ6uuLw4%2BNh0gnVicrAWoVeEeUQrGMKoymgeaU6FUvTSoe3OBGs847wlQ2ZWDSCLhpJQolt%2B1f2qYt%2BaZZ5RMEFatxjmG6RoOC9ppiOuHQAFweViEvzDc85A0pNJ05jXQpwxUfgdB5FvLDBMaDwkYTGPHNNCgy4kvgAuXFnAd2Zvn9vBIEiIJY1VqEeeeSgDZyLd1CAM1C0lFpY%2BzYq00t2SVqVMMcexV37EsYgjIbZ%2FQ7EZTjb1HpYWpmpJqZGdFUtPSSZShlzQy6%2BEnInRibGQ13sptsZsxGmhmtSLjLvtUQDw3l5AeIgplevctOYMPuZKKzn1grKB5Nbaegub2ENtzX3UhBE0lvmoLiEVcVCsqs9G07755Tf7BotUwrtayWVGrsThpyJ9ZKTXuufbVKXftJ9fBjg93MmwqjiFpWZWhlMIpGA0ahMSg8HyQpgL%2Bwi280oM6i2vjGENPxjSGXjW%2BMZCs4kcqCEy%2F5bTNo2UALo2aNTG1xM4EWrUDC8iYOFhMMFm%2FFurZBqG9fM0rXglTZ41E0ZdRVKxl%2FGVmFN7S7OApIVzKDbtEpzLbs1Oo6zdeOSl4PHD80J8s3kgtaI9h3IWp4fQ3Tfv9ScvyRNLKNt5Px68Xz6csr0D2FR1Ojsk1jy2wQFbI6IG0AoyNcnAWSfXs5%2F9N%2Buj3b3%2B8H049VQSZ7twXZs1HRmgt6YR2JIFkJC5f2wOs6VtciDUnaMmGhGePB0Akq0PABVjkLIOdEHAaPJu1tz6fsQsp1TgkAp1ZX1otVPPtZgawCajWbHLajGctgXjirsB0mcIGMZUZh%2B2bVgtyidqIc1idq1%2FN6gxWP2tHeVgW7jDGJ2mHqA3nPjYjaiSrXMOcYqEFssClWkVY0Jk8AFaavVJklTgcRNAZhMDTFiRzWxxQbyKpuoLvGxRNEhJw7UQJARAPJczXTCEj%2BBYZAFzKBWY3vxNZx5wxp8iUXXwoSnW%2FYUqDgAdS1by9HJXpHjkujEr1IzAtFUvWMeVfFxlUFUgqjpIZNKxOLz1DaYMwJjtXTXV5AdJ1TdpOMhoxiyTwIUZdTN1ILpkFsuragvVASzyrrudDzkzp8pisLUA7djExIonI3bBkBCv9uZpYbMC7zaugKwnFg8tw7d69bHx9z6fzlWNL8hwuwOQWVBWTTassyU7BKbPYWWkBuR%2F6ZNzje6764D9bRcH4%2B738k60Lu%2BsEpkU5GQgqtbGsqtDRuVThMf78FlD%2FAYgv12z7F5YakTPU12KBo4%2FZ63wqs0TC7dyJY9l51Cz8JMa0G4JwzK4En2Yz1vlHumzd6a%2BY0bLTNswZNG2eFrYH0xfdqMcLWoiUiJdys6LpEUnLmCd55JZdF1yV0gWNYswHSC9%2BhrGNPlnTHRAmUJJLqNGylwnc1m2xQ0TZEBtR7jatBLZDBSTdfsyzexNCgAtOiqjSomJCgyZOFe9CiewOo28PYoAJ5krU3qLAkkVSnYQYVyJlqskVF62cMntu%2FMIELlAWz8lGlzSAYCtu%2FNAGXRDTrYohFAbHEqlkSsjeRubCqygay15HPSfoUZJZUyirp%2FK0he5h7Ep91YUsAqPS6kBgA%2FgtDhhinWNxCJM%2Fr96c2k%2BUfGOGMcbdEdVDJHEXapjGjrKhUdRBMPsAtrbI6yNTEXaSBioI20C4MQQuiid5MYpf2D9OX084h5zIeoio2zVetEO7bsDKwbq5UzWJaw1Bw41E2%2F0GM7rXWuzm9wGlbZz3DH6vpSMdOM8e3MojnM%2FKtOIGYVH0r6evIfnzG4nHiY%2FeLCr2WtoG5aybWCYzua3RoLmI6r0GjOfhG5zjg%2BcNxvyfGAjpOdex6xnRgHgNjQTkAJjFiIsClV3luVTHH%2FJpC%2Fkb77Opgr926d16vDrq%2Fb2a%2BO%2FiEioornRwh68KuIMmSqhqibKqynpI%2BqWA7AmqrMo6Es65TpaCzoqykPRgZ2K1ilblGkp7UEMq36AtGCeui36z5kyKaECzxHEAJ0hcH5goXhtV8oqooIqlCXEcMgcQugI5tOuyTRtHY9on%2FhVYRkvzVZhWRsPlD5q65%2FqOnb1k4gpVRacy5Mc%2FCXZDi2Tmb9a7bJWlefaND8KlpYGH1MBCUcjngrjVA%2B9Nq29vocnrUWNqn0kpD6LqRthk5963chNBGpio1IbUHmMCn%2FrvwJVFHQQWePh1sVCjYaC7pybxsNEkMa2Si0Q5koTtmlDTLhkwyy2qVjVRBIuMxXx2T9HBhI%2Blffc0y%2BNQFIkG6VqP43KoNQUcoKYKdryeZNTMkpqTvquvKn3bJFHFXkLBtS8oWRkPRN0rbn9jIG33DRiPIBVvvf4Kcph2n8qotJNmFhlkzRpOzOWx%2F4NZrcWS5d2MUNVW%2Fnj9vJ6%2FGi%2FfUGb5eT35%2FauNjCNn66X9KN73AUzvBg3wwtQZDw11tAbOHtpBMUaN0NTF6p6IGiJbKZ7eUq1MaV0GVr31HOfCp8e2trVS%2BTGcAdolbdKxC4WaUnnH36h6PH%2Bx3TfLPfwkDd9hLCMzcKqhmOl%2BjdAP4MOxOuyWsOsCLKhK7aTlpWaK47QVqTlI99t1Vyln1sI%2BLJzQ02A6ajbSDRUp%2FWGe8b2%2FPSifNFzKEhSt%2FqjSEaCfd0iWYooh4Rwq7LHdYJAF8p7lmobrSmu3sAo7wtD23N%2FvEGNAI3F1D5wAk2lId7o7H%2FQeWW%2FsEK1NEUsSB4lVWCVZEoGyNjvH4i2VP0MVvOTvNqpZdgrAO69DcCmaJVjCd8YjpMrw1S3mt6aAKAVkfZSBDnKsKQC4bjzxgONkifwZi4bFE1MfPfrYuP4%2F%2FfGg%2Fb5TpuXjeMtp7CgR0VdqcCEGtjYIBLbXdNXzlP3yPlvSFJd1zQ8t6bLlA37WNNT9xtXIVPycNgo%2Fao%2Bgjx%2FE0MJ%2BMv0zrC2kwTAqgvxiIaVNX4e04iLuAqTFeF850muW%2B1FjZ0pPBttc8dNiaybEbLcw3wOWk4go1yiBibOHYZh5mC56ud2BPu%2FHClRkI%2FGNcqnzZwuOIayv6%2Fs4ku5VrnbEFFHgDQzWu0EIyRuDbM2glvnP%2BLnatPIPksTM9AwtQltKGLG%2BUZx3sGDq9UK7aCQBGZt17gTU6HQ2tKRveCE3hTdWeADC7acmbwHan7aEFZI%2F%2FWwzi6ASQIJcs85bV2b00k2of42DoAkcVIlXHp7aFtdGivcTEclNs0V5nXvRGx%2FN7tt9KNsj2wpPEyXv4uxceCT2L1YnhX4Po%2FymeY2XRy08LH375gctLtheJmPX1HLyClq%2BvGoxVJQZQZiR9MTh1p0vOSxG6eG51LYYCwMwmUBAAGR2HyzNa0%2Fznm%2B7vh6erR%2F%2Fm5L%2FxifcwAKqD2rNp0LxdSmC7lxUdnddfx5odTF%2BmJ6dnw8%2BDvbP3J4COrDfPmJCRozk6PHucju5ebg9%2F3Xp2Tz4RjpwJQMaoKcmp64ydQQORHYwVAMMyuYMmMSsA7sCVObhTxwR%2ByxqtxmpF34pJ%2BGYxR4sOcgkIjUIVurb9qedaA3uMMegv7CpWpIMYJI00BAKdPaMAQAaY2cFMIvBdqG%2BJ4CkRCpqbVrSpUgmJCF%2F6XuR9r947Dr%2FI8MLrRUlQh%2F8P%3C%2Fdiagram%3E%3C%2Fmxfile%3E" width="100%" height="500" frameborder="0"></iframe>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>


Nesse diagrama, é possível perceber que todos os tipos de personagens podem ou não ter um inventário de itens. Porém, esse inventário é útil apenas para o Jogador, os Inimigos (que funcionaria como os itens de queda) e os Vendedores (que funcionaria como o estoque). Os demais personagens não possuem um inventário de itens.

---

A **Figura 3** apresenta o diagrama Entidade-Relacionamento com foco na estrutura do mapa e na organização espacial do cenário do jogo. Nela é possível perceber que as entidades *CampoBatalha*, *Vila* e *Porto* são generalizações do tipo total e exclusiva de *Sala* e também que *CorredorMarítimo é uma região do mapa que liga duas ilhas e é onde o barco poderá navegar.

<details open>
  <summary>Figura 3 – Diagrama Entidade-Relacionamento do Mapa
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 3 – Diagrama Entidade-Relacionamento do Mapa</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/diagrama-entidade-relacionamento-mapa-v1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a>.</p>
  </div>
</details>

---

A **Figura 4** apresenta o diagrama Entidade-Relacionamento com foco nas missões e elementos do cenário interativo. O jogador é a entidade central, sendo capaz de realizar diversas missões, as quais estão disponíveis em diferentes mapas. Durante o jogo, o jogador obtém itens por meio do relacionamento "Dropa", que associa os itens adquiridos a ele.

<details open>
  <summary>Figura 4 – Diagrama Entidade-Relacionamento de missões
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 4 – Diagrama Entidade-Relacionamento de missões</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/diagrama_missoesv1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p>
  </div>
</details>

---

A **Figura 5** apresenta a junção de todas as tabelas dos diagramas anteriores, consolidando o modelo de dados do sistema de inventário, personagens, mapas, e missões de uma maneira integrada. Nesse diagrama, observa-se como as entidades interagem entre si, formando um conjunto coeso de tabelas e relacionamentos que representam o funcionamento do jogo como um todo.

<details open>
  <summary>Figura 5 – Diagrama Entidade-Relacionamento final - Clique na imagem para melhor visualização
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 5 – Diagrama Entidade-Relacionamento final</strong></p>
    <a href="assets/diagrama-entidade-relacionamento-completo-v7.2.png" target="_blank">
      <img src="assets/diagrama-entidade-relacionamento-completo-v7.2.png" alt="Diagrama Relacional">
    </a>
  </div>
</details>

---



## 📚 Bibliografia

> SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. Fundamentos de bases de datos. 5. ed. Madrid: McGraw-Hill España, 2006.



## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 17/04/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 17/04/2025 |
| `1.1` | Atualização do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 24/04/2025 | - | - |
| `2.0` | Adição do diagrama de personagens | [Israel Thalles](https://github.com/IsraelThalles) | 23/04/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 23/04/2025 |
| `2.1` | Adição da versão 2.0 do diagrama de personagens | [Israel Thalles](https://github.com/IsraelThalles) | 26/04/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 26/04/2025 |
| `3.0` | Refatoração do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 26/04/2025 | [Pablo Serra](https://github.com/Pabloserrapxx) | 30/04/2025  |
| `3.1` | Correção dos atributos do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 30/04/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 30/04/2025 |
| `3.2` | Adicionado Diagrama Entidade-Relacionamento de Missões | [Diassis](https://github.com/Diaxiz) | 30/04/2025 | [Pablo Serra](https://github.com/IsraelThalles), [Israel Thalles](https://github.com/IsraelThalles) | 01/05/2025 |
| `4.0` | Adição do diagrama do mapa | [Israel Thalles](https://github.com/IsraelThalles) | 01/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 01/05/2025 |
| `4.1` | Adição do diagrama Entidade-Relacionamento final | [Pablo Serra](https://github.com/Pabloserrapxx) | 02/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 23/05/2025 |
| `4.2` | Atualização do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 23/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |
| `4.3` | Normalização do diagrama dos Personagens | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |  |  |