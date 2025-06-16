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
    <img src="https://raw.githubusercontent.com/SBD1/2025.1-Marventura/refs/heads/main/docs/assets/modelo-relacional-miss%C3%A3o-v1.0.png">
    <p>Autor: <a href="https://github.com/Pabloserrapxx">Pablo Serra</a>.</p>
  </div>
</details>

---

A **Figura 2** apresenta o Diagrama Relacional de um sistema de jogo, onde o Mapa é a entidade central, organizando todos os cenários. Ele se conecta ao `Mar` (com `Corredor_maritimos`), `Ilhas` (que contêm `Salas` e `Portos`) e indiretamente a entidades como `NPCs`, `Inimigos` e `Habitantes`, por exemplo, consolidando-se como uma importante estrutura que abrange as localizações e interações do jogo.

<details>
  <summary>Figura 2 – Diagrama Relacional do Mapa
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 2 – Diagrama Relacional do Mapa</strong></p>
    <img src="https://raw.githubusercontent.com/SBD1/2025.1-Marventura/refs/heads/main/docs/assets/modelo-relacional-mapa-v1.0.png">
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a>.</p>
  </div>
</details>

---

A **Figura 3** abaixo apresenta o Diagrama Relacional com foco nos itens do inventário. Nela é possível observar que somente as entidades específicas apareceram, pois no *Diagrama Entidade-Relacionamento dos Itens do Inventário* a especialização para essas entidades é total e exclusiva. Note que os relacionamentos também foram modelados para as tabelas auxiliares `IngredienteConsumível`, `IngredienteNãoConsumível`, `EfeitoAcessório` e `EfeitoConsumível`.

<details open>
  <summary>Figura 3 – Diagrama Relacional dos Itens do Inventário
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 3 – Diagrama Relacional dos Itens do Inventário</strong></p>
    <iframe src="https://viewer.diagrams.net/?lightbox=1&highlight=0000ff&nav=1&title=modelo-relacional-item-v1.1.drawio&dark=0#R%3Cmxfile%3E%3Cdiagram%20name%3D%22P%C3%A1gina-1%22%20id%3D%22z8SUrFOs0pDH7z4ywPko%22%3E7Z1tc5s4EMc%2FTV76JjIGm5dJml57yXXappe7e9UhAcfcYHAxztOnP7ARtpF4kA0SZnemM7UJJo72L%2F12pV3pTLuav%2F4eWovZn4HteGfDc%2Fv1TPtwNhwSgwzj%2F5Irb5sro%2FFkc%2BEpdO30pu2FO%2FfdSS%2Bep1dXru0s926MgsCL3MX%2BxcfA953HaO%2BaFYbBy%2F5t08Db%2F60L68lhLtw9Wh579W%2FXjmabq5PheHv9k%2BM%2BzehvJoa5%2Bcncojenf8lyZtnBy84l7fpMuwqDINq8mr9eOV7SeLRdNp%2F7WPDT7IuFjh%2FV%2BUB0czm3ppM%2FvG%2Fvs5X%2F8%2FPN86%2F7AdFT%2Bzxb3ir9k787j44bWem3jt5oU8R%2FwCJ5GVkPyaXLZWSFUWox7Ty%2BENsgslzfCeMLZP3e86zF0l3fvrkycz371noLVhF9EH13OXVfHfv7xmDJvbHtbuOHJW%2BTh0%2Fjh9%2BlXyb5seW5T378%2BjH%2B85PfeBk6y%2Fi73FrLKL1jFs299OXLzI2cu4X1mHz6JVZqfI1tv7RJn50wcl53LqXt%2BbsTzJ0ofItvoT8l%2BuYjqbgnZmrrl61UhufptdmOTOh9VqrOp%2BzRWwPGL1IbCtlTY%2BxZbsjviSYvZ0Hovifm89Lm3jXu%2Bv2LO%2FcsPxa7ZecuXQbrzr02kut5V4EXJArwA99hRJDcZIfB4ocVPjlRemERuH60bgn9Mv4Xt83V%2BW%2F6mR5%2F16v4Pdm%2Bj%2F8lt4fRVeAvozAWW%2FIMJ7b5i5PY%2FTIKFulDPWdKnx%2BmDZ%2B8fgiiKJinb3YUwqqhor9UiyQVhVZTE1p7mhgxmvh6U6iKuA0i1%2FLiUSCy%2FCdvY8P14GptbcgxNLfp95p71w757hzEDTr11uPjzLVtxz%2BkA1d0iWqT7djIEDRR%2BrBtswk%2FzfLigcy3orhDrXx7ydg9%2B57HSEFnpPA5buzInbqPMZ7CqrFfjjjo2L6593IZ2931n243nzRy6tE7o57XfVvvmJ%2BMGlVTrcc1K6f7j2Rqzu7vtIsLd%2BGvlv6P5%2FGAIFqUooWjtNbQwhUA6zx%2B7CVYytQPCyvclmB9zqQTreZnV9rZxYdnx%2FsaBvbq3bWDUwJLV9TTZ6zwR8IJ66VcT2O%2FpFg%2BGJNSmejUiHTCZVQTEmTYWgBispxAz4HnOeQkUtdzyPrLCQWlJgsNSEFp1iVAeQ8FbcHOT%2BwFpRVjfwddh5ZjUgHxwHMeTNZ5QNg0GKaKw0ZmmFqgCaO%2BJuQMJ47t0ue1TZr69uo%2FacaMDr7ET%2B06Wrqhjj6j5Hr%2BTq6mi58vH%2B6J4bzMbdP9NSCaieRQSo6666lNkIMvASrFXoGiXO2wQFFgdjrvsgXFvZVYEQIpjpYHOFKwAexFOMcMmmqJDEZ01jEd8bkzU4Rj5eG4rTEf48eGvIDSrnLUVCVPEK35AGzsmExUxs867%2BdiZ2mnQN%2BADSH3JitLB%2F6OeAmtTFUeKZsSn0Fv1meo8zgJOpogZppZE2sGM7xJSqmYMRk9AMLLpLa5%2Bo4XqrkivnyyHlzPtS2787OWXVQPOMoQdiIDMaMwmuHNaErFDC3I6vdSWHlfQMoQNvsGzELYsdroM0P4qao6IkMhMrLETBnM4AvA6CEiSqUOCxH8pmAnun64i86n4XVCG31GBHdQGxaPEIgICYjQVYcVdEOEXiGiVOqwEMFvCnYO%2B9vK8qOTmJ7qhELggUJDUKgExUQ5KEZgQAFy3wl%2BU7A5Nd%2BtEDomGtlZoqeYKE67RUy0j4kMCeowUby3SN8wcV7bOr3HBLs29TV01rtIjIOrYL4IO59a1QmdgMMFKZ59QFxIwAVvjwm5q9oTKLjIpuURF4RNmdvi4t7xbcC0EJAJOFoMOamW4Qp3vK0hEqZeR6%2B7ON1evQ5VEKa4teINZL3ldCp2NDbpEWDJjlY%2FYOi7p6CxgeVeUnX58N8RZ0Fe1Y6AcsA5DxpusF6PNofV7YjTRnnhjsZWf0OiDK5yZU1Rsbk6lu4cJR94qBHYtQw0amQFNsqLdzQ2J1fxUCJt3lPDtLusKdi0O9jFOwLa6DNE%2BFnrxSsjyAwJzOhA9U7xLoany4hSrcNiBP9kFnZSHHj1Dm4SUMxP3OdULSOUl%2B%2FA2eYUdzndGp1dJsPyHSGFgCPFCGeg1JJCef3OqLiAq2ekoFpHUgxG7BIX1u8I6AMeJ3DLGKWcUF%2FAM%2BrjnjGlWkdODEbs%2BhQW8BygE3i8wFUKtbxQXsEz6uMqRanWkRcDOvpgBc9RMgGHC52ducydOF%2BOkxw6YNbyZHNJ9KTwuulNLR69g2fv1PMLDkuu1utrpCulPDqevrPbL9Bl0CvO36nLgY74DxKP4sHws7ht8DCeNuNRce4oL%2BrR2RpxxUOJtPhUx%2Fg0O%2FqPjU9hZ1oLaKPPEOGnXBbvbInMkMAMmdU5fAEUL3qeLiJKpQ4LEfymYANU2InWAtroMyL4%2FkTxrpaICAmIkFqMw1cAmDDCqG%2BdHjGC3xTsniGYaC2kEHikwGBCLSmUl%2BQYfYwmSrWOpBgYbDSBidYC%2BoDHCdz5Wi0nlBfkGGC2vjZw6%2BusKcq2voaeaC2gE3C8oKlbyAs1vFBfmDMGc7IO1TryYjAelvACeKK1gEzA4YJgwb9iXigvzCFwKv4JlvzvtAVb85%2FwYmJ%2BtB5C93HNDnICGbbdkAs4cozZNa8va81owQBrdUR1MyB0c3F67g59v8sFnukzgDQfSAhsRgzaVzisWCfrQEcV64gOLscpgk2jB1isM8Zpyqwp2GnKvWIdSgQs2jleSyUehtmsh1HncRLERVdekD%2BtxKri%2FOEV7Ujlz4QtC1c8lEgLXbPOgNCZsHOdsIt2BLTRZ4jws9Uxf0IpM3hFO20xgy%2BAPqZPlEodFiL4TcHGJcCLdjDOKMZn8foHIkICIrhFO3LjiuJk%2FNNlRKnWYTGC3xTsXlRYtCOkEHikKN7zGEkhgxS8oh25pCgOJ%2FtGCjyPM2sKdtkLi3YE9AGPE3jemlpO8Ip2pHKCChEAJ%2FC8tczo7PIUFu0coBNwvDCLlzGRFxJ4wS3akcsLMDnYVOvIi4HJZmBj0Y64TMDhghA2M%2Ffi0VkuE%2BlcaqFbvNCFGddULsPz1HCUAXW3wm8v4ZoMBfKbQDsGh2Vcb%2FvN6ZyPQKgEYOdcE4EO3ne3gQzZ0pu9rOuaLOiIDyEv2VpERODquciQUw%2BI8GksKj0APsoPSSBDgfOaehanbvsDEodwNsGGnXItoo4%2Bo4SfbIi7YKsFh%2FqTEvqIiVKtw6IEvynYsAR40jWGGyUAxcIctZBQf1YC6WVtTrncYXGioC3Y6hzMvBbTCDxe0N%2BJvFDFC%2BUnJhANzNammdyRF3FbsEtgmH8tohCAtMCaTsW0UH5uAtHAVHVmckdabDdSxCzsI5UCkBpY36mWGupPTyAamArPTO5IjbgtOFubYi62uFDgQWPE%2BhvXU8eNAkzJFhSNTjOrRVOyzdZoMGITX9BFaNBFyDrPCWVkj9jqC4gZ2SP0HrZtwXoPexnZGyB03YOQmIktIB54HoVevCyOjJHBGPWJ1zrn%2FE%2BAjKE9ARkzIPR7YNVPeyKCxxqDLTndOCt4hpOoavLhq1H3aL%2F2wldjyFgXXYsGXQujvkg6E74abJo2RNci6xroWhCDLf3E8LUh8QB0KXRkjFLGqA9fDXbaHCRj6s889J8x7Kz5HmPwiMAGVAQPNmM2fv3sP4WO7SaRIAaxotIZjfeD2Mk5Byaa1CB2jEFsqw7GuJEglqeJ9hwMzunjEB2MrGugg0HGFUFs%2FPXjKLbzaVwSHQsB9ZQ4FuNmHYs6j5MiJ4xi1UKGF8VKhgxGsbs9ASETtwVGse2rCBxstHO2VM2xnxxqmnjgngVPgW9519urcTQZfx%2BHUmV7z22wFklisP%2BcKHpLaWStomDfnM6rG%2F2TfPw3PX33b%2Fqw5PWH1903lFSxlcO3f3bf%2FLt9QvJ2%2B7H1O%2Fo5Via0ljtYhY9OmXLoqe8RZV%2FRnfTouqTpSgUWOp4Vuc%2FO3hdpnh%2Bc4%2Bp35ia%2BrEcJDRfahecoBsNJbpKCVzY0kjpJwTmUHv3HBv3HSSOTFDxNtOc%2FTnCSYq9roP9IJhWTFKJQgOdHCqipxI%2BcNOtH1nmcFHnhpIVa6PAmLSRDByctdnsCQidui4pJC5wZP0I98CDDOebyk%2FXgeuUbcmH4moWvY7Ifvo7q7nqRZV00j43svDWMX1s5espsJH6Vm8Vn8uNXKC4EnlS50xYVcWsNAMDzIpo5w7KniXumwNFCoIFzYOwqDhz1aeOmwG4rfduMy8SAddsWbMD6wfI7X4DUDXX0GSXcY1YM3C5DLTiUHzdlmD3ERKnWYVGC2xQ0d2cHElerZffLVDshjj5Dwr%2B9%2FutuevFw89NYuBfkx%2Bz1%2FssAjySszwhGP%2FWxUcgIqadNcRXQl1CiwjrF6u81Irh%2FNrADCRtURp%2F5UJCCy%2FqQEFNwo5vLuTWd%2FOF9e5%2Bt%2FJ%2Bfb55%2F3Q%2BIng6ezWXWph%2F9mkBvq7es1jlffUofsfmq6afaUAF7AoBEFZBdDWSKqFABaUEF5fViu4nYBXrpVia2Rlj3T2bn7rZZaZ%2BrzK%2FX9Y5ZlXXpsLPmtyiq7qxm44P7kWZVWgzTcbPSjZNP0KxsbiqOwfk9SivHYEKf2RmzKvWYlJq1GpiteM0XYWi97dyQThwVOtWDYS7fjB6R9rHuB4ZjPSeUzXdo1vcm7MlLqKQsMOmGlIiZk5JZIaX8B3RDipTYJcGuS6mpYL4zXFA6n3KQF9c9ExzUSUn%2BGCW9vI%2Fm79e1Zrsod62KsAf0dr2HSvMGa%2FuC6lx8vk3V7mLQaZvSc1dPzqgj%2FiLK58iZM9bGWg%2Bm1oOc5wZjTlo%2Ft7Knia0K%2BAZlk%2BvKDQl1bbyy0qO8vxxT6CFcOnacIjhnn%2FayzqO8P2BK1Yg9dWqvyqN00O%2FI6nkr9R3HCqdkOX3Y7HJ6ncdJUJLOeg0ImYOSdBuCTBP1yUdBRmcryBQPJdKSdvX61uo7YXS26qvXKVlNagMeROAuLVWvGPKWDkpZ0ZH5BM7htmjUXIJNtU3H3bIp3Ln%2BapuepkkpZdCkxYuxCmx64Kptbr%2FU3CJs9QeaTgDgS%2B70lg%2BkSS7bkarLubd8q2LaV7FVx%2BpSbw8aSUa5peLJuHwgyd8vZWnZ6H0O%2F3%2Br%2BYL%2BOVb4WFeD%2FEVbZQo8blg5vWQxabCgh1R0x%2BeM34ZBEO3289BazP4MbCe5438%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E" width="100%" height="500" frameborder="0"></iframe>
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
    <iframe src="https://viewer.diagrams.net/?lightbox=1&nav=1&title=Diagrama%20de%20personagem.drawio&dark=0#R%3Cmxfile%20pages%3D%222%22%3E%3Cdiagram%20id%3D%22hC8xNT2k-P87X9VGEyLD%22%20name%3D%22MR%22%3E7Z1rd6I6F8c%2FTdd6zgtnKSjqS7XXqVprb7ZvuqhQpSJYRGvn0z%2BgYNVsIxQMkGTWWWcKRSZm%2F5NfLnvvnIiN8eLCkifDlqmo%2BomQVxYn4umJIBRKpaLzl3vne3WnKEqrGwNLU7yHfm7caf9U72beuzvTFHW69aBtmrqtTbZv9k3DUPv21j3Zssyv7cfeTX37X53IAxW5cdeXdfTuk6bYw9XdilD%2BuX%2BpaoOh%2Fy8XpOrqN2PZf9j7JtOhrJhfG7fEsxOxYZmmvfppvGioult5fr2sPne%2B57frglmqYQf5QGsxvu68nin1vzMpJ150H0bGWc57y1zWZ94XvpTfNF2RFbWma06BvbLb336FOF9j4v5oy2%2FurfrUli3bs5uYd244lrBlzVAt50Zhea3r8mSqLR9f3Rk6%2F0JT%2FjZntv8i%2F6r%2Bri1Upbsym%2FusY8Gm8zL30n35u%2FPyO68w7q9lXRsYzs99pxLcf7FuqVOnLE15antPDO2x7v2I1pj%2F9VXLVhcbt7wavFDNsWpb384j3m%2FFsmdNT85Sybv%2B%2BhFHoeLdG24Io%2Brdkz09Dtav%2FjGZ84NntRAWLCEWxJus62qwPjQt7Z9rKN2r2E0zLq%2B%2FtLEuG464ZWXnVt1cNualOTRdb5i66draMA0VMbf7kGKZk3vZGqi2d2Niaoa9rIdS3fnPqZlG%2Fk%2FppOSUteFcF36unf%2Fcxy27YRpT23Jk5b5Ddaz7pboWrtvmxHuprr7777e8and%2FfjNt2xx7F6gAsI3isCo8FYgBRSAeSwQSIoLOtVuZQv78eq8cnHqwNVnvOt2mbAz0lfGWvaj8YzzAwmCdb9XzpgFURfPf57ZB06nVd33ZDw41RVGdxlv%2FGmq2ejeR%2B%2B5DXw5HtpvtdpsPZsJSYBNu2KxU%2FVPd%2BFMuh7Og9%2B6f%2Boz6cll3%2BjRDtp0WNzOUKaKS9bf4vXDKiHA05UDHT0Y2fse%2BerY%2BddShGYPm6pNSdCGVYhfSAmvnza5ByP%2FJb%2FwRxDh19pu3ExBahWMqcUxJSWOqyjEFtwqOqQPTlDzAqeVMRXOnKpxVIdXEWeWpbbxQdVO5HU%2Bazd5D60Ydj6vPuQqqthNB0j3bGltSkz5n5rKHVxd2zjVjbmw6ghRrzlOG6dn15zHnp4H795XDiZOGeFITjL4mN%2BW%2BrJn%2Bv%2BGUefXPrB7FczJbM3BI9Ki4Q8%2FKc8XC9rS8JJWCoa4gxMA6WETo0gof8ewb8WAXafBtNJWTdLjIAjj8SRRdu60ZIlXo9otvD6HGOlJIA%2BF5E%2BRtJPgiAqMZmAjZG9ccUMuBcU1U6Sy2Db091oh56JIOLRU5ZgJh5uBeQEyYITnJhouM7gikZpZNEDfFwIajHjfo7kCw6Yyi9k1LtjXTyOma4U1qnFKq1uoSmNdoyu%2FmMikBWir1yR7T0F0JzrQkp07VxJkWYvsgNevFMXUU5cDWoh5k6P7Bo6bINXvmNPmUkyUVAqGZJBej2dT4vNbM54tX9a14URcXHcC9qS47fBjKoWbbGVxoRbUTfVG1nCfo6wSak%2Fs6RdlExraQVC6jgiVm2dcJ2yqYGiCANQF5M3kdfhbHB9G2iCNqhbmxAvdQSh4uJBdPwRKz7KGEbRUcLqAPUrCFVK%2F3d5dP16N35%2BcEfEbYol1ohygqaSdOSiNx9u9NO9d6Tx%2Bjq79zTcsV0H3DK1sdXxlzt0pdlRUsPiXekUeluj0jLhCcEMNW5IOWKIMWfMtI5ZQYLjLLwxZ8w2Bq3AJWhQCNW4L289SOF6KqhrkBg4CupXPUEEcNyQkyLAOBo2ZPw%2BCoEUDHVmdawfkSVio080VvtbVZsyO0n2Zfk%2FqL3J0PnvZlosDHd7E5Dd1NQlEOSoX1zShYAK2HUoEPDvZ5IaMKwDaIVE5DwRKjvX8m4lsOdPQBzSUENhczobxgPaHrjlmK5N2mfjr0xIN5cXrjPkNRpq3xkInkrBUsMRQBkfGpakBb8URIwRSCug6dygaN66Kx64bjx9NV%2BV2VSrXHx3vjofd83TEun4ZSzk8UyXFDDjckw1Vgo1coxAtW3pwvhySBbtE2ZlObDcJElQ5HjCet3L3S%2FLy6yQu5bkW9a2r9ijLz%2B0dOGHKEWS%2Bak0AMaHQaJzA4dXPAHBAEuvjadt7JBF4i6obTxdPVt%2FSpPHXvqoXB4PKs2B30qjecLknQJWhS%2BTjoAhqdRrrg1M3pckAQKF3utQkbk5eIuuF0wSX2BZxTXWF1VGtqGvIA4znEputHwbeRf5wOwQgE2IDcLTSK5we%2BUaTS9QMusoDIgE7fD3wjYMoFFK4KyAU0QHeekhHDUfw7omqGZl9QuG54UtMos9CYoJL4cSFCCN%2Bd7M5L8S2AE0VAnXcCThFSwpRUqIRmhiz%2B3bbmr8%2FGy8X3g5RvP8%2FyX1augI5I4z7E4685kBVHOPzcjg3phUoxtxaLhxwh8L5aHBNaWDfoAJaPPX6VfBbfLFM5t4WLjI5GUxPyeJSE1fh2wdSIBK4KaFxKLg%2BQpvwSPCkZDwWZYxPXLHvjoxA%2B8Uxz7uAifkycIzndhouM%2BsCzxDcpsMGo5xuaVUpTWvIkk0lUQ5xHBWR8iCoVmrFi16aXD42ReS3JhYvLT7P%2F8SStkcspEmSlNiZ0kAx4gK1eTLhrOMbCLFbfbGECrgp0GsSMy2lUbbDHBYlzgTgXiIYpwGbfH%2F5IGxiYnD%2FAVYHOH07Vad%2FSlvkmy8v%2Fi2w4j0aVCnucqHJOkOcEyYAD0Oy%2B%2BhjgRDWwdWjnBOA73DBNy6ltVZF7DPMhuESY4wPfpUiCD5XE%2BbB%2FWZEyPgjBrUM9H1DHC48PsiI%2Fs8uHEBKhmQ%2FvHa39PJ6W3qXyw%2BOgc1vundV5ur808CLwwThx8AKUARMJ%2F7ANgCl8gDWBujOcGao10DK5jU1aHMyBg5%2BklQZwBI1nPho40DRtrICDyROzwJoATvp81BSGscGPxdqvFZ7%2FIA3cKCfNDTDcjA1wrJsAJwcQPNZebnefzlWdXX6EUAjNABlPpI%2Fh%2BX1nXC%2FdPbXF84%2F79hPPr5cALsQ8QVyAVqcRDjh5s8UGsCZQNNw5LYUNd9mI0qAZCp3C430rX%2F%2F7quTmi8rFU%2B3sfsihkAQUSAaag1anEQo4ebMFBbAmoGQTq6BuRZtvaSFAIPluoPjBoPQ3uT8aWO6Xy%2FVXwnHf6LRRY%2Brb0I1P3%2Fid7tZWTpGt0f%2Bswdv%2F8qs0CP5f%2F63%2Bdn8jlEqri80f%2Fvvv5DcB79vfY3XPXZCr2TOn79sXBH%2Fo9rKCsxExH%2FF44nzszZJmIOsjZfY4HZ2L57cvVnVenamL99z%2B%2BDYO5KMBmeixgZDVSxQCGSdvtoAM1gTqOHK2mKhe6ErN6Gs%2BdagjRuxSoRkSYBcH5Kus6Zqs7A914qng1mfa%2BzIJnQnuaPlQgMSTfBQQXyY4IbgzUloywQmoSxmDmeAEJiNd4aqAMuUc6PNTMkIgl4UthF7YGzKE8DdjmjG%2Fy8IWnjGJZ2HzX8xmFrZ1e%2BBsEVHPsmxkYUulWmgmy82%2F90F7Matc1mrTxUD5bg9er%2FkWYuQVy%2FDwIJmHDTQ6jTuIOHWzhQmwJhg%2B9zeiMphDAt%2FEIo8EoinYQKvTuImFkzdnArCJxWr%2BtYhCYQ4R%2B9M1ckQcDREks6%2BBVq%2BwgohyYNvQjgh03Zm11GsRBcIcGvyoaM4GkmwgmXkNNvv%2BhUTK4LAO%2B%2Bd0AKKZWcu8FlUiNPMBDufimRBSAAyiqddgHaB9B4UEwTcBpggCVwW6L8FMDp2o2mAPHWiiV44O8uggmXwN1kGI7K20oYPJ3Qu4KtDtC8aS6ERVCM0Amet95U69PZMfLh9zI%2Fm%2BXX5t853tJHBBMucaaHUad7Zx8maLDWBNoGjYSATAABkiyoM5MHAvWPJgIJpdDbQ6jbMGnLw5GAA32FPZMOvylA1X2IjqoJkLjV6581nWi6rw8G9Uvb07nagWwAVVGah%2B1IrTxw7NgWnI%2BtnP3foyUZLqA%2BDnmaa5FIRrmA%2FVtr89cMgz29w2m2Mt67u3efHsvuxPyb88XfgdyPLKB4u60Ozexs8bn3Kufj7kXvifQSXif2VzZvVVXIfvjbFsn1LOZWsxvu68nin1vzMpJ150H0bG2fr4PrfmsOqyVF22tbm6VQ6MdjouEn9UKfphFbsTD%2F8Vq6%2FkfSp%2BraA0IaEVz%2BaFEDZf6ysfTl%2B%2F14q%2Fyp%2BAVoIOEECToqfJpd2kIbuMQCYFLVVCLYrtJlJiUXQFiKBFw3TMR22koEUrqEX1VlubNTtC%2B2n2Nam%2FyN35YJ2TOCUGRbcCroy5%2B93dleCCpfGkOgHGc8Vtcgb1DViP0mK3Kk%2BpE3yCjh3wY9tMKjPqgCWGE%2BokOmE7Svg6tjEwNXsHawJKoxO0u0%2FJNP4o%2BXQiyoa5aT3PphMMLwez6cSDF5LJdOBlnjwiCDqT6WBbA%2BcL4JusKR3VmjrTvYE6zhJb0iIZ5tgSxq%2BZabgQmruQTLYDCwI6vCHt%2B47xdBMhkrlTjxbUd%2Flem6R%2BupIKbdDMkPq9cK%2F2K0%2FCdDR6Vmq31%2FnGbba2HVF7AyvOuFFEineFQOskutH3qz2EY1hUnJRG4uzfm3au9Z4%2BRld%2F55qWKwCbCLjFCfIWlZ9nRuNc7nZf5%2FbjV6FVzI96OXTYf2VjhvsZ3DnYa9Lg3W%2Bh4PeEIUdW64CR2O3Gh9rB13FQBWCbQir3BsASo8PrTOwNhPbdwrYApgbYYE2g42tNwfbiKRlhB9kQIK0VmgfcYNWECChkGiTw6DAekJDcBQBLHMLpIDXrNPH0DMEX1WinCOpocPB01BAnra5WfPacOJpuTKVBfMxhCfV34FgijSWS%2BwdgiUM4K1CGpUpgW9GOJcBBIU4urY4C4Fz6pfqY4xLP4ZYCMBE9MgAucoj1V8rQxGYKN7gq0AXY25ls2JoiK2xE1UZVCM38EO%2FLZlkcFcsPL%2Fr9W%2FFFaZpX%2FPiABGhB8vQA0Og0nh6AUzdbaABrAp26dmWLHS5EVAdzWOBHByTABZInB8BWp%2FHkAKy%2BORmgqWPHUlcHj5kNczyx2MgBHVUn7DECzcnBGXFkRhA9LAC2%2Bv7MrbQxQgxsHeoZgXrl%2FDDiUTUYOSYgqkzYQ4SE6IJk%2BET%2BhJCzvf%2FgprM9zvGPvLN9pd36N%2F%2Be1m7vmsqLrgjFe0NOOLglpHWOllNvvFB1U7kdT5rN3kPrRh2Pq8%2B5ShG1KFiHYtwW9T66k1IvJ%2Firhr6zt1TafseqpEhOvZplyd8bj3lDov3%2FUHEnBZEkljbfd%2FgDglTaUeaqDL%2FtWcBqRyctTbkv8xxTAfCTKxZ2DBZ4%2BzKOUSWuFfFd7KiR2tjGkspIErDEaAiBG0nivCtPZzYQbKNgav4B1gQ6%2FdCUA%2F19SuYdR0kyFVEtNE9DrNd3e%2FK8aL1Jg7byMOya5vSCHzaTKExIRpOA5kd7DzohgtM%2BWxABawINKtKUS%2FlN0zO7DX5AIdsii1suNFME7Ph4JtxgWDmY7yAerJCMBgFLjAao0YkVbGNgCitgTUCZcFvyJJM7ItGAElEozAGF576NsqEeD0WIhm7AmzBQQFmiXccxdtixDYBDBAjjWkUCZo8hpKVBMzbq348v773HReX19O3r2ejUvq8%2B%2BWpWApQgGbIBGp3Gk5Nx6maLCWBNoOsNp%2Bq0b2krt6vl%2F8XU73%2BkQSg0E8KuTS8fGiPzWpILF5efZv%2FjSeLRG0kggmT0Bmx1GqM3sPpmCxJwVfhC%2FaFEwzQtp7ZVRe4xQYeoEmEODzzmmzgdiMZtgEanMeYbp27OBmB92UODrMjP7KKBh33vX4ZERxOcFcRZUSTIClgGWTwnKZ51ZzbPSYKrAnXCftQYifSLqg32yMHztqeAHOXEycFE5nZ8C%2BDkKKCuce3lfsXpXNUZ5gfPr%2B6%2BbVidC9Ko8dE7653fCP37xrtp803tQ7RARBMUIHtpIeYJ0gI0Oi2b2gdss1%2FwVKMB%2FNro%2BOBsMVG9Te2a0dfonV%2FEqBKa8XB6pS%2FeLv7Orm96F%2FmPQj3%2FdFMDjoVsDNX3%2Ff5xPNp%2FHe1f9rv5RKL9QWvyVcbg9McOM7FtJZXR%2FmCJ4XMj6Y32xzYKpqaPYE1A50fiu%2FuUDA2OEuwfUSw0DxXACNb9XlCcJcdnSeLB%2FujYgk6G4LTPFkPAmkCHFFkK9k%2BjYmgGCdj38R2tYGQ5GO8fD1lIxvuDJUaXrugkC7YxMEUWsCbQvS1W4%2F0jCoU5oPAzhKO4SMRDEaLx%2FmCRmThEGKt%2FzhAg5wMz4f4RpUEzNcA4V76eRR4SiYf708gEnLrZYgJYE%2BiKFQ%2F3%2F5VQaCYEGNDEfefIEyLxaH9afOcOhusxmRAGrAl0AZKH%2BocSCHNk4HMH4mRIPtKfxrkDTt2cDMDcgUf6hxIIzWSA%2BzXUo5qzgjgrSEb6w0UWgssgu%2FTAtwCm8AFXBcoPZiL9o2qDPXKg7tmcHMTJQTLSHy5yCPc42sjB5JIUXBXomhRjkf5RFUIzP8CQVr4mFS3Sfz9A9tIi%2BUh%2FWtjwmxhu%2BtEAfm10TsEj%2FcOrhGY83J1Nr5rtRilnlCa1YrNiaJ8QHlRloPpeyE5XOzQHpiHrZz9365ZbGtXnwM8zTXMpCNcwH6ptf3v8kGe2uW02xzTWd8%2FvK9yLZ%2FfiT8m%2FPF1s%2FvLU54u60Oye%2Fw7n541POVc%2FH3Iv%2FM%2BgevC%2Fsjmz%2Bt53xp3wbPusci5bi%2FF15%2FVMqf%2BdSTnxovswMs5y%2FgvdisOOPSxVl21trm4VY690apYlf2884GHy580d98aPZnPrrRB%2F0iKVNhVz%2BAOV0o7CVkWIVW8omTKgt3zcesMFGSelN0QfolD8U5B%2B%2FpS3xFLa6atWxfZeEX8%2FVU1UN4WU9FMXo9nU%2BLzWzOeLV%2FWteFEXFx3fmXdTN%2BOFqpvK7XjSbPYeWjfqeFx9zlVi103QMSpo0SK6olGXnRnIcP9AhaeZWffdRaTvDjjnWN%2BM36D8xObgc0%2FsIge%2BvaQy0QxcZDR4r0NlDCe%2BPTC1bglXBXRq86HePiXT0qNkmYkqGObmqWWRsyRJlpBMNAMLAN0HpTMfAFb%2BnCW5Mjpv0JS%2F5kBWHENmiCWpEQx7LMlzliTJEpKpZWABoN6YLLEkH9hg1LNEAFhS0zWHJRwlv9ALcyiR%2BOGeiaKEaH4ZWAHo0gZDLJGYPP4Trgo001AG8yinRi7MoaQYIlMV02w5mAAzLraQTEsDltkvAJtsWTcIzpYSOmHVlCunIS29%2BwTXu68p92WNz1p%2Box7mUFOWEJ2k2JsGNTjgGYMdbmy6xuBcr1LiGVNGJ5UpNs%2FHbDzxiyZb%2FZMjus1hG3oC%2Fk%2B%2F89Pcdd0p5PMHHDWLYtRPVA59APEFDfsBybs%2BqvdouZJoy8jH1TJidwzE7gFttozFv9vW%2FPXZeLn4fpDy7edZ%2FstaByQn3TIK0ramqsIBEe5%2BYMfl%2BUgizJQvauIizAcUoSClQoSl8o4GS3gN7j4ftwTBY0SSHSBE7gYDqQl3fsqmmPRWW5s1O0L7afY1qb%2FI3fngKf4B3e86tPKuOKoHOrTdDxTylTz2E0Il4gd2QH8cvWYc27%2FXazFbei1UQ%2Bp19wMVEf%2BBQjni8yTU6mfpyYZc94qTvOiCznrL9%2BqlcF9R7wrzx5uOeH75Pb8Ezhzuqn1Vs%2BVpwzSGal9T5CliFx4ZgkSGrBeZvCZTDhoGUMWsa0WyrIBYFm9HVjc2Dm6aY9tNKsNCwBKzdv4wtlEwtbkB1gR0%2FnAG%2FXljiw2JKBeadzPAquEHR8a0bx4PXkhGioAlRsNQGcQLkwdIgjUBHSDpzSw4XsLLhTm8FNDzXlK8GnC0vVfcqCSzG0zlcsIbTOV3VSrVHh%2FvjYfe83XHuHwaSsBKiHuUutNG7P2upHwBZN0z7Wx9C0FdxNfpwSONSCCD8gWQuBZAcM0lnQsgUImZWwDBNQq2RqhQTUALIId7fKrHqNEEQ%2FUYFaoavgQS1xJILIAhugQClRhdAmEILGwufUA1AS19tORJptY90qIV5piCxrVypgQ%2FdyQekJDMlAGWOERMYrYyyx%2B0VSWwrWiniO%2Fov3noiPPStEMkDdKgGRqK1b0emf%2FGjdfWrS1dFrr5QRNwTOaMODIjiKbAAI2Oevdmnwk4dbPFBLAm0HHBqTrte6eNlJf%2FF1MfjJwGoTBHCHQ3lRPi2IQgmcgCNHqJFUIweVQhWBPoEqR3RrqqyD12ycBPKtxbNfykQvJkqCRNBhrXk3Dq5mQAvB88MsiK%2FMwuGfgZ6Pv7NdQjjrOCNCvWCV8S24zw43IZ3I0oMIkPuCqAk26nE7XvWFtTZIXhfYkQImEOIQJ9Ke9wTnJZObS2tJtw4sCZtbvPx3xkbbGoFO7Mvze1T0usNCqVofF4A7jjt9WB6R6oHWixm3vm%2B8ar7qSMKwUdUcTimQ%2FaNsSIgvmBJRZI2JaTSs98sMSwZ36iA4qjOMNhGwNTY0ywJiCP%2FFCdfkrGmkdxzo%2BoHZqHnnAvyJ1ikmQKSWd8uMSsnBCDVT%2BnSq4AnRBzZavjLGEkNWphjyPcdSZJjpD0xYdLjEb5scQRJl1r4KpAfWsymTEtNYJhDiU8XjgYWg7GC8eDFqIu%2FGCRWQkYxrYGThYoYPhRdffAOFl%2BoxfmwMKDhlM1ZyHq%2BQ8WOYsBxPH0EkwGEMOyRQOIb2eyYWfWXYe0QGjGiPL37HNRuhLuGqp49XFfuap%2B6TwUIFlqEI0KgOxPIyRwQmcLEmBNAJ4XlrrabDfPNcNp5CyAIqJIaAYF3LfxyIBUoYNokABcZIHZGQebQQJwVaA4udcmqffXSoU2aIYIyNdMJfhH7Q2EBmB9KzZjA%2BTnmdE4l7vd17n9%2BFVoFfOjXnLnAoLWQXNHZD1wA7eovGkcXIBHSoyTbFRNyKbzm7MxfnkYLHZHOivHZVTy2%2FEaUgEfnIM87%2FXvgU%2FXCP2BuI%2FjMMU7pXOtS5eLjzdNMabawBb3HMehu4uXh5wuMhj7s1feEY4gXR%2FJQeIIUtCGISYFzE8TUQVgm0Uqg3vAEqf42I3ogeTbjT6YCYXAJqRovgjWRIbPII2olVLsWqF5%2FghWDfemSx4uJKN8wBKn%2BNTRZODCpFcdWBOQV91yCpFZB4gj8IU71e2tmioiERKLLL9YLDnqmiZuVJKVFRV0xSPpA0hh%2BuaTVFwh1YoD1mn1VlubNTtC%2B2n2Nam%2FyN354InYOq1zaZmmvSkApz8etkxFdZ%2F4Pw%3D%3D%3C%2Fdiagram%3E%3C%2Fmxfile%3E" width="100%" height="500" frameborder="0"></iframe>
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
      <img src="https://raw.githubusercontent.com/SBD1/2025.1-Marventura/refs/heads/main/docs/assets/modelo-relacional-Completo-v1.1.drawio.png" alt="Diagrama Relacional">
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
| `2.5` | Normalização do diagrama dos Personagens | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 16/06/2025 |
| `2.6` | Correção das restrições de chaves do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 16/06/2025 |  |  |
