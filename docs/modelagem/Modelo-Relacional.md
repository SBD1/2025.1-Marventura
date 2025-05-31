# Modelo Relacional

## Introdução

Dando continuidade ao processo de modelagem de dados iniciado com o Modelo Entidade-Relacionamento (MER) — conforme apresentado anteriormente, baseado nos conceitos de *Silberschatz (2006)* — avançamos agora para a construção do Modelo Relacional, que é uma representação mais detalhada e formal, adequada para implementação em sistemas de gerenciamento de banco de dados relacionais.

  De acordo com *C. J. Date (2004, p. 47)*, o Modelo Relacional é fundamentado na teoria dos conjuntos e na lógica de predicados, e organiza os dados em estruturas chamadas relações (ou tabelas). Cada relação contém um conjunto de tuplas (linhas) e atributos (colunas), onde:

 *   Cada atributo representa uma propriedade da entidade ou do relacionamento;
 *   Cada tupla representa uma instância individual dessa entidade;
 *   As chaves primárias garantem a unicidade dos registros;
 *   As chaves estrangeiras asseguram a integridade referencial entre tabelas.

O Modelo Relacional é amplamente utilizado por sua simplicidade, clareza e robustez, permitindo uma representação lógica do banco de dados que é independente da implementação física.

## Metodologia

Partindo do Modelo Entidade-Relacionamento (MER) previamente desenvolvido para o projeto Marventura — o qual foi elaborado com base em uma divisão temática e estruturada das entidades e relacionamentos mais relevantes do sistema — foi possível avançar para a construção do Modelo Relacional, mantendo a coerência estrutural e lógica da modelagem de dados.

Para realizar essa transição, foi adotada a abordagem teórica proposta por C. J. Date, que orienta a conversão sistemática de entidades e relacionamentos do MER em tabelas relacionais. Essa conversão seguiu os seguintes passos:

1.  Transformação de entidades em tabelas com seus respectivos atributos e definição da chave primária;
2.  Conversão de relacionamentos em chaves estrangeiras ou tabelas associativas, de acordo com a cardinalidade;
3.  Aplicação dos conceitos de normalização, a fim de evitar redundâncias e assegurar a integridade dos dados;

## Diagrama Modelo Relacional

A **Figura 1** abaixo apresenta o Diagrama relacional construído para representar a organização dos dados de um sistema de jogo, tendo a entidade missão como elemento central de conexão entre os demais componentes. Cada missão está associada a um Item, que pode ser necessário para completá-la, e a um Mapa, que define o local onde a missão ocorre. Além disso, a missão está diretamente ligada ao jogador, indicando quem a executa, e também ao `controller_missão`, responsável por agrupar ou organizar missões em conjuntos coerentes.

<details>
  <summary>Figura 1 – Diagrama Relacional das Missões
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 1 – Diagrama Relacional das Missões</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/modelo-relacional-missão-v1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/Pabloserrapxx">Pablo Serra</a>.</p>
  </div>
</details>

---

<details>
  <summary>Figura 2 – Diagrama Relacional do Mapa
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 2 – Diagrama Relacional do Mapa</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/modelo-relacional-mapa-v1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a>.</p>
  </div>
</details>

---

A **Figura 3** abaixo apresenta o Diagrama Relacional com foco nos itens do inventário. Nela é possível observar que somente as entidades específicas apareceram, pois no *Diagrama Entidade-Relacionamento dos Itens do Inventário* a especialização para essas entidades é total e exclusiva. Note que os relacionamentos também foram modelados para as tabelas auxiliares `IngredienteConsumível`, `IngredienteNãoConsumível`, `EfeitoAcessório` e `EfeitoConsumível`.

<details>
  <summary>Figura 3 – Diagrama Relacional dos Itens do Inventário
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 3 – Diagrama Relacional dos Itens do Inventário</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/modelo-relacional-item-v1.1.png?raw=true">
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

A **Figura 4** abaixo apresenta o Diagrama Relacional, com destaque para os personagens. Nela é possível observar que as entidades principais `Jogador`, `Aliado`, `Lacaio`, `Chefe` e `Habitante` são especializações distintas de `Personagen` no mapa, cada uma com atributos próprios como vida, nível, experiência e coordenadas. A entidade `Habitante` representa uma especialização parcial e exclusiva entre os papéis de `Vendedor`, `Recrutador` e `Cozinheiro`, mas optou-se por mapear todos os papéis em uma única tabela, utilizando o atributo `Tipo` para diferenciar as especializações.

Vale destacar que alguns dos relacionamentos também foram modelados para tabelas auxiliares como `HabilidadeAliado`, `ReceitasConhecidas` e `ItemInventário`, permitindo a associação de habilidades específicas por aliado, o conhecimento de receitas pelo jogador e o armazenamento de itens no inventário, respectivamente.

Além disso, o diagrama contempla os processos de negociação de itens, através da entidade `Negociação`, e a modelagem de batalhas, por meio da tabela `Batalha`, que integra chefes, aliados, instâncias de lacaios e jogadores em uma única estrutura de combate.

<details open>
  <summary>Figura 4 – Diagrama Relacional dos Personagens
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 4 – Diagrama Relacional dos Personagens</strong></p>
    <iframe src="https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&nav=1&title=Diagrama%20de%20personagem.drawio&dark=0#R%3Cmxfile%20pages%3D%222%22%3E%3Cdiagram%20id%3D%22hC8xNT2k-P87X9VGEyLD%22%20name%3D%22MR%22%3E7Z1rd6I6F8c%2FTdd6zgtnKd5fqr1O1bH3y5uuVKhSERxEa%2BfTP6Bg1WwCCAZMMuusM5UCE7P%2FyS%2BXvXdOiq3x4sJEk2HHkBXtRMrLi5Pi6YkkFSpS3v7LufK9ulKqllcXBqYquzf9XLhT%2FynuRfe5wUyVlenWjZZhaJY62b7YN3Rd6Vtb15BpGl%2Fbt30Y2va%2FOkEDBbtw10cafvVJla3h6mpNqv5cv1TUwdD7lwuV%2Buo3Y%2BTd7H6T6RDJxtfGpeLZSbFlGoa1%2Bmm8aCmaU3levayeO%2Ff57bpgpqJbYR7oLMbXvbczufl7VskVL24fRvpZzn3LHGkz9wtfondVk5GsNDTVLrBbduvbqxD7a0ycHy307lxqTi1kWq7dinn7gm0JC6m6YtoXCsvPmoYmU3V5%2B%2BrK0P4X2ujbmFnei7xPzQ91oci3K7M599oWbNsvcz46L%2F%2BwX37nFsb5NdLUgW7%2F3LcrwfkXm6YytcvSRlPLvWNojTX3R7zGvK%2BvmJay2Ljk1uCFYowVy%2Fy2b3F%2FW6y61nTlXKm5n79%2BxFHwrg03hFF3ryFXj4P1q39MZv%2FgWi2CBcuYBckmu3U02BwapvrPMZTmVuymGZefv9SxhnRb3EjeudQ0lo15aQ5V01qGZji21g1dwczt3CSbxuQemQPFci9MDFW3lvVQbtr%2F2TXTyv8qn5Ttsrbsz4Wfz%2FZ%2Fzu2m1TL0qWXasnLeodjW%2FVIcCzctY%2BK%2BVFM%2BvPebbrU7P78blmWM3Q%2B4AIiNIlgVrgqKIUVQPJQIKpgIetdOZUr582tfOdj1YKlIu7W7TaQPtJXxlr0o%2BjEeYGGwzrfqedMAiqx673PaoGHX6oe27AeHqiwrduNtfg1VS7mboL5z05fNke1mu93mw5mwHNqEGzYr13%2FVN%2F5Uq9Es6L77pz7jvhxpdp%2BmI8tucTNdnmIqWX%2BL%2FYVTxYSjygEdPx3ZeB376t7m1FaHqg%2Faqycr8YVUTlxIC6KdN7sGKf8rv%2FFHKiaps33eTkFoNYGp1DFVSRtTdYEpuFUITAVMU%2FIAp5YzFdWZqghWRVSTYJWrtvFC0Qz5Zjxpt58fOn%2BU8bj%2BkqvhajuRKpprW31LapW%2FM2PZwysLK%2BeYMTc2bEEWG%2FZduuHa9ec2%2B6eB8%2FeVzYmTVvGkIel9FbVRH6mG92%2FYZV79M6tbyZw8rhk4JHpc3JFn5blSYXtaXg6LuoKUAOtgEeFLK2LE4zfiIS7SkNtoJifpcJElcPiTKrp2WzNEqsjtl9weIo11KhENROZNmLfR4EsRGM3ARDi%2BcU2AWgLGNXGls9g29PZYI%2BGhSza0VBKYCYWZwL2AhDBDc5INFxnfEcjMLJsibkqhDcc8bvDdgXDTGVnpGyayVEPPaaruTmrsUirm6iMwr1Hl%2FeYyGQFaJvXJH9PwXQnBtDSnTvXUmRZh%2ByAz68UJdRTV0NZiHmT4%2FsGjKqOGNbObfMbJkgmBsEySi9Fsqv%2B9Vo2XizflvXTRLC56gHtTE9l8GKJIs%2B0jXGjFtRN%2FUbWap%2BjrBJpT%2BDrF2UQmtpBMLqOCJebZ14nYKrgaIIA1AXkzuR3%2BMY4P4m0Rx9QKd2MF4aGUPlxoLp6CJebZQ4nYKgRcQB%2BkcAupbu%2FvLJ%2BuR%2B%2F2zyn4jPBFu8gOUUzSrjgpj4qzf%2B%2Fqufr89Dm6%2Bj1X1VwB3ze8spTxlT53qtRRWcEUU%2BIdedTq2zPiAsUJMWxFMWiJM2ght4xMTonhIvM8bCE3DK7GLWBVSNC4JWw%2Fz%2Bx4Ia5quBswSPhaukANddTQnCDDMpAEanwahkCNBDq22tMKwZeoUmGZL1qnq87aPan7NPuaNF%2FR7Xzw5JeJghzfxec0dDcJRTWsf06hnAAWQOvhVBCDAz8vZFwBxAaRyWkoWGK89z%2BK%2BJaAjj6kuaTQ5uImlBesJ3zd8Zgiebepnw09iWBekt6Ez1CcaWsyZKI5awVLDEVAHPlUNaStRCKkcArBXYdOkc7iumjiuhH4cXVV%2FVAq5cbj473%2B8Pxy3dMvn4aVnJcoUuCGHm5ohqvARq8xiBeivAVfgiSBb9G2ZlOLD8LElY5AjCut3L3c%2Fnv1Jy%2FlbmvKXVvt1%2BSZ1z8KwtAjzHrRnAZiQKOzOIEhqVsAJkAQ%2BOJr134nF3iJqRtBF1LqRcB96F6dGD3FnBo6GhD2dvncnCt4NvIOPKDoIwobUDjuxNmbIzeKTG7OwUWWMBmwuTtHbgRcOenAVQE56YTozjMyYjjIDlxczbDsrQPXjUg7F2cWmhBUUk%2FoLkXYXT3eeSm5BQiiSPj2asgpQkaYkgmVsMyQxb%2BbzvztRX%2B9%2BH6o5Lsvs%2FyXmSvgI9Kk06z%2FNgZItoUjMqtvSC9SEqC1WFzkSKFXPpOY0MK6wQewYuyxV3pAcrPM5NwWLjI%2BGs1MUMpBUoqS2wVXIxK4KqBxKb1MDaq8J3gyMh4KM8emrln%2BxkcRvBa55lzgIn5CnKM53YaLjHsp8sS3SmiDMc83PO%2BHKnfQ5CjT3EU4MQSIyY0rFZaxYjWmlw%2BtkXFdQYWLy79G%2F%2FOpskauoIjfSi2mmtA0yYRLKmz1UspdQ1ILswHGIUieaUzA3xufBjHtFJSkNvjjQkVwgToXqDqSwmb3D1DhAAwVTsGAzx9OlWnfVJcZwarL%2FxfZjU1IUir8caIuOEGfE%2BW0OeGpj09O1PnkBOA73DIM065tRUbPgg8hJMIdH8QuRRp8qKXOB%2F9lRfb5IPlYh3k%2B4I4XLh%2BQjF4EH0JIhGU%2BfPTU7st4Wv6oVB8eB72b6vNZUyRkisyLA2xlhz66IAlegDLgIiUTsQFwtY0N1gTuznCmK%2BZAPcptbNri4A4c4qyTLIAjbDzzwcCBJ9LhBRxcnmkC1gRwFptzEji%2F2BAHl%2FhrReQ%2FyAI3qmlzAww34wMc6yYgyAEEj3WX292nc0Xjlx8RFMIyQMaTyufw%2FL43bpbvnrrF88%2F77pPIr5cCLop5irgArc4iHEjy5osNYE3gaLizWwq77rIJSoNlKPQKj%2FedfPP3m5ybL2oXT42z%2B6GAQhpQoBloDlqdRSiQ5M0XFMCagJJNrIK6ZXW%2BpYUQgeS7geKBQenvqD8amM6Xy%2FVXwnHeaLdRferZ0IlP3%2Fid5tRWTkbm6H%2Fm4P1%2F%2BVUaBO%2Bv%2F1Z%2FO7%2BRyuXVh80f%2FvvvZJ%2BA9%2B3vsbrmLMg1rJnd9%2FkFwQddXlbwcUTMxzxAMp94s2QZyNpInj1OR%2BfF85tXsz6vz5TFR84%2Fvk0A%2BWBApnqwE2T1MoNAJsmbLyCDNYE7jpwtJoobutLQ%2B6pHHeaIkbhUWIYE2MUB%2BSobmopk%2F1AnkQpufeqwJ5PImeAOlg8FSDwpRgHJZYKTwjsjZSUTnIS7lHGYCU4SmXLWVQFlygno8zMyQqCXhS2CXvgbMkTwN%2BOaMftlYYvOmNSzsHkv5jML27o9CLYUcc%2By48jClkm1sEyWP%2F8%2BBt3FrHbZaEwXA%2Fm7O3i7FluIh4iTXfHEFx4087CBRmdlBzHANv6CZxoT4Nfm7GTGBJXBHRLEJhZ9JFBNwQZanZVNrH1afolPJuAL1yL%2F2l5C4Q4R%2FukaBSIOhgia2ddAq9c4RkSVT0Tg684i9VokgXCHBi8qWrCBJhtoZl6Dze6%2FkMg%2BHFaa548OQDSzyLwWTSIs8wEO5xKZEKIC4wD711RTr8E6wPsORggSHNHIZWATXBX4vgQ3OXTiaoM%2FdOCJXgU66KODZvI1WAcRsreyhg4uQ3DgqsC3LzhLohNXISwDZK715Tvl5gw9XD7mRui%2BW33rip3tNHBBM%2BcaaHVWdrY3jUOSN19sAGsCR8NGIgAOyBBTHtyBQXjB0gcD1exqoNVZnDWQ5C3AALjBniLdaKIpu66wCaqDZS60nqu9v1WtpEgP%2F0b1m7vTiWICXFDkgeJFrdh97NAYGDrSzn6uNpeJkhQPAD%2F3tI2lIBzDfCqW9e2CA80sY9tstrXM7%2BfNDy%2FOy36VvY%2BnC68DWX7ywKIsVOt54%2BeNp%2BxPPw85H7xncIl4X9mYmX2F1OG7YyzLo5T9sbMYX%2FfezuTm71klV7y4fRjpZ%2Bvj%2B5yaI6rLVDRkqXNlqxwE7fQcJP6osuiFVexOPLxXrL6S%2B1TyWsFpQkMrrs0LEWy%2B1lc%2Bmr7214q3yp%2BCVsIOEECT4qfJZd2kEbuMUCYFLVXGLUrsJjJiUXwFiKJFo3TMB22koEVruEW1TledtXtS92n2NWm%2Botv5YJ2TOCMGxbcCrvS5892dleCCqYqkOiHGc6Vtcob1DViP0hK3qkipE36CThzwE9tMJjPqgCWGE%2BqkOmE7SPg6sTFwNXsHawJKoxO2u8%2FINP4g%2BXRiyoa7ab3IphMOL4HZdJLBC81kOvAyTx4TBJvJdIitQfAF8E1W5Z5iTu3p3kAZHxNbsiIZ7tgSxa%2BZa7hQmrvQTLYDCwI6vCHr%2B47JdBMRkrkzjxbcd%2FlenWR%2BupIJbbDMkOa9dK%2F0a0%2FSdDR6kRs31%2FnWzXFtO%2BL2BlacSaOIDO8KgdZJdaNvrz2EQ1i0OCmPirN%2F7%2Bq5%2Bvz0Obr6PVfVXAHYRCAtTtC3KHqZ6a1zdHv7NrcevwqdUn70nMOH%2FVcWYbh%2FhDsHviYN3%2F0WCl5PGHFktQ4YSdxuYqgdfh0HVwCxKWRybwAsMT68Poq9gci%2BW8QWwNUAG6wJfHytysRePCMj7DAbArS1wvKAG6yaCAGFXIMEHh0mAxKauwBgiSM4HWRmnSaZniH8ohrrFMEdDQJPR41w0upqxcfnxNFsYyoL4uMOS7i%2Fg8ASbSzR3D8ASxzBWYExLNVC24p1LAEOCklyaXUUgODSnurjjksih1sGwET1yAC4yBHWXxlDE58p3OCqwBdgb2ZIt1QZyXxE1cZVCMv8KN5XjWpxVKo%2BvGr376VXuW1cieMDUqAFzdMDQKOzcnrApm1I6uYLDWBN4FPXW2Tyw4WY6uAOC%2BLogBS4QPPkANjqrJwcENj016s4ggzA1LFnKquDx4yWMZ6YfOSAjqsT%2FhiB5%2BQQjDgwI6geFgBb3T9zK2uMKIa2DvOMwL1yfhjxqOicHBMQVyb8IaKC6YJm%2BET%2BhJKzvXfjprM9yfGPvrN9rdv5N%2F%2BeNm7u2vKrJkulex2lHNwS0ToHy6k3XiiaId%2BMJ%2B3280PnjzIe119ytRJuUbAOi0lb1H10J6VeTvJWDT1n70p5%2Bx2rkmI59Rqmib43bnOHRP7%2FUGknBVGlWN58X%2FADUqW8o8xVGfbtWcBqxyctbdRHIsdUCPzkSoUdg4XevkxiVElqRWIXO26kNrGxZDKSBCwxHkLgRJLY78qzmQ2E2Ci4mn%2BANYFPP1Q5oL%2FPyLzjIEmmYqqF5WmI%2BfZhTV4WnffKoCs%2FDG8NY3ohDptJFSY0o0lA8%2BO9B5sQIWmfL4iANYEHFanyJXpXtaPdBg9QyLbIkpYLyxQBOz6RCTccVgLzHSSDFZrRIGCJ8QA1NrFCbAxcYQWsCSgTbgdNjnJHJB5QYgqFO6CI3LdxNtSToQjV0A14EwYKKEu16zjEDjuxAQiIAGFcq0jA42MIbWmwjI3m9%2BPrx%2FPjovZ2%2Bv71ovca31d%2FxWpWECUw0YQFhz8laIZsgEZn5eTkANv4C55pJoBfG19vOFWmfVNduV0t%2F1%2FM%2FP5HFoTCMiGsxvTyoTUyriuocHH51%2Bh%2FPlVE9EYaiKAZvQFbnZXojQDjECTPNCTg7%2B3NeH8o0TIM065tRUbPvNIhkkS4w4OI%2BaZOB6pxG6DRWYn53qflV%2FlkA76%2B7KIByehFoCFYICyTAV6GxEcTghW0tyTWSfrT25I4xnOSkll35vOcJLgqcCfsR5WTSL%2B42uCPHCJvewbIUU2dHFxkbie3AEGOAu4a113uV5zOFY1jfoj86v51478%2BIXBxIFwU86njos4NHbjMoA7rFHJ4i5hB3bWhz8EeV7o6Vgdcn%2B8RV4QsA%2Bj0Slu8X%2FyeXf95vsh%2FFpr5pz8N4ODJ1lD58PfAE%2FkE1vkEqh5HUsknAFpTrGOGH14Q%2BxFiW8lkPgGwxPDJlOzmEyA2Cq6GIGBNQCdUkrv7jIwNDpJOIKZYWB4qgDGy%2Fn5WgiWHZ0nq6QTwsQWbDCFpny%2BGgDWBDymOKZ1AFhXDMkjAvk%2FsmYUjS2BGgWTIQjOjAFhifPOMTbIQGwNXZAFrAt894zWjQEyhcAcUcUpxnF21ZChCNaMAWGQujikm6l8wBMgqwU1CgZjSYJkaYNisWM%2BKFw%2Fkzw1%2FSKSeUIAVJuwTJ84%2BE8Cvja9YiYQCewmFZUKA8VEi5Qx9QqSeT4CTlDP%2BgmeaEODXxhcgRTKBSALhjgxi7kCdDOnnEuBk7uAveP7IgM8dRC6BSAJhmQxwJ4Z7VAtW0N6MoJpLAC6yFF4Gx0WPYGtx6SwFVwXOD25yCcTVBn%2FkwN2zBTmok4NmLgG4yBHc41gjB5endsFVga9JcZZLIK5C%2BOOHSHBJHRdUcwnARWYlw2WwcaqhrcM8HSBfN5FLgAaAwouQZQDdnU2v2t1WOaeXJ41Su6arfy1gU0SRB4rn52z35UNjYOhIO%2Fu52jSd0igeaH7uaRtLRTiW%2BVQs69sFFJpZxrbdbHOZ389eX%2BR8eHE%2B%2FCp7H08Xm7889QCmLFTr2XuH%2FfPGU%2Fann4ecD94zuEa8r2zMzL77nUmnVFseDO2PncX4uvd2Jjd%2Fzyq54sXtw0g%2Fy3kvdCqOKC5T0ZClzpWtYvhKp2Ga6HvjBpfDP2%2FuORd%2BNJtbb7Z406JKeVMxwQ%2FUyjsKWxUhUb3h86Ij0Fs%2Bab2RwpjT0humj6JU%2BlWo%2FPypbomlvNNXrYrtviL5fgrPvkRTN4WM9FMXo9lU%2F3utGi8Xb8p76aJZXPQ8d%2BFN3YwXimbIN%2BNJu%2F380PmjjMf1l1wtcd2EHQSDFi3hayZNZE9xhv5LrSKRzbrvLmF9d8hJzbrTT96g4tTp8JNb4iiW3F4ymcoGLjIeHthjMkqU3B64mvvCVQGdPB3U22dkXnqQPDZxBcPdPLVaFCxJkyU0U9nAAsB3WtnMOECUv2BJrorPG1T5tzFAsm3II2JJZgTDH0vygiVpsoRm8hpYALi%2FJ08syYc2GPMskQCWNDTVZolAyR564Q4lFeG%2FkSpKqGawgRWAL21wxJIKl%2F4dcFXg%2Fh1HmKk5M3LhDiWlCLmwuGZLYIrNpNhCM%2FENWGavAHyyZd0gBFvK%2BIRVla%2FshrR0L5f0voraqI9UMWvZRz3coaaMT3sFalKdxtDMoANL4hjP0U6mp1i3BsGZMr7JdraYKG7etYbDmQukZ3%2FPPhNi4Q4r1Qqmiww7aeIGBxwuibPYTY9LkkdvRhwuq%2FhaZYbN8zkbT7yiIbN%2FckBvbOL4MQW32uWjkd3%2Fdz1CC%2Fl8gP9%2FqRj3iVrQA1iIQdQHKnkKQQlVPB4vw1EJ%2Fi0jcX9zomvBZstY%2FLvpzN9e9NeL74dKvvsyy3%2BZ60waabeMQmVbU3UpQIS7D%2BxE0hxIhEcV4pC6CPMhRShVMiHCcnVHg2WyBnfvT1qC4PlX6Q4QYneDodREOvhrU0xap6vO2j2p%2BzT7mjRf0e188JT8gG6%2FDq26K456QIe2%2B0Ah7y4u%2BD0h1WI%2BUCtS0OuRY3t%2FvZaOS6%2BFekS97j5ARU1e%2BrfjkNP%2B4gEmNnTEE3b2Wr1XLqX7mnJXmD%2F%2B6RXPL7%2Fnl8Ch97dKX1EtNG0Z%2BlDpqzKaYvYTgYNY4OB6schtWtWwUWL1BJaeQcuKzYiENiOI7SaTUYNgifGdCCdo0H5Xns3Nb2Kj4GpPAqwJfEviKMM9EgsdjCkXlnclwKoRJxcn5FaVDF5oBhKCJcazFHCIFy5PMAZrAjrB2J1ZCLxElwt3eCngB45leNXgYHuopFHJ0W4UVaspbxRVP5RKufH4eK8%2FPL9c9%2FTLp2EFWAm5RO92d6Vb%2FpEGYgFk3TPtbGFLYSOI1udTxBqRQAYVCyBJLYCQmks2F0CgEnO3AEJqFHyNUKGagBZAgnt8pseo8QTD9BgVqhqxBJLUEkgigKG6BAKVGF8C4QgsfC59QDUBLX100OSo1j2yohXumIKnPRBMCX%2BSSTIgoZlICSxxhJD1zASNRT5Tgih%2FQRHPYX%2Fz1Cv7pVmHSBakwTI0ZPP2emT8G7feOjdW5bJwmx%2B0AQdjwYgtRgSc4uyPDV9GUM2QBBqdlcOuAmzjL3immQB%2BbXxccKpM%2B24YcXX5%2F2Lmc1VkQSjcEQLfTRWEODQhaOY5Ao1e5pgQJT4JgS9BtgzDtOtakdGzIEOwQLgjA35SoSDDoclAMy0RaHRW1pP2afjsryeBXxv3fnDJgGT0IsgQLBCWyQB3YrhHnGAF7b2IdeKW1DYjvPhdDncjCuHNxRA%2B4KrA%2BXE2nSh929qqjGSO9yUiiIQ7hEjspa4jOckdy5nm5d3EEQFHmu%2Fen%2FCJ5qWSXLgzfv9p%2FDWLtVatNtQf%2FwDu%2BF1lYNj9TbjFbuGZ7xmvvpP6rRx2RJGIZz5o2wgjCu4HlkQgEVtOJj3zwRLDnvmpDigO4gxHbAxcjTHBmoA88iN1%2BhkZax7EOT%2BmdlgeesK9oHCKSZMpNJ3x4RLzcoAYUf2CKrkCdIDYlaWMjwkjmVELfxwRrjNpcoSmLz5cYjzKjyeOlEIbjHmO4L41R5kxLTOC4Q4lIl44HFoC44WTQQtVF36wyLwEDBNbgyALFDD8qDh7YIIs%2B%2BiFO7CIoOFMzVmoev6DRT7GAOJkegkuA4hh2eIBxDczpFtH665DWyAsY0T%2BffZ3Ub6S7lpK8erzvnZV%2F9JEKEC61KAaFQDZn0VIkITOFyTAmgA8L0xltdlunKu63ch5AEVMkbAMCrhvE5EBmUIH1SABuMgStzMOPoME4KrAcXKvTjLvr5UJbbAMEZCvR5XgH7c3EBpA9K3YjA1ALzO9dY5ub9%2Fm1uNXoVPKj57TOxcQtA6eO%2BLYAzdIi8qbxiEFeGTEOOlG1URsOvucjbHnoa7EHeljOS6jlt%2BO16gUyME52P1u%2Fx76dI3IDyR9HIdRvJN711rlcvH5rsr6VB1YRZ%2FjODRn8TLI6eIIY398hgmA4n1HDtgRpOsjOWgcQQraMMKkgPtpYigF%2BLcU37khzeAesHgZPnYjfiD5dqPf24QSbEKG5ovg1z7iM0hjasXPmWF%2FrbA8fwTrQXjTpQ8XmlE%2BYPEyfOpoZuBS5hMukFfdcgpxtA4QdPjiIxfu%2BFLHJEJjkWWPxZJ4a5o7qx2BayykiV7IJRbaKyr4ikfaB5DCqM2nqbjCcSkOWLjVOl111u5J3afZ16T5im7ngye%2F0XLcdVr7o2kY1qYA7P542DFkxbnj%2Fw%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E" width="100%" height="500" frameborder="0"></iframe>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

A **Figura 5** é uma junção de todos os diagramas relacionais apresentados nas figuras anteriores, integrando as entidades e relacionamentos dos itens do inventário, personagens, missões e mapas em uma única estrutura abrangente. Este diagrama relacional consolidado oferece uma visão completa do sistema de jogo, permitindo entender como todas as partes interagem entre si.
<details>
  <summary>Figura 5 – Diagrama Relacional final - Clique na imagem para melhor visualização
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
      <path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" />
    </svg>
  </summary>
  <div align="center">
    <p><strong>Figura 5 – Diagrama Relacional final</strong></p>
      <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/modelo-relacional-Completo-v1.1.drawio.png?raw=true" alt="Diagrama Relacional">
  </div>
</details>

---

## 📚 Bibliografia

>*   DATE, C. J. **Introdução a Sistemas de Bancos de Dados**. 8. ed. Rio de Janeiro: Campus, 2004.
>*   SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. **Fundamentos de bases de datos**. 5. ed. Madrid: McGraw-Hill España, 2006.


## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 17/04/2025 | [Diassis Bezerra](https://github.com/Diaxiz) | 20/04/2025 |
| `1.1` | Adição do diagrama das Missões | [Pablo Serra](https://github.com/Pabloserrapxx) | 30/04/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 30/04/2025 |
| `2.0` | Adição do diagrama do Mapa | [Israel Thalles](https://github.com/IsraelThalles) | 01/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 01/05/2025 |
| `2.1` | Adição do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 01/05/2025 | [Helder Lourenço](https://github.com/F1reFinger) | 01/05/2025 |
| `2.2` | Adição do diagrama dos Personagens | [Israel Thalles](https://github.com/IsraelThalles) | 02/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 |
| `2.3` | Atualização do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 02/05/2025 |
| `2.4` | Adição do diagrama relacional final | [Pablo Serra](https://github.com/Pabloserrapxx) | 02/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |
| `2.5` | Normalização do diagrama dos Personagens | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |  |  |
