INSERT INTO efeito
    (nome, valor)
VALUES
    ('Cura', 1),
    ('Cura', 2),
    ('Cura', 3),
    ('Cura', 4),
    ('Cura', 5),
    ('Cura', 6),
    ('Cura', 7),
    ('Cura', 8),
    ('Cura', 9),
    ('Cura', 10),
    ('Cura', 11),
    ('Cura', 12),
    ('Cura', 13),
    ('Cura', 14),
    ('Cura', 15),
    ('Cura', 16),
    ('Cura', 17),
    ('Cura', 18),
    ('Cura', 19),
    ('Cura', 20),
    ('Energia', 1),
    ('Energia', 2),
    ('Energia', 3),
    ('Energia', 4),
    ('Energia', 5),
    ('Energia', 6),
    ('Energia', 7),
    ('Energia', 8),
    ('Energia', 9),
    ('Energia', 10),
    ('Energia', 11),
    ('Energia', 12),
    ('Energia', 13),
    ('Energia', 14),
    ('Energia', 15),
    ('Vida Máxima', 1),
    ('Vida Máxima', 2),
    ('Vida Máxima', 3),
    ('Vida Máxima', 4),
    ('Vida Máxima', 5),
    ('Vida Máxima', 6),
    ('Vida Máxima', 7),
    ('Vida Máxima', 8),
    ('Vida Máxima', 9),
    ('Vida Máxima', 10),
    ('Vida Máxima', 11),
    ('Vida Máxima', 12),
    ('Vida Máxima', 13),
    ('Vida Máxima', 14),
    ('Vida Máxima', 15),
    ('Energia Máxima', 1),
    ('Energia Máxima', 2),
    ('Energia Máxima', 3),
    ('Energia Máxima', 4),
    ('Energia Máxima', 5),
    ('Energia Máxima', 6),
    ('Energia Máxima', 7),
    ('Energia Máxima', 8),
    ('Energia Máxima', 9),
    ('Energia Máxima', 10),
    ('Sorte', 1),
    ('Sorte', 2),
    ('Sorte', 3),
    ('Sorte', 4),
    ('Sorte', 5),
    ('Sorte', 6),
    ('Sorte', 7),
    ('Eletrificado', 0),
    ('Eletrificado', 1),
    ('Congelado', 0),
    ('Congelado', 1),
    ('Molhado', 0),
    ('Molhado', 1),
    ('Envenenado', 0),
    ('Envenenado', 1),
    ('Sangramento', 0),
    ('Sangramento', 1),
    ('Queimadura', 0),
    ('Queimadura', 1),
    ('Tontura', 0),
    ('Tontura', 1),
    ('Cegueira', 0),
    ('Cegueira', 1),
    ('Purificação', NULL);



INSERT INTO acessorio
    (nome, descricao, raridade, local_encontrado,
     preco_de_compra)
VALUES
    ('Botas de Areia Firme', 'Essas botas estão sempre secas. Sempre. Mesmo dentro d’água.', '★★', 'Loja de Acessórios', 35),
    ('Coração de Coral', 'Um pingente delicado que pulsa junto com o seu. Um toque de vida extra.', '★★★', 'Loja de Acessórios', 60),
    ('Ampola da Brisa do Mar', 'Um frasquinho com o ar mais fresco da costa. Inspira fundo e sente o vigor voltar!', '★★', 'Loja de Acessórios', 40),    
    ('Bracelete Estrela-do-Mar', 'Brilha no escuro e traz uma paz estranha — talvez um pouco demais.', '★★★', 'Loja de Acessórios', 65),
    ('Luva de Lobo Feroz', 'Dizem que era de um lobo muito nervoso. Agora é só estilo e poder.', '★★', 'Loja de Acessórios', 35),
    ('Faixa da Força da Vovó Yuba', 'Costurada entre uma sopa e outra, essa faixa guarda o cheiro de tempero e a força de mil panelas batendo.', '★★★', 'Loja de Acessórios', 60),
    ('Olho de Sorte', 'Um broche com um olho pintado que “pisca” quando você se esquiva de um golpe.', '★★', 'Loja de Acessórios', 55),
    ('Bandana do Incrível', 'Dizia-se que quem a usava nunca perdia... ou pelo menos parecia bem confiante.', '★★★', 'Loja de Acessórios', 85);



INSERT INTO arma
    (nome, descricao, raridade, tipo_arma, local_encontrado,
     preco_de_compra)
VALUES
    ('Espadinha do Marinheiro', 'Básica, reta e sem sal — igual à comida do quartel.', '★', 'esp', 'Loja de Espadas', 50),    
    ('Corte de Areia', 'Uma lâmina fina, feita para deslizar no calor escaldante do deserto. Melhor usar antes que enferruje.', '★', 'esp', 'Loja de Espadas', 55),
    ('Gume de Coral', 'Forjada com pedaços de coral duro. Linda, mas cuidado com lascas!', '★★', 'esp', 'Loja de Espadas', 80),
    ('Espada Fantasma', 'Você jura que ela está na sua mão, mas às vezes… ela desaparece.', '★★', 'esp', 'Loja de Espadas', 90),
    ('Cortadora do Capitão', 'Usada por um lendário capitão que dizia "o melhor ataque é um grito seguido de corte".', '★★', 'esp', 'Loja de Espadas', 90),
    ('Lâmina da Brisa', 'Tão leve que quase voa sozinha. Ideal para quem gosta de parecer estiloso enquanto luta.', '★★★', 'esp', 'Loja de Espadas', 105),
    ('Lâmina Sussurrante', 'Dizem que ela corta o ar tão silenciosamente que até o vento pede licença.', '★★★', 'esp', 'Loja de Espadas', 110),
    ('Katana do Sushi Supremo', 'Corta peixe tão bem que o próprio mar fica com inveja. Também serve pra vilões, se estiverem quietos o suficiente.', '★★★', 'esp', 'Loja de Espadas', 140),
    ('Katana da Vovó Yuba', 'Ela usava pra cortar carne, peixe e argumentos. Respeito e corte limpo em cada golpe.', '★★★', 'esp', 'Loja de Espadas', 150),
    ('Katana do Capitão Caído', 'Roubada de um lendário capitão samurai que confundiu o oceano com arrozal. Ainda tem cheiro de saquê.', '★★★', 'esp', 'Loja de Espadas', 165),
    ('Estilingue de Iniciante', 'Feito com elástico e madeira de galho. Não subestime a força de uma boa gambiarra.', '★', 'est', 'Loja de Estilingues e Arcos', 30),
    ('Lança-Suspiro', 'Disparar projéteis doces não é eficaz, mas é surpreendentemente ofensivo ao ego inimigo.', '★', 'arc', 'Loja de Estilingues e Arcos', 45),
    ('Estilingue Crocante', 'Feito com casca de noz e muita teimosia. Dizem que acerta melhor se estiver com fome.', '★', 'est', 'Loja de Estilingues e Arcos', 45),
    ('Arco de Liana', 'Um arco feito com cipós flexíveis e muita criatividade. Tensão máxima, estilo selvagem.', '★★', 'arc', 'Loja de Estilingues e Arcos', 65),
    ('Atira-Coco', 'Não é elegante, mas já derrubou mais de um pirata. Lançar cocos exige força… e coragem.', '★★', 'est', 'Loja de Estilingues e Arcos', 70),
    ('Arco do Oásis', 'Suave e silencioso como uma brisa no deserto. Ideal para acertar antes de ser visto.', '★★★', 'arc', 'Loja de Estilingues e Arcos', 125),
    ('Estilingue de Batalha Naval', 'Usado por um pirata que confundia navios com alvos de treino. Deu certo… até certo ponto.', '★★★', 'est', 'Loja de Estilingues e Arcos', 125);



INSERT INTO fruta
    (nome, descricao, raridade, local_encontrado)
VALUES
    ('Mimi Mimi no Mi: Fruta do Eco', 'Uma fruta rara, de cor chamativa e com um aroma meio doce, meio… enxerido. Quem a come desenvolve habilidades sonoras peculiares — perfeitas para quem adora ouvir, repetir e, claro, se meter onde não foi chamado.', '★★★', 'Missão');



INSERT INTO nao_consumivel
    (nome, descricao, raridade, local_encontrado,
     preco_de_compra, preco_de_venda)
VALUES
    ('Abóbora Redonduda', 'Grande, laranja e cheia de personalidade. Ótima para sopas, risos e sustos.', '★', 'Ilha de Borabóia', 15, 6),
    ('Arroz do Planalto', 'Grãos branquinhos que dançam quando caem na panela. Base de quase tudo!', '★', 'Ilha de Borabóia', 10, 5),
    ('Ovo dos Campos', 'Um ovo fresquinho, coletado de aves que vivem soltas pelos campos. Dá vontade de fritar, mas também pode virar algo mais sofisticado.', '★', 'Ilha de Borabóia', 10, 5),
    ('Carne de Ave Brava', 'Um pedaço de ave com gosto de aventura. Cozinhe bem ou corra risco de bicadas!', '★', 'Ilha de Borabóia', NULL, 7),
    ('Presa de Lobo', 'Um dente afiado arrancado de um lobo valente. Não é comestível, mas é estiloso.', '★★', 'Ilha de Borabóia', NULL, 15),
    ('Farinha Misteriosa', 'Ninguém sabe de onde veio, mas faz bolos ótimos. Melhor não perguntar.', '★', 'Cidade de Lurien', 10, 5),
    ('ButterCream de Fuligem', 'O preferido dos confeiteiros da cidade, feito com um toque especial de cana-de-açúcar e... partículas do ar local.', '★★', 'Cidade de Lurien', NULL, 15),
    ('Farinha Misteriosa', 'Ninguém sabe de onde veio, mas faz bolos ótimos. Melhor não perguntar.', '★', 'Cidade de Lurien', 20, 8),
    ('Medalha de Marinheiro', 'Símbolo de honra… ou corrupção. Não serve pra comer, mas pode abrir portas.', '★★', 'Cidade de Lurien', NULL, 20),
    ('Pérola Cantante', 'Emite um som suave quando tocada. Dizem que revive quem ouve sua melodia até o fim.', '★★', 'Ilha Glacial de Frimora', 30, 17),
    ('Pedaço de Tecido Rasgado', 'Um trapo que já foi parte de um uniforme pirata. Cheira a nostalgia e mofo.', '★', 'Ilha Glacial de Frimora', NULL, 8),
    ('Lamento Gelado', 'Um fragmento de tristeza congelada. Só aparece quando almas inquietas são libertadas.', '★★', 'Ilha Glacial de Frimora', NULL, 12),
    ('Faixa de Pirata Estorricado', 'Um pano ressecado de pirata que enfrentou o sol por tempo demais. Ótimo pra rituais e costura.', '★', 'Cactuaraquara', NULL, 10),
    ('Fragmento de Miragem', 'Um cristal etéreo que brilha e some quando você olha fixo. Nasceu da confusão de mentes perdidas.', '★★', 'Cactuaraquara', NULL, 12),
    ('Sombra Engarrafada', 'Uma sombra viva que foi capturada. Útil em receitas que assustam até o cozinheiro.', '★★', 'Nublária', NULL, 17),
    ('Açúcar Estranho', 'Doce, crocante e... será que isso tá brilhando? Ideal para doces perigosamente bons.', '★', 'Nublária', 5, 2),
    ('Essência de Névoa Doce', 'Um xarope espesso que adoça e assusta. Parece açúcar, mas sussurra nomes perdidos.', '★★', 'Nublária', 10, 4),
    ('Asa de Morcego Noturno', 'Negra como a meia-noite sem lua. Serve para receitas, poções e decoração gótica.', '★', 'Nublária', NULL, 9),
    ('Presa Venenosa', 'Brilha com um verde nada confiável. Cuide para não furar o dedo ao manusear.', '★', 'Nublária', NULL,  7),
    ('Peixe Saltitante', 'Ainda parece se mexer! Ideal para grelhar, cozinhar ou assustar aprendizes.', '★', 'Quartel Naval D-57', NULL, 11),
    ('Pepino de Salmoura', 'Conservado com tanto sal que chega a arrepiar a alma. Dizem que dura uma década.', '★', 'Quartel Naval D-57', NULL, 5),
    ('Chapéu de Marinheiro', 'Simboliza status, disciplina e... bom, é só um chapéu suado. Não comestível.', '★★', 'Quartel Naval D-57', NULL, 15);



INSERT INTO consumivel
    (nome, descricao, raridade, local_encontrado,
     preco_de_compra, preco_de_venda, e_fabricavel)
VALUES
    ('Fruta do Mar Azul', 'Uma frutinha brilhante e saborosa! Recupera energia e pode causar inveja em gaivotas.', '★', 'Ilha de Borabóia', NULL, 5, FALSE),
    ('Fruta do Mar Vermelha', 'Mais doce e vibrante que sua prima azul. Dizem que aquece até o coração gelado.', '★', 'Ilha de Borabóia', NULL, 5, FALSE),
    ('Folha de Hortelã', 'Refrescante, cheirosa e ótima em chás ou nas mãos de piratas resfriados.', '★', 'Ilha de Borabóia', NULL, 5, FALSE),
    ('Maçã Lustrosa', 'Brilha tanto que você se vê nela. Tão docinha quanto promessas de marinheiro.', '★', 'Cidade de Lurien', NULL, 7, FALSE),
    ('Repolho Redondo', 'Enrola mais que muito pirata mentiroso. Cru ou cozido, sempre útil.', '★', 'Cidade de Lurien',  NULL, 5, FALSE),
    ('Alga Fresca', 'Parece nojenta, mas dizem que é cheia de nutrientes. Piratas fitness adoram.', '★', 'Cidade de Lurien', NULL, 6, FALSE),
    ('Chá Enlatado', 'Vendido em latas esquisitas. Tem gosto de “quase chá”, mas funciona.', '★', 'Cidade de Lurien', 15, 6, FALSE),
    ('Doce Amassado', 'Parece que foi esmagado por um punho gigante. Ainda doce, com gosto de luta.', '★', 'Cidade de Lurien', NULL, 2, FALSE),
    ('Noz Crocante', 'Pequena, dura e barulhenta. Ideal para mordidas rápidas ou espantar pinguins curiosos.', '★', 'Ilha Glacial de Frimora', NULL, 2, FALSE),
    ('Ervas Aromáticas', 'Um cheirinho que aquece a alma. Ótimas para chás, sopas ou magias de vovó.', '★', 'Ilha Glacial de Frimora', NULL, 3, FALSE),
    ('Neve Mágica', 'Parece gelo raspado, mas derrete em cura. Tente não comer tudo de uma vez.', '★★', 'Ilha Glacial de Frimora', NULL, 12, FALSE),
    ('Leite de Cabra Alpina', 'Quentinho, cremoso e nutritivo. Perfeito para combater o frio e o mau humor.', '★', 'Ilha Glacial de Frimora', 10, 6, FALSE),
    ('Chocolate Amargo', 'Amargo como a vida no gelo. Derrete o cansaço e o coração congelado.', '★', 'Ilha Glacial de Frimora', 15, 8, FALSE),
    ('Fruta Cítrica do Oeste', 'Azeda, suculenta e cheia de energia solar. Ótima pra acordar até múmia adormecida.', '★', 'Cactuaraquara', NULL, 4, FALSE),
    ('Côco do Oásis', 'Pesado, difícil de abrir, mas vale cada gole. Ideal pra hidratar e bater na cabeça dos outros.', '★', 'Cactuaraquara', NULL, 7, FALSE),
    ('Areia Mineral', 'Tem gosto de... areia. Mas misture bem e talvez vire um tônico impressionante.', '★★', 'Cactuaraquara', NULL, 10, FALSE),
    ('Carne do Deserto', 'Picante o suficiente pra te fazer cuspir fogo. +1 em coragem depois de comer.', '★★', 'Cactuaraquara',  20, 8, FALSE),
    ('Geleia de Cacto Doce', 'Um docinho raro feito do néctar de um cacto bem zangado. Cuidadosamente colhida!', '★★', 'Cactuaraquara', 11, 6, FALSE),
    ('Suco Refrescante Solar', 'Tão gelado que parece mágica. Refresca mais que mergulho em fonte sagrada.', '★', 'Cactuaraquara', 7, 4, FALSE),
    ('Cogumelo Risonho', 'Tem uma carinha feliz. Ninguém sabe por quê. Comer pode causar risos... ou arrependimentos.', '★', 'Nublária', NULL, 9, FALSE),
    ('Fruta Fluorescente', 'Brilha no escuro! Alguns dizem que tem alma própria.', '★', 'Nublária', NULL, 7, FALSE),
    ('Doce Fantasmal', 'Derrete na língua e deixa um leve arrepio na espinha. Doces espíritos aprovariam.', '★', 'Nublária', 13, 5, FALSE),
    ('Ração de Soldado', 'Embalada à vácuo e sem gosto. Mas dá energia e fortalece o espírito patriótico.', '★★', 'Quartel Naval D-57', NULL, 10, FALSE),
    ('Biscoito de Gengibre', 'Na ala dos oficiais, um confeiteiro reformado da Marinha mantém a tradição de assar biscoitos para “manter a moral da tropa”. Só não conte pros recrutas — é só pros superiores.', '★★', 'Quartel Naval D-57', 12, 7, FALSE),
    ('Café Turbinado', 'Tão forte que acorda até os mortos e os marinheiros de plantão.', '★', 'Quartel Naval D-57',     8, 3, FALSE),
    ('Carne de Rei dos Mares', 'Gigantesca, rara e cara. Cheia de proteína e orgulho militar.', '★★★', 'Quartel Naval D-57', 40, 19, FALSE),
    ('Rosquinha Mordida', 'Quem mordeu e largou? Ainda tá boa. Restaura pouco, mas serve como prova de negligência.', '★', 'Quartel Naval D-57', NULL, 3, FALSE),
    ('Sushi Enrolado', 'Enrolado com carinho e peixe saltitante! Um lanche leve, mas cheio de sabor.', '★★', 'Cozinha', NULL, 15, TRUE),
    ('Chá de Algas', 'Um gole desse chá marinho e você sente até as ondas te abraçando por dentro.', '★', 'Cozinha',  NULL, 10, TRUE),
    ('Pastel de Fruta do Diabo', 'Ardido e adocicado, um quitute perigoso para os mais ousados.', '★★', 'Cozinha', NULL, 18, TRUE),
    ('Caldo da Vovó Yuba', 'Uma sopa tão boa que parece que te dá um abraço. Feita com amor... e pimenta!', '★★', 'Cozinha', NULL, 22, TRUE),
    ('Tônico de Areia', 'Tem gosto de areia? Sim. Funciona? Mais do que você imagina!', '★★', 'Cozinha', NULL, 16, TRUE),
    ('Chá Gelado de Neve', 'Refrescante até congelar os pensamentos. A escolha perfeita pra esfriar os ânimos.', '★★', 'Cozinha', NULL, 15, TRUE),
    ('Receita Secreta do Capitão', 'Uma mistura poderosa e misteriosa, só os verdadeiros líderes se atrevem a provar.', '★★★', 'Cozinha', NULL, 27, TRUE),
    ('Carne Grelhada', 'Crocante por fora, suculenta por dentro. Perfeita para qualquer fogueira.', '★★', 'Cozinha', NULL, 18, TRUE),
    ('Pérola Caramelizada', 'Crocante, mágica e doce. Dizem que revive até o humor de um pirata carrancudo.', '★★', 'Cozinha', NULL, 13, TRUE),
    ('Pérola da Lua de Inverno', 'Um doce etéreo que brilha como a luz da lua sobre a neve. Quem o come sente o universo piscando para si — e os dados da vida rolando a seu favor.', '★★★', 'Cozinha', NULL, 24, TRUE),
    ('Pérola do Sol Escaldante', 'Forjada no calor do deserto, essa pérola brilha como o sol ao meio-dia, aquecendo o corpo e dando força para suportar o calor implacável.', '★★★', 'Cozinha', NULL, 24, TRUE),
    ('Gelado de Algas', 'Uma sobremesa geladinha com gosto do mar e um toque de frescor sobrenatural.', '★', 'Cozinha',  NULL, 15, TRUE),
    ('Omurice de Arroz', 'Receita tradicional dos viajantes do campo, famosa por causar nostalgia e fome ao mesmo tempo.', '★★', 'Cozinha', NULL, 15, TRUE),
    ('Bolo do Campo', 'Um bolo simples, mas saboroso, feito com ingredientes fresquinhos do campo. Perfeito para uma pausa na aventura!', '★★', 'Cozinha', NULL, 14, TRUE),
    ('Bombom Nebuloso', 'Um docinho que parece derreter em névoa assim que toca a língua. Feito com carinho (e um pouco de sombra).', '★★', 'Cozinha', NULL, 12, TRUE),
    ('Arroz dos Sete Mares', 'Uma tigela robusta de arroz misturado com sabores do mar. Os marinheiros juram que dá sorte.', '★', 'Cozinha', NULL, 9, TRUE),
    ('Doce da Ilha', 'Um doce feito com coco e calda cítrica, lembra o pôr do sol nas dunas do deserto.', '★★', 'Cozinha', NULL, 12, TRUE),
    ('Omelete dos 4 Ventos', 'Leve e fofa, com o sabor do campo e a brisa das planícies.', '★★', 'Cozinha', NULL, 13, TRUE),
    ('Frango Assado Estaladiço', 'Crocante por fora, macio por dentro. Tão bom que até o corvo queria roubar.', '★', 'Cozinha', NULL, 10, TRUE),
    ('Sopa da Guarda Noturna', 'Revigorante e quentinha, ideal para noites frias e perseguições por becos.', '★', 'Cozinha', NULL, 6, TRUE),
    ('Doce de Duna Dourada', 'Doce exótico feito com frutas do deserto. Cuidado: pode atrair camelos.', '★★', 'Cozinha', NULL, 16, TRUE),
    ('Bife do Abismo', 'Um corte suculento direto das profundezas do mar. Tão macio que derrete na boca, mas tão forte que faz os músculos tremerem.', '★★★', 'Cozinha', NULL, 35, TRUE),
    ('Sashimi do Fim do Mundo', 'Cru, fino e perfeitamente cortado. Dizem que só quem já viu o mar no escuro da lua nova entende seu verdadeiro sabor.', '★★★', 'Cozinha', NULL, 35, TRUE),
    ('Torta do Marujo Feliz', 'Um clássico entre os navegadores nostálgicos. Um pedaço e você esquece do enjoo... e do resto da tripulação.', '★', 'Cozinha',  NULL, 10, TRUE),
    ('Doce Assombrado', 'Não se sabe se o sabor é bom ou se é só a maldição agindo. Textura perfeita... demais até.', '★★', 'Cozinha', NULL, 12, TRUE),
    ('Curry do Capitão Covarde', 'O cheiro é intenso, o sabor é duvidoso, mas nenhum pirata consegue parar de comer.', '★★', 'Cozinha', NULL, 13, TRUE),
    ('Elixir Sombrio', 'Bebida proibida sussurrada em tavernas assombradas. Quem é que vai querer beber isso...?', '★★', 'Cozinha', NULL, 18, TRUE),
    ('Poção do Dente Torto', 'Um gole é suficiente para se sentir... diferente. Tem certeza que isso não é veneno?', '★★', 'Cozinha', NULL, 18, TRUE),
    ('Cookie de Chocolate', 'Crocante por fora, macia por dentro. Derrete na boca como a neve da infância.', '★', 'Cozinha', NULL, 14, TRUE),
    ('Leite Condensado Alpino', 'Um creme docinho e suave.', '★', 'Cozinha',  NULL, 11, TRUE),
    ('Chocolate Quente', 'Um gole e você sente como se tivesse abraçado um urso de cachecol... que acabou de sair do banho e decidiu virar seu terapeuta de plantão.', '★★', 'Cozinha',  NULL, 15, TRUE),
    ('Doce do Silêncio Eterno', 'Um doce que ecoa sussurros antigos. Quem come diz sentir a presença dos que partiram.', '★★', 'Cozinha', NULL, 17, TRUE),
    ('Cacto-Pop Geladinho', 'Uma explosão refrescante e pegajosa! Perfeito para os dias escaldantes no deserto.', '★★', 'Cozinha', NULL, 16, TRUE),
    ('Esfera da Miragem', 'Parece sólida, mas será que é? Um doce ilusório que desorienta quem o encara por muito tempo.', '★★', 'Cozinha', NULL, 17, TRUE),
    ('Pickles Pirata', 'Um prato inusitado e ousado. Os piratas juram que melhora a mira (e o hálito!).', '★', 'Cozinha', NULL, 10, TRUE),
    ('Frankenprato', 'Uma aberração culinária nascida da mistura de ingredientes incompatíveis. Não parece comida... mas tecnicamente é.', '★', 'Cozinha', NULL, 5, TRUE);



INSERT INTO ilha
	(nome, visitada)
VALUES
	('Ilha de Borabóia', FALSE), -- → ilh001
	('Cidade de Lurien', FALSE), -- → ilh002
	('Ilha Glacial de Frimora', FALSE), -- → ilh003
	('Cactuaraquara', FALSE), -- → ilh004
	('Nublária', FALSE), -- → ilh005
	('Quartel Naval D-57', FALSE); -- → ilh006



INSERT INTO conexao_entre_ilhas
    (identificador_ilha_a, identificador_ilha_b, bloqueada)
VALUES
    ('ilh001', 'ilh002', TRUE),
    ('ilh001', 'ilh004', TRUE),
    ('ilh002', 'ilh003', TRUE),
    ('ilh002', 'ilh006', TRUE),
    ('ilh003', 'ilh004', TRUE),
    ('ilh003', 'ilh005', TRUE),
    ('ilh005', 'ilh006', TRUE);



INSERT INTO area
	(identificador_ilha, nome, tipo_area, chave_imagem_fundo, chave_imagem_frente, visitada)
VALUES
	('ilh001', 'Pastos do Sol Dourado', 'Área de combate', 'cenario_boraboia_pastos', 'cenario_boraboia_pastos_camada_superior', FALSE), -- → are001
	('ilh001', 'Vilarejo de Borabóia', 'Vila', 'cenario_boraboia_vila', null, FALSE), -- → are002
	('ilh001', 'Vale Verdejante', 'Porto', 'cenario_boraboia_vale', null, FALSE), -- → are003
	('ilh001', 'Loja de Borabóia', 'Loja', 'loja_interior', null, FALSE), -- → are004
	('ilh001', 'Casa', 'Vila', 'cenario_boraboia_casa', null, FALSE), -- → are005
	('ilh001', 'Sótão', 'Vila', 'cenario_boraboia_sotao', null, FALSE), -- → are006
	('ilh002', 'Porto de Lurien', 'Porto', 'cenario_lurien_porto', 'cenario_lurien_porto_camada_superior', FALSE), -- → are007
	('ilh002', 'Centro', 'Área neutra', 'cenario_lurien_centro', null, FALSE), -- → are008
	('ilh002', 'Praça de execução', 'Área de combate', 'cenario_lurien_praca', null, FALSE), -- → are009
	('ilh002', 'Beco', 'Área neutra', 'cenario_lurien_beco', null, FALSE), -- → are010
	('ilh002', 'Esconderijo', 'Área neutra', 'cenario_lurien_esconderijo', null, FALSE), -- → are011
	('ilh002', 'Prisão', 'Área neutra', 'cenario_lurien_prisao', null, FALSE), -- → are012
	('ilh003', 'Porto de Frimora', 'Área neutra', 'cenario_frimora_porto', null, FALSE), -- → are013
	('ilh003', 'Vila de Frimora', 'Vila', 'cenario_frimora_vila', null, FALSE), -- → are014
	('ilh003', 'Montanha da Cabra Congelada', 'Área de combate', 'cenario_frimora_montanha', null, FALSE), -- → are015
	('ilh003', 'Cozinha da Vovó Yuba', 'Loja', 'cozinha_interior', null, FALSE), -- → are016
	('ilh004', 'Duna Braba', 'Porto', 'cenario_cactuaraquara_duna', null, FALSE), -- → are017
	('ilh004', 'Cidadela de Cactuaraquara', 'Vila', 'cenario_cactuaraquara_cidadela', null, FALSE), -- → are018
	('ilh004', 'Oásis de Ramtak', 'Área de combate', 'cenario_cactuaraquara_oasis', null, FALSE), -- → are019
	('ilh004', 'Loja de Cactuaraquara', 'Loja', 'loja_interior', null, FALSE), -- → are020
	('ilh005', 'Penumbra dos Ossudos', 'Porto', 'cenario_nublaria_penumbra', null, FALSE), -- → are021
	('ilh005', 'Acampamento de Nublária', 'Vila', 'cenario_nublaria_acampamento', null, FALSE), -- → are022
	('ilh005', 'Floresta', 'Área de combate', 'cenario_nublaria_floresta', null, FALSE), -- → are023
	('ilh005', 'Loja de Nublária', 'Loja', 'loja_interior', null, FALSE), -- → are024
    ('ilh005', 'Yomotsu Hirasaka', 'Yomotsu Hirasaka', null, null, FALSE), -- → are025
	('ilh006', 'Porto da Égide', 'Porto', 'cenario_quartel_porto', null, FALSE), -- → are026
	('ilh006', 'Interior', 'Área de combate', 'cenario_quartel_interior', null, FALSE), -- → are027
	('ilh006', 'Escritório do Vice-Almirante', 'Área neutra', 'cenario_quartel_escritorio', null, FALSE), -- → are028
	('ilh006', 'Loja da Marinha', 'Loja', 'loja_interior', null, FALSE), -- → are029
	('ilh006', 'Cozinha do Capitão', 'Loja', 'cozinha_interior', null, FALSE); -- → are030



INSERT INTO conexao_entre_areas
    (identificador_area_a, identificador_area_b)
VALUES
    ('are001', 'are002'),
    ('are002', 'are003'),
    ('are002', 'are004'),
    ('are002', 'are005'),
    ('are005', 'are006'),
    ('are007', 'are008'),
    ('are008', 'are009'),
    ('are008', 'are010'),
    ('are009', 'are012'),
    ('are010', 'are011'),
    ('are013', 'are014'),
    ('are014', 'are015'),
    ('are014', 'are016'),
    ('are017', 'are018'),
    ('are018', 'are019'),
    ('are018', 'are020'),
    ('are021', 'are022'),
    ('are022', 'are023'),
    ('are022', 'are024'),
    ('are026', 'are027'),
    ('are027', 'are028'),
    ('are027', 'are029'),
    ('are027', 'are030');



-- Insere eventos de embarcar
/*INSERT INTO evento
    (identificador_conexao_ilha_a, identificador_conexao_ilha_b, tipo_evento, ponto_geracao_x,
    ponto_geracao_y, orientacao)
VALUES
    ('ilh001', 'ilh002', 'embarcar', 2470, 265, 'esquerda'),
    ('ilh001', 'ilh002', 'embarcar', 4160, 280, 'esquerda'),
    ('ilh002', 'ilh003', 'embarcar', 100, 415, 'direita'),
    ('ilh002', 'ilh003', 'embarcar', 2470, 265, 'esquerda');*/



-- Insere eventos de mudar_area
INSERT INTO evento
    (identificador_area_origem, identificador_area_destino, tipo_evento, ponto_geracao_x,
    ponto_geracao_y, orientacao)
VALUES
    ('are001', 'are002', 'mudar_area', 100, 370, 'direita'),
    ('are001', 'are002', 'mudar_area', 4373, 174, 'esquerda'),
    ('are002', 'are004', 'mudar_area', 100, 275, 'direita'),
    ('are002', 'are004', 'mudar_area', 1716, 300, 'esquerda'),
    ('are002', 'are003', 'mudar_area', 50, 190, 'direita'),
    ('are002', 'are003', 'mudar_area', 3361, 370, 'esquerda'),
    ('are007', 'are008', 'mudar_area', 100, 415, 'direita'),
    ('are007', 'are008', 'mudar_area', 680, 175, 'esquerda'),
    ('are008', 'are009', 'mudar_area', 100, 415, 'direita'),
    ('are008', 'are009', 'mudar_area', 1570, 460, 'esquerda');



INSERT INTO area_interativa
    (identificador_area, identificador_evento, x, y, largura, altura)
VALUES
    ('are001', 'eve001', 4473, 187, 30, 180),
    ('are002', 'eve002', 0, 360, 50, 150),
    ('are002', 'eve003', 1716, 300, 200, 40),
    ('are004', 'eve004', 0, 300, 50, 270),
    ('are002', 'eve005', 3490, 360, 50, 150),
    ('are003', 'eve006', 0, 200, 50, 150),
    --('are003', 'eve001', 4205, 313, 50, 158),
    ('are007', 'eve007', 610, 185, 250, 20),
    --('are007', 'eve002', 2472, 375, 93, 67),
    ('are008', 'eve008', 0, 480, 50, 150),
    ('are008', 'eve009', 1656, 484, 50, 150),
    ('are009', 'eve010', 0, 500, 50, 85);



INSERT INTO caminho
    (identificador_area, tipo_terreno, x, y, largura, altura)
VALUES
    ('are001', 'arena', 3329, 0, 1144, 600),
    ('are001', 'normal', 4473, 197, 36, 180),
    ('are001', 'normal', 826, 216, 2503, 154),
    ('are001', 'normal', 826, 370, 150, 230),
    ('are001', 'normal', 339, 438, 487, 162),
    ('are002', 'normal', 0, 445, 3540, 155),
    ('are002', 'normal', 1728, 412, 174, 33),
    ('are003', 'normal', 0, 236, 1360, 156),
    ('are003', 'arena', 1360, 33, 1226, 567),
    ('are003', 'normal', 2586, 230, 827, 145),
    ('are003', 'normal', 3413, 230, 481, 370),
    ('are003', 'normal', 3894, 313, 361, 158),
    ('are007', 'normal', 111, 309, 2589, 107),
    ('are007', 'normal', 580, 270, 290, 39),
    ('are008', 'normal', 0, 498, 1682, 102),
    ('are008', 'normal', 1539, 403, 143, 95),
    ('are009', 'normal', 0, 483, 764, 117),
    ('are009', 'arena', 764, 203, 1036, 397),
    ('are014', 'normal', 0, 407, 3540, 193),
    ('are014', 'neve', 0, 407, 3540, 74),
    ('are014', 'neve', 0, 571, 3540, 29);



INSERT INTO habitante
    (identificador_area, nome, descricao, tipo_habitante, coordenada_x, coordenada_y)
VALUES
    ('are001', 'Aldeão', 'Habitante da Ilha de Borabóia', 'rct', 0, 0),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 290, 300),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 615, 330),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 1650, 340),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 2775, 345),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 2870, 345),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 1000, 450),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 915, 323),
    ('are007', 'Cidadão', 'Costuma vender frutas no porto da Cidade de Lurien', 'rct', 0, 0),
    ('are012', 'Revolucionário', 'Oficial do exército revolucionário em missão na Cidade de Lurien', 'rct', 0, 0),
    ('are014', 'Chefe da vila', 'Chefe da vila da Ilha Glacial de Frimora', 'rct', 0, 0),
    ('are019', 'Chefe do vilarejo', 'Chefe do vilarejo de Cactuaraquara', 'rct', 0, 0),
    ('are027', 'Marinheiro', 'Marinheiro de baixo escalão', 'rct', 0, 0);



INSERT INTO jogador
    (identificador_area, nome, descricao, coordenada_x, coordenada_y,
    energia, vida, nivel, sorte, vida_atual, experiencia_atual)
VALUES
    ('are001', 'Silvie', 'Cheios de sonhos, coragem e um apetite por aventura (e por comida também), eles partem rumo ao desconhecido com um sorriso no rosto e o vento nas costas. Nada como enfrentar piratas, tempestades ou um prato estranho com garra e garfo na mão!',
    1950, 140, 5, 10, 0, 1, 10, 0)



INSERT INTO lacaio
    (nome, descricao, vida, nivel, experiencia)
VALUES
    ('Corvo',	'Um bico afiado e uma risada sarcástica. Costuma roubar frutas e orgulho.', 5, 3, 10), -- lac001
    ('Lobo',	'Uiva alto, morde forte e adora assustar viajantes desavisados.', 7, 7, 10), -- lac002
    ('Brutamontes',	'Grande, mal-humorado e com um gosto inusitado por doces.', 12, 12, 15), -- lac003
    ('Marinheiro Corrupto',	'Usa o uniforme da Marinha, mas segue as ordens do bolso.', 17, 17, 17), -- lac004
    ('Pirata Congelado',	'Foi soterrado pela neve... e agora está de volta para esfriar os ânimos.', 22, 22, 22), -- lac005
    ('Alma Soterrada',	'Um espírito inquieto com voz gelada e olhos que brilham no escuro.', 27, 27, 27), -- lac006
    ('Pirata do Deserto',	'Armado com espadas enferrujadas e piadas secas como o clima.', 32, 32, 32), -- lac007
    ('Pirata Iludido',	'Perdeu o rumo e parte da sanidade nas miragens. Ainda acha que está no mar.', 37, 37, 37), -- lac008
    ('Morcego',	'Só aparece no escuro. Detesta luz e adora cabelo desgrenhado.', 30, 42, 42), -- lac009
    ('Aranha',	'Anda silenciosa e deixa rastros de teia e calafrios por onde passa.', 35, 47, 47), -- lac010
    ('Marinheiro',	'Cansado, mal pago, mas ainda tenta manter a postura.', 52, 52, 52), -- lac011
    ('Oficial da Marinha',	'Sabe gritar "atenção!" melhor do que lutar, mas impõe respeito.', 57, 57, 57); -- lac012



INSERT INTO instancia_lacaio
    (identificador_lacaio, identificador_area, coordenada_x, coordenada_y, vida_atual)
VALUES
    ('lac001', 'are001', 3430, 55, 5),
    ('lac001', 'are001', 4273, 412, 5),
    ('lac001', 'are001', 3935, 208, 5),
    ('lac001', 'are001', 3600, 427, 5),
    ('lac002', 'are002', 1500, 125, 7),
    ('lac002', 'are002', 1900, 400, 7),
    ('lac002', 'are002', 2360, 210, 7);



INSERT INTO chefe
    (identificador_area, nome, descricao, coordenada_x, coordenada_y, vida, nivel, experiencia)
VALUES
    ('are001', 'Javali',	'Um tanque com presas. Corre como se tivesse dívida com o vento.', 0, 0, 15, 10, 20),
    ('are009', 'Capitão Renegado',	'Exibido, barulhento e com um corte de cabelo que grita "autoridade duvidosa".', 0, 0, 25, 20, 30),
    ('are015', 'Imediato Espectral',	'Leal até depois da morte. Ainda segue ordens do velho capitão pirata.', 0, 0, 35, 30, 40),
    ('are019', 'Capitão das Areias',	'Tático, traiçoeiro e com um bigode que desafia a gravidade.', 0, 0, 45, 40, 50),
    ('are023', 'Aranha Gigante',	'Gosta de se pendurar no teto e pregar sustos. Tem um ego do tamanho do abdômen.', 0, 0, 60, 50, 60),
    ('are026', 'Vice-Almirante Caelum Drayke',	'Um estrategista implacável... quando sua segunda personalidade não atrapalha.',0, 0, 120, 60, 70);



INSERT INTO missao
    (identificador_jogador, identificador_area, identificador_recrutador, descricao, nome)
VALUES
    ('jog001', 'are001', 'rct001', 'Derrotar o animal selvagem que atacou o protagonista no caminho para a vila.', 'Animal Selvagem'),
    ('jog001', 'are001', 'rct001', 'Enfrentar a fera que esta atacando camponeses e destruindo plantacoes perto da vila.', 'A Fera da Vila'),
    ('jog001', 'are007', 'rct002', 'Salvar o velho vendedor de frutas sendo agredido no porto da cidade.', 'Vendedor Agressao'),
    ('jog001', 'are012', 'rct003', 'Invadir os registros da prisao para libertar inocentes e buscar pistas sobre a irma do protagonista.', 'Infiltracao Prisao'),
    ('jog001', 'are009', null, 'Lutar e derrotar o comandante da Marinha na cidade.', 'Comandante da Marinha'),
    ('jog001', 'are013', null, 'Lutar contra lobos no caminho para o vilarejo do norte.', 'Ataque de Lobos'),
    ('jog001', 'are014', 'rct001', 'Defender o vilarejo do norte de um ataque de piratas.', 'Defesa do Vilarejo'),
    ('jog001', 'are017', null, 'Lutar contra o verme de areia que destruiu o barco no deserto.', 'Verme da Areia'),
    ('jog001', 'are019', 'rct001', 'Destruir suprimentos e usar ilusoes para diminuir o numero de piratas no deserto.', 'Estrategia do Deserto'),
    ('jog001', 'are019', 'rct001', 'Lutar e derrotar o lider dos piratas no deserto.', 'Lider Pirata do Deserto'),
    ('jog001', 'are014', 'rct001', 'Passar por treinamento e coletar materiais para aprender tecnica secreta.', 'Treinamento Secreto'),
    ('jog001', 'are026', 'rct001', 'Realizar favores para os marinheiros enquanto espera o marinheiro nobre.', 'Favores na Fortaleza'),
    ('jog001', 'are025', null, 'Derrotar uma besta marinha no caminho para a fortaleza.', 'Besta Marinha'),
    ('jog001', 'are025', null, 'Lutar contra o marinheiro nobre em sua forma hibrida.', 'Marinheiro Nobre - Hibrido'),
    ('jog001', 'are025', null, 'Luta final contra o marinheiro nobre em sua forma completa.', 'Marinheiro Nobre - Final');

