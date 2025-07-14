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
    ('Ataque', 1),
    ('Ataque', 2),
    ('Ataque', 3),
    ('Ataque', 4),
    ('Ataque', 5),
    ('Ataque', 6),
    ('Ataque', 7),
    ('Ataque', 8),
    ('Ataque', 9),
    ('Ataque', 10),
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
    ('Eletrificado', NULL),
    ('Congelado', NULL),   
    ('Molhado', NULL),     
    ('Envenenado', NULL),  
    ('Sangramento', NULL), 
    ('Queimadura', NULL),  
    ('Tontura', NULL),     
    ('Cegueira', NULL),    
    ('Purificação', NULL); 



-- Habilidades do Personagem
INSERT INTO habilidade
    (identificador_efeito, nome, descricao, tipo_de_ataque, tipo_de_alvo, dano, custo)
VALUES
    (NULL, 'Soco Direto', 'Um golpe rápido e certeiro. Simples, mas eficiente como uma boa bronca.', 'soco', 'alvo_terrestre', 8, 0), -- Dano_final = dano_base * (1 + (nivel_jogador / escala)) * multiplicador_area * multiplicador_raridade
    ('efe084', 'Martelo de Carne', 'Socos pesados e ritmados como um churrasqueiro raivoso. Aplica Tontura.', 'soco', 'terrestre', 8, 4),
    (NULL, 'Soco Giratório', 'Um giro rápido com soco final. Às vezes acerta dois alvos lado a lado.', 'soco', 'alvo_terrestre', 8, 0),
    ('efe084', 'Trovão de Punhos', 'Uma sequência de socos trovejantes que sacodem o chão. Pode causar Tontura em todos.', 'soco', 'terrestre', 8, 4),
    ('efe084', 'Onda de Reverb', 'Uma onda sonora concentrada vibra direto no corpo do inimigo, bagunçando os sentidos e até o penteado. Quem nunca tomou um choque de eco?', 'fruta', 'alvo_terrestre', 11, 6),
    ('efe079', 'Tempestade de Ecos', 'Libera todos os ecos gravados de uma só vez — risos, gritos, passos, trovões, sinos e até um “quem deixou isso cair?”. O resultado é um caos auditivo que confunde e machuca.', 'fruta', 'area', 11, 10),
    (NULL, 'Golpe Quadrado', 'Um corte direto, como manda o manual.', 'espada', 'fila', 8, 0),
    (NULL, 'Golpe de Ordem', 'Um ataque com impacto moral.', 'espada', 'fila', 9, 3),
    (NULL, 'Corte Rasteiro', 'Um corte baixo que levanta poeira nos olhos do inimigo.', 'espada', 'fila', 9, 0),
    ('efe082', 'Tempestade de Grãos', 'Uma rajada de cortes rápidos e secos. Aplica Sangramento em até dois inimigos.', 'espada', 'terrestre', 9, 4),
    (NULL, 'Estocada Espinhosa', 'Um ataque direto com o risco de lascar... o inimigo.', 'espada', 'fila', 9, 0),
    ('efe081', 'Maré Ácida', 'Um corte que espalha fragmentos venenosos. Aplica Envenenado em todos os inimigos.', 'espada', 'terrestre', 9, 5),
    (NULL, 'Corte Ilusório', 'Você ataca... ou acha que atacou? O inimigo fica confuso.', 'espada', 'fila', 9, 0),
    ('efe085', 'Passo entre Dimensões', 'Some e surge atrás do inimigo com um golpe crítico. Aplica Cegueira.', 'espada', 'fila', 10, 6),
    (NULL, 'Corte Ascendente', 'Um golpe leve que levanta o inimigo no ar.', 'espada', 'terrestre', 9, 0),
    ('efe082', 'Dança do Vento', 'Vários golpes tão rápidos quanto o vento. Aplica Sangramento e pode atacar duas vezes.', 'espada', 'terrestre', 10, 6),
    (NULL, 'Corte Silencioso', 'Um corte que mal faz barulho, mas dói do mesmo jeito.', 'espada', 'fila', 9, 0),
    ('efe079', 'Fio da Névoa', 'Um ataque rápido e gelado que aplica Congelado. Ideal para travar inimigos velozes.', 'espada', 'terrestre', 9, 8),
    (NULL, 'Corte Preciso', 'Um golpe tão limpo que dá até vontade de servir com arroz.', 'espada', 'fila', 10, 0),
    ('efe083', 'Fatia de Dragão', 'Um corte flamejante que torra o ar ao redor. Aplica Queimadura em todos os inimigos.', 'espada', 'terrestre', 12, 9),
    (NULL, 'Corte Temperado', 'O golpe tem gosto de lar... e um leve ardor de pimenta.', 'espada', 'fila', 10, 0),
    ('efe083', 'Receita Final', 'Um corte carregado de amor (e fúria). Aplica Queimadura e aumenta o ataque por 1 turno.', 'espada', 'fila', 11, 8),
    (NULL, 'Golpe Bêbado', 'Um ataque errático com chance de acerto crítico… ou escorregar.', 'espada', 'fila', 11, 0),
    ('efe084', 'Brado do Samurai Fantasma', 'Um golpe sombrio e instável. Aplica Tontura no inimigo e pode reduzir o ataque dele.', 'espada', 'terrestre', 11, 6),
    (NULL, 'Pedra Voadora', 'Um disparo simples que pode surpreender pelo barulho (não pela força).', 'estilingue', 'alvo_livre', 7, 0),
    (NULL, 'Pancada Improvisada', 'Lança dois projéteis de uma vez. Chance de causar dano duplo.', 'estilingue', 'alvo_livre', 8, 3),
    (NULL, 'Doce no Olho', 'Dispara uma bala de açúcar direto no orgulho do alvo.', 'estilingue', 'alvo_livre', 6, 0),
    ('efe084', 'Nuvem de Confeiteiro', 'Estoura uma explosão de confeitos. Aplica Tontura a todos os inimigos.', 'estilingue', 'area', 7, 2),
    (NULL, 'Flecha Dramática', 'Dispara com estilo, aumentando sua autoestima.', 'arco', 'alvo_livre', 9, 0),
    ('efe085', 'Rajada Ofuscante', 'Disparo que reflete a luz. Aplica Cegueira por 2 turnos.', 'arco', 'alvo_livre', 9, 5),
    (NULL, 'Coco Direto', 'Dispara um coco com a delicadeza de um canhão de praia.', 'estilingue', 'alvo_livre', 10, 0),
    ('efe084', 'Tempestade Tropical', 'Lança uma sequência de cocos. Aplica Tontura e dano leve em 2 alvos.', 'estilingue', 'area', 10, 6),
    (NULL, 'Flecha Reciclada', 'Atira farpas com aquele sentimento de “quebra galho”.', 'arco', 'alvo_livre', 9, 0),
    (NULL, 'Assento Desmontável', 'Disparo pesado. Chance de Sangramento.', 'arco', 'alvo_livre', 11, 7),
    (NULL, 'Duplo Estalo', 'Atira duas vezes no mesmo alvo. Mais precisão, menos paciência.', 'estilingue', 'alvo_livre', 9, 0),
    ('efe082', 'Golpe Veloz', 'Dispara três vezes em sequência. Aplica Sangramento no último golpe.', 'estilingue', 'alvo_livre', 10, 5),
    (NULL, 'Flecha Natural', 'Disparo com o som suave de folhas ao vento.', 'arco', 'alvo_livre', 10, 0),
    ('efe083', 'Chama da Selva', 'Flecha flamejante. Aplica Queimadura e reduz defesa por 1 turno.', 'arco', 'area', 10, 8),
    (NULL, 'Flecha Silenciosa', 'Disparo limpo que quase não se ouve.', 'arco', 'alvo_livre', 11, 0),
    ('efe081', 'Veneno Dourado', 'Flecha envenenada. Aplica Envenenado e reduz ataque.', 'arco', 'alvo_livre', 10, 6),
    (NULL, 'Canhão de Bolinha', 'Um disparo pesado como o nome sugere.', 'estilingue', 'alvo_livre', 11, 0),
    ('efe083', 'Bombardeio Pirata', 'Dispara uma salva em todos os inimigos. Aplica Queimadura.', 'estilingue', 'area', 11, 9);



-- Habilidades de Inimigos
INSERT INTO habilidade
    (identificador_efeito, nome, descricao, tipo_de_ataque, tipo_de_alvo, dano)
VALUES
    ('efe085', 'Investida Penosa', 'O corvo mergulha com um grito estridente, mirando os olhos. Quem precisa de precisão quando se tem drama?', 'soco', 'alvo_livre', 1),
    ('efe082', 'Mordida Selvagem', 'Uma mordida rápida e feroz. Ele rosna depois, só pra garantir que você não esqueça.', 'soco', 'alvo_terrestre', 2),
    ('efe084', 'Carga Desgovernada', 'Baixa a cabeça, corre, atropela. Você não está preparado. Ninguém está preparado.', 'soco', 'terrestre', 4),
    ('efe084', 'Soco Açucarado', 'Um murro tão forte quanto seu vício em balas. Quem diria que açúcar deixava alguém assim?', 'soco', 'alvo_terrestre', 4),
    (NULL, 'Suborno de Honra', 'Ele tenta “convencer” você a baixar a guarda. Com um soco. E uma proposta indecente.', 'soco', 'alvo_terrestre', 4),
    ('efe084', 'Discurso Furioso', 'Ele grita tanto — e tão mal — que o chão treme. E sua paciência também. Todo mundo sai atordoado.', 'soco', 'area', 4),
    ('efe079', 'Corte Gélido', 'Um golpe vindo do além... e do frio. Faz até os ossos doerem — literalmente.', 'espada', 'alvo_terrestre', 4),
    ('efe084', 'Lamento Espectral', 'Um grito abafado ecoa debaixo da neve, mexendo com a cabeça de quem ainda está vivo.', 'soco', 'area', 4),
    (NULL, 'Chicote da Disciplina Fantasma', 'Ele ainda tenta manter a ordem no navio… mesmo sem navio. O golpe consome sua energia e sua moral.', 'soco', 'alvo_terrestre', 4),
    ('efe082', 'Corte Ressecado', 'Um corte seco e direto, como o vento do deserto. Não dói na hora, mas logo arde como areia nos olhos.', 'espada', 'alvo_terrestre', 4),
    ('efe085', 'Miragem Veloz', 'Ele gira, tropeça e ataca ilusões. O problema? Às vezes acerta você no processo — e ainda te deixa tonto de confusão.', 'soco', 'area', 4),
    ('efe081', 'Estratégia de Escorpião', 'Ele ataca como quem traça um plano: rápido, certeiro e com veneno suficiente pra fazer um camelo desmaiar.', 'estilingue', 'alvo_terrestre', 4),
    (NULL, 'Chilreio Atordoante', 'Um grito agudo que reverbera dentro do crânio. Você esquece por um momento quem é o inimigo… ou quem é você.', 'soco', 'alvo_livre', 4),
    ('efe081', 'Picada Venenosa', 'Um ataque rápido com as presas. A picada mal se sente — mas a dormência e a baba verde depois, sim.', 'soco', 'alvo_terrestre', 4),
    ('efe079', 'Teia Sinistra', 'Lança uma rede de teias espectrais que grudam em tudo. Não é frio... mas te faz travar como se fosse.', 'soco', 'area', 4),
    (NULL, 'Investida Quadrada', 'Um avanço com baioneta ou espada curta. Pouco inspirador, mas certinho como o manual.', 'espada', 'alvo_terrestre', 4),
    ('efe084', 'Comando Impositivo', 'Um grito autoritário que ecoa pelo campo. Não machuca, mas deixa todos meio zonzos (e irritados).', 'soco', 'area', 4),
    ('efe085', 'Golpe da Maré Controlada', 'Um golpe técnico e preciso, mirando nos olhos e na moral do oponente. A disciplina é uma arma.', 'soco', 'alvo_terrestre', 4),
    ('efe082', 'Rajada Vento-Escamas', 'As asas batem com força, espalhando escamas cortantes e um vendaval que embaralha sentidos.', 'fruta', 'area', 5),
    ('efe080', 'Dilúvio Celeste', 'Do alto, o dragão invoca uma chuva mística e destrutiva. O chão treme, a visão embaça, e o terror paira.', 'fruta', 'area', 6),
    ('efe078', 'Trovão Ancestral', 'As nuvens rugem, e do céu o dragão invoca relâmpagos que atingem inimigos e solo. O zumbido permanece mesmo após o silêncio.', 'fruta', 'area', 6),
    ('efe083', 'Inferno Celeste', 'Do alto, o dragão cospe uma rajada flamejante que gira como um furacão. O calor dobra o ar e torce a razão. Só os mais firmes não caem.', 'fruta', 'area', 6);



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



INSERT INTO efeito_acessorio
    (identificador_acessorio, identificador_efeito)
VALUES
    ('ace001', 'efe052'),
    ('ace002', 'efe055'),
    ('ace003', 'efe065'),
    ('ace004', 'efe067'),
    ('ace005', 'efe039'),
    ('ace006', 'efe044'),
    ('ace007', 'efe073'),
    ('ace008', 'efe074');



INSERT INTO arma
    (nome, descricao, raridade, tipo_arma, local_encontrado,
     preco_de_compra)
VALUES
    ('Espadinha do Marinheiro', 'Básica, reta e sem sal — igual à comida do quartel.', '★', 'esp', 'Loja de Espadas', 50),    
    ('Corte de Areia', 'Uma lâmina fina, feita para deslizar no calor escaldante do deserto. Melhor usar antes que enferruje.', '★', 'esp', 'Loja de Espadas', 55),
    ('Gume de Coral', 'Forjada com pedaços de coral duro. Linda, mas cuidado com lascas!', '★★', 'esp', 'Loja de Espadas', 80),
    ('Espada Fantasma', 'Você jura que ela está na sua mão, mas às vezes… ela desaparece.', '★★', 'esp', 'Loja de Espadas', 90),
    ('Lâmina da Brisa', 'Tão leve que quase voa sozinha. Ideal para quem gosta de parecer estiloso enquanto luta.', '★★', 'esp', 'Loja de Espadas', 105),
    ('Lâmina Sussurrante', 'Dizem que ela corta o ar tão silenciosamente que até o vento pede licença.', '★★', 'esp', 'Loja de Espadas', 110),
    ('Katana do Sushi Supremo', 'Corta peixe tão bem que o próprio mar fica com inveja. Também serve pra vilões, se estiverem quietos o suficiente.', '★★★', 'esp', 'Loja de Espadas', 140),
    ('Katana da Vovó Yuba', 'Ela usava pra cortar carne, peixe e argumentos. Respeito e corte limpo em cada golpe.', '★★★', 'esp', 'Loja de Espadas', 150),
    ('Katana do Capitão Caído', 'Roubada de um lendário capitão samurai que confundiu o oceano com arrozal. Ainda tem cheiro de saquê.', '★★★', 'esp', 'Loja de Espadas', 165),
    ('Estilingue de Iniciante', 'Feito com elástico e madeira de galho. Não subestime a força de uma boa gambiarra.', '★', 'est', 'Loja de Estilingues e Arcos', 30),
    ('Lança-Suspiro', 'Disparar projéteis doces não é eficaz, mas é surpreendentemente ofensivo ao ego inimigo.', '★', 'arc', 'Loja de Estilingues e Arcos', 45),
    ('Arco da Pose Perfeita', 'Aumenta carisma em 20% ao ser empunhado dramaticamente diante do pôr do sol.', '★', 'arc', 'Loja de Estilingues e Arcos', 50),
    ('Atira-Coco', 'Não é elegante, mas já derrubou mais de um pirata. Lançar cocos exige força… e coragem.', '★★', 'est', 'Loja de Estilingues e Arcos', 70),
    ('Arco de Pedaço de Cadeira', 'Sim, é o encosto de uma cadeira com uma corda. Sim, funciona. Vai discutir com ele?', '★★', 'arc', 'Loja de Estilingues e Arcos', 70),
    ('Estilingue do Voo Duplo', 'Se acertar o mesmo inimigo duas vezes seguidas, você ganha o direito de chamá-lo de ‘meu alvo favorito’.', '★★', 'est', 'Loja de Estilingues e Arcos', 80),
    ('Arco de Liana', 'Um arco feito com cipós flexíveis e muita criatividade. Tensão máxima, estilo selvagem.', '★★', 'arc', 'Loja de Estilingues e Arcos', 85),
    ('Arco do Oásis', 'Suave e silencioso como uma brisa no deserto. Ideal para acertar antes de ser visto.', '★★★', 'arc', 'Loja de Estilingues e Arcos', 125),
    ('Estilingue de Batalha Naval', 'Usado por um pirata que confundia navios com alvos de treino. Deu certo… até certo ponto.', '★★★', 'est', 'Loja de Estilingues e Arcos', 125);



INSERT INTO fruta
    (nome, descricao, raridade, local_encontrado)
VALUES
    ('Mimi Mimi no Mi: Fruta do Eco', 'Uma fruta rara, de cor chamativa e com um aroma meio doce, meio… enxerido. Quem a come desenvolve habilidades sonoras peculiares — perfeitas para quem adora ouvir, repetir e, claro, se meter onde não foi chamado.', '★★★', 'Missão');

INSERT INTO habilidade_arma
    (identificador_arma, identificador_habilidade)
VALUES
    ('arm001', 'hab007'),
    ('arm001', 'hab008'),
    ('arm002', 'hab009'),
    ('arm002', 'hab010'),
    ('arm003', 'hab011'),
    ('arm003', 'hab012'),
    ('arm004', 'hab013'),
    ('arm004', 'hab014'),
    ('arm005', 'hab015'),
    ('arm005', 'hab016'),
    ('arm006', 'hab017'),
    ('arm006', 'hab018'),
    ('arm007', 'hab019'),
    ('arm007', 'hab020'),
    ('arm008', 'hab021'),
    ('arm008', 'hab022'),
    ('arm009', 'hab023'),
    ('arm009', 'hab024'),
    ('arm010', 'hab025'),
    ('arm010', 'hab026'),
    ('arm011', 'hab027'),
    ('arm011', 'hab028'),
    ('arm012', 'hab029'),
    ('arm012', 'hab030'),
    ('arm013', 'hab031'),
    ('arm013', 'hab032'),
    ('arm014', 'hab033'),
    ('arm014', 'hab034'),
    ('arm015', 'hab035'),
    ('arm015', 'hab036'),
    ('arm016', 'hab037'),
    ('arm016', 'hab038'),
    ('arm017', 'hab039'),
    ('arm017', 'hab040'),
    ('arm018', 'hab041'),
    ('arm018', 'hab042');



INSERT INTO habilidade_fruta
    (identificador_fruta, identificador_habilidade)
VALUES
    ('fru001', 'hab005'),
    ('fru001', 'hab006');




INSERT INTO nao_consumivel
    (nome, descricao, raridade, local_encontrado,
     preco_de_compra, preco_de_venda, e_coletado)
VALUES
    ('Abóbora Redonduda', 'Grande, laranja e cheia de personalidade. Ótima para sopas, risos e sustos.', '★', 'Ilha de Borabóia', 15, 6, FALSE),
    ('Arroz do Planalto', 'Grãos branquinhos que dançam quando caem na panela. Base de quase tudo!', '★', 'Ilha de Borabóia', 10, 5, FALSE),
    ('Ovo dos Campos', 'Um ovo fresquinho, coletado de aves que vivem soltas pelos campos. Dá vontade de fritar, mas também pode virar algo mais sofisticado.', '★', 'Ilha de Borabóia', 10, 5, FALSE),
    ('Carne de Ave Brava', 'Um pedaço de ave com gosto de aventura. Cozinhe bem ou corra risco de bicadas!', '★', 'Ilha de Borabóia', NULL, 7, FALSE),
    ('Presa de Lobo', 'Um dente afiado arrancado de um lobo valente. Não é comestível, mas é estiloso.', '★★', 'Ilha de Borabóia', NULL, 15, FALSE),
    ('Farinha Misteriosa', 'Ninguém sabe de onde veio, mas faz bolos ótimos. Melhor não perguntar.', '★', 'Cidade de Lurien', 10, 5, FALSE),
    ('ButterCream de Fuligem', 'O preferido dos confeiteiros da cidade, feito com um toque especial de cana-de-açúcar e... partículas do ar local.', '★★', 'Cidade de Lurien', NULL, 15, FALSE),
    ('Farinha Misteriosa', 'Ninguém sabe de onde veio, mas faz bolos ótimos. Melhor não perguntar.', '★', 'Cidade de Lurien', 20, 8, FALSE),
    ('Medalha de Marinheiro', 'Símbolo de honra… ou corrupção. Não serve pra comer, mas pode abrir portas.', '★★', 'Cidade de Lurien', NULL, 20, FALSE),
    ('Pérola Cantante', 'Emite um som suave quando tocada. Dizem que revive quem ouve sua melodia até o fim.', '★★', 'Ilha Glacial de Frimora', 30, 17, FALSE),
    ('Pedaço de Tecido Rasgado', 'Um trapo que já foi parte de um uniforme pirata. Cheira a nostalgia e mofo.', '★', 'Ilha Glacial de Frimora', NULL, 8, FALSE),
    ('Lamento Gelado', 'Um fragmento de tristeza congelada. Só aparece quando almas inquietas são libertadas.', '★★', 'Ilha Glacial de Frimora', NULL, 12, FALSE),
    ('Faixa de Pirata Estorricado', 'Um pano ressecado de pirata que enfrentou o sol por tempo demais. Ótimo pra rituais e costura.', '★', 'Cactuaraquara', NULL, 10, FALSE),
    ('Fragmento de Miragem', 'Um cristal etéreo que brilha e some quando você olha fixo. Nasceu da confusão de mentes perdidas.', '★★', 'Cactuaraquara', NULL, 12, FALSE),
    ('Sombra Engarrafada', 'Uma sombra viva que foi capturada. Útil em receitas que assustam até o cozinheiro.', '★★', 'Nublária', NULL, 17, TRUE),
    ('Açúcar Estranho', 'Doce, crocante e... será que isso tá brilhando? Ideal para doces perigosamente bons.', '★', 'Nublária', 5, 2, FALSE),
    ('Essência de Névoa Doce', 'Um xarope espesso que adoça e assusta. Parece açúcar, mas sussurra nomes perdidos.', '★★', 'Nublária', 10, 4, FALSE),
    ('Asa de Morcego Noturno', 'Negra como a meia-noite sem lua. Serve para receitas, poções e decoração gótica.', '★', 'Nublária', NULL, 9, FALSE),
    ('Presa Venenosa', 'Brilha com um verde nada confiável. Cuide para não furar o dedo ao manusear.', '★', 'Nublária', NULL,  7, FALSE),
    ('Peixe Saltitante', 'Ainda parece se mexer! Ideal para grelhar, cozinhar ou assustar aprendizes.', '★', 'Quartel Naval D-57', NULL, 11, TRUE),
    ('Pepino de Salmoura', 'Conservado com tanto sal que chega a arrepiar a alma. Dizem que dura uma década.', '★', 'Quartel Naval D-57', NULL, 5, TRUE),
    ('Chapéu de Marinheiro', 'Simboliza status, disciplina e... bom, é só um chapéu suado. Não comestível.', '★★', 'Quartel Naval D-57', NULL, 15, FALSE);



INSERT INTO consumivel
    (nome, descricao, raridade, local_encontrado,
     preco_de_compra, preco_de_venda, e_fabricavel, e_coletado)
VALUES
    ('Fruta do Mar Azul', 'Uma frutinha brilhante e saborosa! Recupera energia e pode causar inveja em gaivotas.', '★', 'Ilha de Borabóia', NULL, 5, FALSE, TRUE),
    ('Fruta do Mar Vermelha', 'Mais doce e vibrante que sua prima azul. Dizem que aquece até o coração gelado.', '★', 'Ilha de Borabóia', NULL, 5, FALSE, TRUE),
    ('Folha de Hortelã', 'Refrescante, cheirosa e ótima em chás ou nas mãos de piratas resfriados.', '★', 'Ilha de Borabóia', NULL, 5, FALSE, TRUE),
    ('Maçã Lustrosa', 'Brilha tanto que você se vê nela. Tão docinha quanto promessas de marinheiro.', '★', 'Cidade de Lurien', NULL, 7, FALSE, TRUE),
    ('Repolho Redondo', 'Enrola mais que muito pirata mentiroso. Cru ou cozido, sempre útil.', '★', 'Cidade de Lurien',  NULL, 5, FALSE, TRUE),
    ('Alga Fresca', 'Parece nojenta, mas dizem que é cheia de nutrientes. Piratas fitness adoram.', '★', 'Cidade de Lurien', NULL, 6, FALSE, TRUE),
    ('Chá Enlatado', 'Vendido em latas esquisitas. Tem gosto de “quase chá”, mas funciona.', '★', 'Cidade de Lurien', 15, 6, FALSE, FALSE),
    ('Doce Amassado', 'Parece que foi esmagado por um punho gigante. Ainda doce, com gosto de luta.', '★', 'Cidade de Lurien', NULL, 2, FALSE, FALSE),
    ('Noz Crocante', 'Pequena, dura e barulhenta. Ideal para mordidas rápidas ou espantar pinguins curiosos.', '★', 'Ilha Glacial de Frimora', NULL, 2, FALSE, TRUE),
    ('Ervas Aromáticas', 'Um cheirinho que aquece a alma. Ótimas para chás, sopas ou magias de vovó.', '★', 'Ilha Glacial de Frimora', NULL, 3, FALSE, TRUE),
    ('Neve Mágica', 'Parece gelo raspado, mas derrete em cura. Tente não comer tudo de uma vez.', '★★', 'Ilha Glacial de Frimora', NULL, 12, FALSE, TRUE),
    ('Leite de Cabra Alpina', 'Quentinho, cremoso e nutritivo. Perfeito para combater o frio e o mau humor.', '★', 'Ilha Glacial de Frimora', 10, 6, FALSE, FALSE),
    ('Chocolate Amargo', 'Amargo como a vida no gelo. Derrete o cansaço e o coração congelado.', '★', 'Ilha Glacial de Frimora', 15, 8, FALSE, FALSE),
    ('Fruta Cítrica do Oeste', 'Azeda, suculenta e cheia de energia solar. Ótima pra acordar até múmia adormecida.', '★', 'Cactuaraquara', NULL, 4, FALSE, TRUE),
    ('Côco do Oásis', 'Pesado, difícil de abrir, mas vale cada gole. Ideal pra hidratar e bater na cabeça dos outros.', '★', 'Cactuaraquara', NULL, 7, FALSE, TRUE),
    ('Areia Mineral', 'Tem gosto de... areia. Mas misture bem e talvez vire um tônico impressionante.', '★★', 'Cactuaraquara', NULL, 10, FALSE, TRUE),
    ('Carne do Deserto', 'Picante o suficiente pra te fazer cuspir fogo. +1 em coragem depois de comer.', '★★', 'Cactuaraquara',  20, 8, FALSE, FALSE),
    ('Geleia de Cacto Doce', 'Um docinho raro feito do néctar de um cacto bem zangado. Cuidadosamente colhida!', '★★', 'Cactuaraquara', 11, 6, FALSE, FALSE),
    ('Suco Refrescante Solar', 'Tão gelado que parece mágica. Refresca mais que mergulho em fonte sagrada.', '★', 'Cactuaraquara', 7, 4, FALSE, FALSE),
    ('Cogumelo Risonho', 'Tem uma carinha feliz. Ninguém sabe por quê. Comer pode causar risos... ou arrependimentos.', '★', 'Nublária', NULL, 9, FALSE, TRUE),
    ('Fruta Fluorescente', 'Brilha no escuro! Alguns dizem que tem alma própria.', '★', 'Nublária', NULL, 7, FALSE, TRUE),
    ('Doce Fantasmal', 'Derrete na língua e deixa um leve arrepio na espinha. Doces espíritos aprovariam.', '★', 'Nublária', 13, 5, FALSE, FALSE),
    ('Ração de Soldado', 'Embalada à vácuo e sem gosto. Mas dá energia e fortalece o espírito patriótico.', '★★', 'Quartel Naval D-57', NULL, 10, FALSE, TRUE),
    ('Biscoito de Gengibre', 'Na ala dos oficiais, um confeiteiro reformado da Marinha mantém a tradição de assar biscoitos para “manter a moral da tropa”. Só não conte pros recrutas — é só pros superiores.', '★★', 'Quartel Naval D-57', 12, 7, FALSE, FALSE),
    ('Café Turbinado', 'Tão forte que acorda até os mortos e os marinheiros de plantão.', '★', 'Quartel Naval D-57',     8, 3, FALSE, FALSE),
    ('Carne de Rei dos Mares', 'Gigantesca, rara e cara. Cheia de proteína e orgulho militar.', '★★★', 'Quartel Naval D-57', 40, 19, FALSE, FALSE),
    ('Rosquinha Mordida', 'Quem mordeu e largou? Ainda tá boa. Restaura pouco, mas serve como prova de negligência.', '★', 'Quartel Naval D-57', NULL, 3, FALSE, FALSE),
    ('Sushi Enrolado', 'Enrolado com carinho e peixe saltitante! Um lanche leve, mas cheio de sabor.', '★★', 'Cozinha', NULL, 15, TRUE, FALSE),
    ('Chá de Algas', 'Um gole desse chá marinho e você sente até as ondas te abraçando por dentro.', '★', 'Cozinha',  NULL, 10, TRUE, FALSE),
    ('Pastel de Fruta do Diabo', 'Ardido e adocicado, um quitute perigoso para os mais ousados.', '★★', 'Cozinha', NULL, 18, TRUE, FALSE),
    ('Caldo da Vovó Yuba', 'Uma sopa tão boa que parece que te dá um abraço. Feita com amor... e pimenta!', '★★', 'Cozinha', NULL, 22, TRUE, FALSE),
    ('Tônico de Areia', 'Tem gosto de areia? Sim. Funciona? Mais do que você imagina!', '★★', 'Cozinha', NULL, 16, TRUE, FALSE),
    ('Chá Gelado de Neve', 'Refrescante até congelar os pensamentos. A escolha perfeita pra esfriar os ânimos.', '★★', 'Cozinha', NULL, 15, TRUE, FALSE),
    ('Receita Secreta do Capitão', 'Uma mistura poderosa e misteriosa, só os verdadeiros líderes se atrevem a provar.', '★★★', 'Cozinha', NULL, 27, TRUE, FALSE),
    ('Carne Grelhada', 'Crocante por fora, suculenta por dentro. Perfeita para qualquer fogueira.', '★★', 'Cozinha', NULL, 18, TRUE, FALSE),
    ('Pérola Caramelizada', 'Crocante, mágica e doce. Dizem que revive até o humor de um pirata carrancudo.', '★★', 'Cozinha', NULL, 13, TRUE, FALSE),
    ('Pérola da Lua de Inverno', 'Um doce etéreo que brilha como a luz da lua sobre a neve. Quem o come sente o universo piscando para si — e os dados da vida rolando a seu favor.', '★★★', 'Cozinha', NULL, 24, TRUE, FALSE),
    ('Pérola do Sol Escaldante', 'Forjada no calor do deserto, essa pérola brilha como o sol ao meio-dia, aquecendo o corpo e dando força para suportar o calor implacável.', '★★★', 'Cozinha', NULL, 24, TRUE, FALSE),
    ('Gelado de Algas', 'Uma sobremesa geladinha com gosto do mar e um toque de frescor sobrenatural.', '★', 'Cozinha',  NULL, 15, TRUE, FALSE),
    ('Omurice de Arroz', 'Receita tradicional dos viajantes do campo, famosa por causar nostalgia e fome ao mesmo tempo.', '★★', 'Cozinha', NULL, 15, TRUE, FALSE),
    ('Bolo do Campo', 'Um bolo simples, mas saboroso, feito com ingredientes fresquinhos do campo. Perfeito para uma pausa na aventura!', '★★', 'Cozinha', NULL, 14, TRUE, FALSE),
    ('Bombom Nebuloso', 'Um docinho que parece derreter em névoa assim que toca a língua. Feito com carinho (e um pouco de sombra).', '★★', 'Cozinha', NULL, 12, TRUE, FALSE),
    ('Arroz dos Sete Mares', 'Uma tigela robusta de arroz misturado com sabores do mar. Os marinheiros juram que dá sorte.', '★', 'Cozinha', NULL, 9, TRUE, FALSE),
    ('Doce da Ilha', 'Um doce feito com coco e calda cítrica, lembra o pôr do sol nas dunas do deserto.', '★★', 'Cozinha', NULL, 12, TRUE, FALSE),
    ('Omelete dos 4 Ventos', 'Leve e fofa, com o sabor do campo e a brisa das planícies.', '★★', 'Cozinha', NULL, 13, TRUE, FALSE),
    ('Frango Assado Estaladiço', 'Crocante por fora, macio por dentro. Tão bom que até o corvo queria roubar.', '★', 'Cozinha', NULL, 10, TRUE, FALSE),
    ('Sopa da Guarda Noturna', 'Revigorante e quentinha, ideal para noites frias e perseguições por becos.', '★', 'Cozinha', NULL, 6, TRUE, FALSE),
    ('Doce de Duna Dourada', 'Doce exótico feito com frutas do deserto. Cuidado: pode atrair camelos.', '★★', 'Cozinha', NULL, 16, TRUE, FALSE),
    ('Bife do Abismo', 'Um corte suculento direto das profundezas do mar. Tão macio que derrete na boca, mas tão forte que faz os músculos tremerem.', '★★★', 'Cozinha', NULL, 35, TRUE, FALSE),
    ('Sashimi do Fim do Mundo', 'Cru, fino e perfeitamente cortado. Dizem que só quem já viu o mar no escuro da lua nova entende seu verdadeiro sabor.', '★★★', 'Cozinha', NULL, 35, TRUE, FALSE),
    ('Torta do Marujo Feliz', 'Um clássico entre os navegadores nostálgicos. Um pedaço e você esquece do enjoo... e do resto da tripulação.', '★', 'Cozinha',  NULL, 10, TRUE, FALSE),
    ('Doce Assombrado', 'Não se sabe se o sabor é bom ou se é só a maldição agindo. Textura perfeita... demais até.', '★★', 'Cozinha', NULL, 12, TRUE, FALSE),
    ('Curry do Capitão Covarde', 'O cheiro é intenso, o sabor é duvidoso, mas nenhum pirata consegue parar de comer.', '★★', 'Cozinha', NULL, 13, TRUE, FALSE),
    ('Elixir Sombrio', 'Bebida proibida sussurrada em tavernas assombradas. Quem é que vai querer beber isso...?', '★★', 'Cozinha', NULL, 18, TRUE, FALSE),
    ('Poção do Dente Torto', 'Um gole é suficiente para se sentir... diferente. Tem certeza que isso não é veneno?', '★★', 'Cozinha', NULL, 18, TRUE, FALSE),
    ('Cookie de Chocolate', 'Crocante por fora, macia por dentro. Derrete na boca como a neve da infância.', '★', 'Cozinha', NULL, 14, TRUE, FALSE),
    ('Leite Condensado Alpino', 'Um creme docinho e suave.', '★', 'Cozinha',  NULL, 11, TRUE, FALSE),
    ('Chocolate Quente', 'Um gole e você sente como se tivesse abraçado um urso de cachecol... que acabou de sair do banho e decidiu virar seu terapeuta de plantão.', '★★', 'Cozinha',  NULL, 15, TRUE, FALSE),
    ('Doce do Silêncio Eterno', 'Um doce que ecoa sussurros antigos. Quem come diz sentir a presença dos que partiram.', '★★', 'Cozinha', NULL, 17, TRUE, FALSE),
    ('Cacto-Pop Geladinho', 'Uma explosão refrescante e pegajosa! Perfeito para os dias escaldantes no deserto.', '★★', 'Cozinha', NULL, 16, TRUE, FALSE),
    ('Esfera da Miragem', 'Parece sólida, mas será que é? Um doce ilusório que desorienta quem o encara por muito tempo.', '★★', 'Cozinha', NULL, 17, TRUE, FALSE),
    ('Pickles Pirata', 'Um prato inusitado e ousado. Os piratas juram que melhora a mira (e o hálito!).', '★', 'Cozinha', NULL, 10, TRUE, FALSE),
    ('Torta de Telhado', 'Doce crocante e levemente defumado. Dizem que foi assada nos telhados quentes da cidade durante uma greve dos padeiros.', '★★', 'Cozinha', NULL, 15, TRUE, FALSE),
    ('Doce de Fuligem Cítrica', 'Uma sobremesa brilhante com um leve toque de fumaça — parece suspeita, mas é incrivelmente viciante.', '★', 'Cozinha', NULL, 11, TRUE, FALSE),
    ('Rosquinha do Quartel Proibida', 'Criada por um marinheiro rebelde com talento para confeitaria e zero noção de higiene. Um sucesso entre os subalternos.', '★★', 'Cozinha', NULL, 16, TRUE, FALSE),
    ('Bolo da Chaminé Encantada', 'Dizem que foi feito com açúcar mágico... ou fuligem encantada. Vai saber. Pelo menos é fofo e aquece o coração.', '★★★', 'Cozinha', NULL, 18, TRUE, FALSE),
    ('Frankenprato', 'Uma aberração culinária nascida da mistura de ingredientes incompatíveis. Não parece comida... mas tecnicamente é.', '★', 'Cozinha', NULL, 5, TRUE, FALSE);



INSERT INTO efeito_consumivel
    (identificador_consumivel, identificador_efeito)
VALUES
    ('con001', 'efe023'),
    ('con002', 'efe003'),
    ('con003', 'efe022'),
    ('con003', 'efe086'),
    ('con004', 'efe003'),
    ('con004', 'efe021'),
    ('con005', 'efe022'),
    ('con006', 'efe022'),
    ('con006', 'efe036'),
    ('con007', 'efe038'),
    ('con007', 'efe078'),
    ('con008', 'efe002'),
    ('con009', 'efe003'),
    ('con010', 'efe024'),
    ('con010', 'efe086'),
    ('con011', 'efe006'),
    ('con011', 'efe079'),
    ('con012', 'efe025'),
    ('con013', 'efe002'),
    ('con013', 'efe038'),
    ('con014', 'efe037'),
    ('con014', 'efe078'),
    ('con015', 'efe003'),
    ('con015', 'efe024'),
    ('con016', 'efe025'),
    ('con016', 'efe083'),
    ('con017', 'efe039'),
    ('con017', 'efe083'),
    ('con018', 'efe001'),
    ('con018', 'efe024'),
    ('con019', 'efe025'),
    ('con019', 'efe078'),
    ('con020', 'efe004'),
    ('con020', 'efe084'),
    ('con021', 'efe039'),
    ('con022', 'efe027'),
    ('con022', 'efe079'),
    ('con023', 'efe005'),
    ('con023', 'efe025'),
    ('con024', 'efe006'),
    ('con024', 'efe037'),
    ('con025', 'efe029'),
    ('con026', 'efe010'),
    ('con026', 'efe081'),
    ('con027', 'efe003'),
    ('con027', 'efe022'),
    ('con028', 'efe010'),
    ('con029', 'efe026'),
    ('con029', 'efe086'),
    ('con030', 'efe006'),
    ('con030', 'efe041'),
    ('con031', 'efe027'),
    ('con031', 'efe083'),
    ('con032', 'efe026'),
    ('con032', 'efe078'),
    ('con033', 'efe028'),
    ('con033', 'efe079'),
    ('con034', 'efe015'),
    ('con034', 'efe030'),
    ('con034', 'efe072'),
    ('con035', 'efe004'),
    ('con035', 'efe041'),
    ('con036', 'efe073'),
    ('con036', 'efe004'),
    ('con037', 'efe077'),
    ('con037', 'efe079'),
    ('con038', 'efe075'),
    ('con038', 'efe083'),
    ('con039', 'efe028'),
    ('con040', 'efe006'),
    ('con040', 'efe022'),
    ('con041', 'efe004'),
    ('con041', 'efe071'),
    ('con042', 'efe039'),
    ('con042', 'efe085'),
    ('con043', 'efe002'),
    ('con043', 'efe039'),
    ('con044', 'efe024'),
    ('con044', 'efe071'),
    ('con045', 'efe022'),
    ('con045', 'efe038'),
    ('con046', 'efe003'),
    ('con046', 'efe040'),
    ('con047', 'efe021'),
    ('con047', 'efe038'),
    ('con048', 'efe001'),
    ('con048', 'efe025'),
    ('con049', 'efe045'),
    ('con049', 'efe083'),
    ('con050', 'efe020'),
    ('con050', 'efe078'),
    ('con050', 'efe085'),
    ('con051', 'efe004'),
    ('con051', 'efe022'),
    ('con052', 'efe038'),
    ('con052', 'efe078'),
    ('con053', 'efe024'),
    ('con053', 'efe085'),
    ('con054', 'efe005'),
    ('con054', 'efe081'),
    ('con055', 'efe025'),
    ('con055', 'efe084'),
    ('con056', 'efe003'),
    ('con056', 'efe071'),
    ('con057', 'efe001'),
    ('con057', 'efe023'),
    ('con058', 'efe005'),
    ('con058', 'efe071'),
    ('con059', 'efe038'),
    ('con059', 'efe085'),
    ('con060', 'efe023'),
    ('con060', 'efe036'),
    ('con061', 'efe073'),
    ('con061', 'efe085'),
    ('con062', 'efe042'),
    ('con062', 'efe080'),
    ('con063', 'efe005'),
    ('con063', 'efe037'),
    ('con064', 'efe026'),
    ('con064', 'efe078'),
    ('con065', 'efe024'),
    ('con065', 'efe037'),
    ('con066', 'efe009'),
    ('con066', 'efe085'),
    ('con067', 'efe002'),
    ('con067', 'efe084');



INSERT INTO receita
    (consumivel_produzido)
VALUES
    ('con028'),
    ('con029'),
    ('con030'),
    ('con031'),
    ('con032'),
    ('con033'),
    ('con034'),
    ('con035'),
    ('con036'),
    ('con037'),
    ('con038'),
    ('con039'),
    ('con040'),
    ('con041'),
    ('con042'),
    ('con043'),
    ('con044'),
    ('con045'),
    ('con046'),
    ('con047'),
    ('con048'),
    ('con049'),
    ('con050'),
    ('con051'),
    ('con052'),
    ('con053'),
    ('con054'),
    ('con055'),
    ('con056'),
    ('con057'),
    ('con058'),
    ('con059'),
    ('con060'),
    ('con061'),
    ('con062'),
    ('con063'),
    ('con064'),
    ('con065'),
    ('con066'),
    ('con067');



INSERT INTO ingrediente_nao_consumivel
    (identificador_receita, identificador_nao_consumivel)
VALUES
    ('rec001', 'ncn020'),
    ('rec005', 'ncn017'),
    ('rec009', 'ncn010'),
    ('rec009', 'ncn016'),
    ('rec013', 'ncn002'),
    ('rec013', 'ncn003'),
    ('rec014', 'ncn006'),
    ('rec014', 'ncn003'),
    ('rec015', 'ncn015'),
    ('rec015', 'ncn017'),
    ('rec016', 'ncn002'),
    ('rec018', 'ncn003'),
    ('rec019', 'ncn004'),
    ('rec020', 'ncn004'),
    ('rec022', 'ncn012'),
    ('rec023', 'ncn015'),
    ('rec024', 'ncn001'),
    ('rec024', 'ncn006'),
    ('rec025', 'ncn001'),
    ('rec025', 'ncn017'),
    ('rec026', 'ncn001'),
    ('rec027', 'ncn018'),
    ('rec027', 'ncn015'),
    ('rec028', 'ncn019'),
    ('rec030', 'ncn016'),
    ('rec032', 'ncn012'),
    ('rec034', 'ncn014'),
    ('rec035', 'ncn021'),
    ('rec036', 'ncn007'),
    ('rec036', 'ncn006'),
    ('rec037', 'ncn007'),
    ('rec038', 'ncn007'),
    ('rec039', 'ncn007');



INSERT INTO ingrediente_consumivel
    (identificador_receita, identificador_consumivel)
VALUES
    ('rec001', 'con006'),
    ('rec002', 'con006'),
    ('rec003', 'con002'),
    ('rec003', 'con017'),
    ('rec004', 'con017'),
    ('rec004', 'con010'),
    ('rec004', 'con003'),
    ('rec005', 'con016'),
    ('rec006', 'con011'),
    ('rec006', 'con003'),
    ('rec007', 'con028'),
    ('rec007', 'con031'),
    ('rec008', 'con017'),
    ('rec010', 'con036'),
    ('rec010', 'con011'),
    ('rec011', 'con036'),
    ('rec011', 'con016'),
    ('rec012', 'con006'),
    ('rec012', 'con011'),
    ('rec015', 'con013'),
    ('rec016', 'con001'),
    ('rec016', 'con002'),
    ('rec016', 'con014'),
    ('rec016', 'con021'),
    ('rec017', 'con015'),
    ('rec017', 'con014'),
    ('rec018', 'con003'),
    ('rec018', 'con010'),
    ('rec019', 'con010'),
    ('rec020', 'con005'),
    ('rec020', 'con006'),
    ('rec021', 'con016'),
    ('rec021', 'con015'),
    ('rec022', 'con026'),
    ('rec023', 'con026'),
    ('rec026', 'con017'),
    ('rec028', 'con019'),
    ('rec029', 'con009'),
    ('rec029', 'con013'),
    ('rec030', 'con012'),
    ('rec031', 'con013'),
    ('rec031', 'con012'),
    ('rec032', 'con011'),
    ('rec033', 'con018'),
    ('rec033', 'con014'),
    ('rec034', 'con016'),
    ('rec035', 'con017'),
    ('rec037', 'con014'),
    ('rec038', 'con025'),
    ('rec039', 'con041');



INSERT INTO progresso
    (numero_do_slot, data_ultimo_salvamento)
VALUES
    (1, null),
    (2, null),
    (3, null);



INSERT INTO ilha
	(nome)
VALUES
	('Ilha de Borabóia'), -- → ilh001
	('Cidade de Lurien'), -- → ilh002
	('Ilha Glacial de Frimora'), -- → ilh003
	('Cactuaraquara'), -- → ilh004
	('Nublária'), -- → ilh005
	('Quartel Naval D-57'); -- → ilh006



INSERT INTO ilha_visitada
    (identificador_progresso, identificador_ilha, visitada)
VALUES
    ('pro001', 'ilh001', TRUE),
    ('pro001', 'ilh002', FALSE),
    ('pro001', 'ilh003', FALSE),
    ('pro001', 'ilh004', FALSE),
    ('pro001', 'ilh005', FALSE),
    ('pro001', 'ilh006', FALSE),
    ('pro002', 'ilh001', TRUE),
    ('pro002', 'ilh002', FALSE),
    ('pro002', 'ilh003', FALSE),
    ('pro002', 'ilh004', FALSE),
    ('pro002', 'ilh005', FALSE),
    ('pro002', 'ilh006', FALSE),
    ('pro003', 'ilh001', TRUE),
    ('pro003', 'ilh002', FALSE),
    ('pro003', 'ilh003', FALSE),
    ('pro003', 'ilh004', FALSE),
    ('pro003', 'ilh005', FALSE),
    ('pro003', 'ilh006', FALSE);



INSERT INTO conexao_entre_ilhas
    (identificador_ilha_a, identificador_ilha_b, identificador_progresso)
VALUES
    ('ilh001', 'ilh002', 'pro001'),
    ('ilh001', 'ilh004', 'pro001'),
    ('ilh002', 'ilh003', 'pro001'),
    ('ilh002', 'ilh006', 'pro001'),
    ('ilh003', 'ilh004', 'pro001'),
    ('ilh003', 'ilh005', 'pro001'),
    ('ilh005', 'ilh006', 'pro001'),
    ('ilh001', 'ilh002', 'pro002'),
    ('ilh001', 'ilh004', 'pro002'),
    ('ilh002', 'ilh003', 'pro002'),
    ('ilh002', 'ilh006', 'pro002'),
    ('ilh003', 'ilh004', 'pro002'),
    ('ilh003', 'ilh005', 'pro002'),
    ('ilh005', 'ilh006', 'pro002'),
    ('ilh001', 'ilh002', 'pro003'),
    ('ilh001', 'ilh004', 'pro003'),
    ('ilh002', 'ilh003', 'pro003'),
    ('ilh002', 'ilh006', 'pro003'),
    ('ilh003', 'ilh004', 'pro003'),
    ('ilh003', 'ilh005', 'pro003'),
    ('ilh005', 'ilh006', 'pro003');



INSERT INTO area
	(identificador_ilha, nome, tipo_area, chave_imagem_fundo, chave_imagem_frente)
VALUES
	('ilh001', 'Pastos do Sol Dourado', 'Área de combate', 'cenario_boraboia_pastos', 'cenario_boraboia_pastos_camada_superior'), -- → are001
	('ilh001', 'Vilarejo de Borabóia', 'Vila', 'cenario_boraboia_vila', null), -- → are002
	('ilh001', 'Vale Verdejante', 'Porto', 'cenario_boraboia_vale', 'cenario_boraboia_vale_camada_superior'), -- → are003
	('ilh001', 'Loja de Borabóia', 'Loja', 'loja_interior', null), -- → are004
	('ilh001', 'Casa', 'Vila', 'cenario_boraboia_casa', null), -- → are005
	('ilh001', 'Sótão', 'Vila', 'cenario_boraboia_sotao', null), -- → are006
	('ilh002', 'Porto de Lurien', 'Porto', 'cenario_lurien_porto', 'cenario_lurien_porto_camada_superior'), -- → are007
	('ilh002', 'Centro', 'Área neutra', 'cenario_lurien_centro', null), -- → are008
	('ilh002', 'Praça de execução', 'Área de combate', 'cenario_lurien_praca', 'cenario_lurien_praca_camada_superior'), -- → are009
	('ilh002', 'Beco', 'Área neutra', 'cenario_lurien_beco', null), -- → are010
	('ilh002', 'Esconderijo', 'Área neutra', 'cenario_lurien_esconderijo', null), -- → are011
	('ilh002', 'Prisão', 'Área neutra', 'cenario_lurien_prisao', null), -- → are012
	('ilh002', 'Loja de espadas', 'Loja', 'loja_interior', null), -- → are013
	('ilh002', 'Loja de acessórios', 'Loja', 'loja_interior', null), -- → are014
	('ilh003', 'Costa de Frimora', 'Porto', 'cenario_frimora_costa', null), -- → are015
	('ilh003', 'Vila de Frimora', 'Vila', 'cenario_frimora_vila', null), -- → are016
	('ilh003', 'Floresta de Frimora', 'Área de combate', 'cenario_frimora_floresta', 'cenario_frimora_floresta_camada_superior'), -- → are017
	('ilh003', 'Montanha da Cabra Congelada', 'Área de combate', 'cenario_frimora_montanha', null), -- → are018
	('ilh003', 'Cozinha da Vovó Yuba', 'Loja', 'cozinha_interior', null), -- → are019
	('ilh003', 'Loja de Frimora', 'Loja', 'loja_interior', null), -- → are020
	('ilh004', 'Duna Braba', 'Porto', 'cenario_cactuaraquara_duna', null), -- → are021
	('ilh004', 'Cidadela de Cactuaraquara', 'Vila', 'cenario_cactuaraquara_cidadela', null), -- → are022
	('ilh004', 'Oásis de Ramtak', 'Área de combate', 'cenario_cactuaraquara_oasis', null), -- → are023
	('ilh004', 'Loja de Cactuaraquara', 'Loja', 'loja_interior', null), -- → are024
	('ilh004', 'Loja de armas', 'Loja', 'loja_interior', null), -- → are025
	('ilh005', 'Penumbra dos Ossudos', 'Porto', 'cenario_nublaria_penumbra', null), -- → are026
	('ilh005', 'Acampamento de Nublária', 'Vila', 'cenario_nublaria_acampamento', null), -- → are027
	('ilh005', 'Floresta', 'Área de combate', 'cenario_nublaria_floresta', null), -- → are028
	('ilh005', 'Loja de Nublária', 'Loja', 'loja_interior', null), -- → are029
	('ilh006', 'Porto da Égide', 'Porto', 'cenario_quartel_porto', null), -- → are030
	('ilh006', 'Interior', 'Área de combate', 'cenario_quartel_interior', null), -- → are031
	('ilh006', 'Escritório do Vice-Almirante', 'Área neutra', 'cenario_quartel_escritorio', null), -- → are032
	('ilh006', 'Loja da Marinha', 'Loja', 'loja_interior', null), -- → are033
    (null, 'Yomotsu Hirasaka', 'Yomotsu Hirasaka', null, null); -- → are034



INSERT INTO conexao_entre_areas
    (identificador_area_origem, identificador_area_destino, ponto_geracao_x,
    ponto_geracao_y, orientacao)
VALUES
    ('are001', 'are002', 100, 370, 'direita'),
    ('are002', 'are001', 4373, 174, 'esquerda'),
    ('are002', 'are003', 50, 190, 'direita'),
    ('are003', 'are002', 3361, 370, 'esquerda'),
    ('are003', 'are007', 2470, 265, 'esquerda'), -- ilh001 → ilh002
    ('are003', 'are021', 100, 415, 'direita'), -- ilh001 → ilh004
    ('are002', 'are004', 100, 275, 'direita'),
    ('are004', 'are002', 1781, 312, 'esquerda'),
    ('are002', 'are005', 0, 0, 'esquerda'),
    ('are005', 'are002', 2147, 312, 'esquerda'),
    ('are005', 'are006', 0, 0, 'esquerda'),
    ('are006', 'are005', 0, 0, 'esquerda'),
    ('are007', 'are008', 100, 415, 'direita'),
    ('are007', 'are003', 4160, 280, 'esquerda'),-- ilh002 → ilh001
    ('are007', 'are015', 645, 735, 'esquerda'),-- ilh002 → ilh003
    ('are007', 'are030', 0, 0, 'direita'),-- ilh002 → ilh006
    ('are008', 'are007', 680, 175, 'esquerda'),
    ('are008', 'are009', 100, 415, 'direita'),
    ('are009', 'are008', 1570, 460, 'esquerda'),
    ('are008', 'are010', 0, 0, 'direita'),
    ('are010', 'are008', 0, 0, 'esquerda'),
    ('are008', 'are014', 0, 0, 'esquerda'),
    ('are014', 'are008', 1083, 397, 'direita'),
    ('are009', 'are012', 0, 0, 'direita'),
    ('are012', 'are009', 1439, 111, 'esquerda'),
    ('are009', 'are013', 0, 0, 'esquerda'),
    ('are013', 'are009', 289, 397, 'direita'),
    ('are010', 'are011', 0, 0, 'esquerda'),
    ('are011', 'are010', 0, 0, 'esquerda'),
    ('are015', 'are016', 2870, 415, 'esquerda'),
    ('are015', 'are007', 2470, 265, 'esquerda'),-- ilh003 → ilh002
    ('are015', 'are021', 0, 0, 'esquerda'),-- ilh003 → ilh004
    ('are015', 'are026', 0, 0, 'esquerda'),-- ilh003 → ilh005
    ('are016', 'are015', 50, 700, 'direita'),
    ('are016', 'are017', 1410, 775, 'esquerda'),
    ('are017', 'are016', 50, 415, 'direita'),
    ('are016', 'are019', 0, 0, 'direita'),
    ('are019', 'are016', 695, 320, 'direita'),
    ('are016', 'are020', 0, 0, 'esquerda'),
    ('are020', 'are016', 1460, 320, 'direita'),
    ('are017', 'are018', 1377, 757, 'esquerda'),
    ('are018', 'are017', 50, 750, 'direita'),
    ('are021', 'are022', 0, 0, 'esquerda'),
    ('are021', 'are003', 4160, 280, 'esquerda'),-- ilh004 → ilh001
    ('are021', 'are015', 0, 0, 'esquerda'),-- ilh004 → ilh003
    ('are022', 'are021', 0, 0, 'esquerda'),
    ('are022', 'are023', 0, 0, 'esquerda'),
    ('are023', 'are022', 0, 0, 'esquerda'),
    ('are022', 'are024', 0, 0, 'esquerda'),
    ('are024', 'are022', 0, 0, 'esquerda'),
    ('are022', 'are025', 0, 0, 'esquerda'),
    ('are025', 'are022', 0, 0, 'esquerda'),
    ('are026', 'are027', 0, 0, 'esquerda'),
    ('are027', 'are026', 0, 0, 'esquerda'),
    ('are027', 'are028', 0, 0, 'esquerda'),
    ('are028', 'are027', 0, 0, 'esquerda'),
    ('are027', 'are029', 0, 0, 'esquerda'),
    ('are029', 'are027', 0, 0, 'esquerda'),
    ('are030', 'are030', 0, 0, 'esquerda'),
    ('are030', 'are003', 2470, 265, 'esquerda'),-- ilh006 → ilh002
    ('are030', 'are026', 0, 0, 'esquerda'),-- ilh006 → ilh005
    ('are031', 'are031', 0, 0, 'esquerda'),
    ('are031', 'are032', 0, 0, 'esquerda'),
    ('are032', 'are031', 0, 0, 'esquerda'),
    ('are031', 'are033', 0, 0, 'esquerda'),
    ('are033', 'are031', 0, 0, 'esquerda');



INSERT INTO area_interativa
    (identificador_area_origem, identificador_area_destino, x, y, largura, altura, tipo_evento, metodo_ativacao)
VALUES
    ('are001', 'are002', 4473, 187, 30, 180, 'mudar_area', 'ativo'), -- → vila
    ('are002', 'are001', 0, 360, 50, 150, 'mudar_area', 'ativo'), -- → pastos
    ('are002', 'are004', 1716, 300, 200, 40, 'mudar_area', 'ativo'), -- → loja
    ('are002', 'are003', 3490, 360, 50, 150, 'mudar_area', 'ativo'), -- → vale
    ('are003', 'are002', 0, 200, 50, 150, 'mudar_area', 'ativo'), -- → vila
    ('are003', null, 4205, 313, 50, 158, 'embarcar', 'ativo'), -- → navegar
    ('are004', 'are002', 0, 300, 50, 270, 'mudar_area', 'ativo'), -- → sair da loja
    ('are007', 'are008', 610, 185, 250, 20, 'mudar_area', 'ativo'), -- → centro
    ('are007', null, 2472, 375, 93, 67, 'embarcar', 'ativo'), -- → navegar
    ('are008', 'are007', 0, 480, 50, 150, 'mudar_area', 'ativo'), -- → porto
    ('are008', 'are009', 1656, 484, 50, 150, 'mudar_area', 'ativo'), -- → praça
    ('are009', 'are008', 0, 500, 50, 85, 'mudar_area', 'ativo'), -- → centro
    ('are015', 'are016', 0, 745, 50, 100, 'mudar_area', 'ativo'), -- → vila
    ('are015', null, 960, 930, 80, 90, 'embarcar', 'ativo'), -- → navegar
    ('are016', 'are015', 2950, 473, 50, 100, 'mudar_area', 'ativo'), -- → costa
    ('are016', 'are017', 0, 473, 50, 100, 'mudar_area', 'ativo'), -- → floresta
    ('are016', 'are019', 695, 273, 78, 108, 'mudar_area', 'ativo'), -- → cozinha
    ('are016', 'are020', 1449, 269, 95, 108, 'mudar_area', 'ativo'), -- → loja
    ('are017', 'are016', 1486, 735, 50, 290, 'mudar_area', 'ativo'), -- → vila
    ('are017', 'are018', 0, 735, 50, 290, 'mudar_area', 'ativo'), -- → montanha
    ('are018', 'are017', 1486, 735, 50, 172, 'mudar_area', 'ativo'), -- → floresta
    ('are019', 'are016', 0, 0, 50, 600, 'mudar_area', 'ativo'), -- → vila
    ('are020', 'are016', 0, 0, 50, 600, 'mudar_area', 'ativo'); -- → vila



INSERT INTO area_interativa
    (identificador_area_origem, chave_imagem, x, y, chance_sucesso, tipo_evento, metodo_ativacao)
VALUES
    ('are001', 'arbusto', 1247, 119, 0.5, 'investigar', 'ativo'),
    ('are001', 'arbusto', 2955, 111, 0.5, 'investigar', 'ativo'),
    ('are002', 'arbusto', 559, 359, 0.5, 'investigar', 'ativo'),
    ('are002', 'arbusto', 741, 361, 0.5, 'investigar', 'ativo'),
    ('are002', 'arbusto', 1903, 354, 0.5, 'investigar', 'ativo'),
    ('are002', 'arbusto', 1903, 354, 0.5, 'investigar', 'ativo'),
    ('are003', 'arbusto', 817, 138, 0.5, 'investigar', 'ativo'),
    ('are003', 'arbusto', 2692, 126, 0.5, 'investigar', 'ativo'),
    ('are003', 'arbusto', 3160, 132, 0.5, 'investigar', 'ativo');

    

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
    ('are015', 'normal', 0, 705, 1130, 319),
    ('are015', 'neve', 0, 705, 675, 60),
    ('are015', 'neve', 0, 853, 247, 172),
    ('are015', 'neve', 247, 878, 334, 147),
    ('are015', 'neve', 581, 910, 72, 115),
    ('are015', 'neve', 653, 931, 92, 94),
    ('are015', 'neve', 745, 970, 70, 55),
    ('are016', 'normal', 0, 407, 3540, 193),
    ('are016', 'neve', 0, 407, 3540, 74),
    ('are016', 'neve', 0, 571, 3540, 29),
    ('are017', 'arena', 0, 735, 1536, 289),
    ('are017', 'neve', 0, 735, 1536, 289);



INSERT INTO obstaculo
    (identificador_area, x, y, largura, altura)
VALUES
    ('are003', 3717, 471, 250, 24),
    ('are007', 354, 390, 93, 22),
    ('are007', 1413, 390, 93, 22),
    ('are007', 2472, 390, 93, 22),
    ('are008', 1539, 418, 102, 17),
    ('are008', 1641, 435, 41, 25),
    ('are017', 635, 781, 56, 100),
    ('are017', 1208, 968, 121, 56),
    ('are017', 201, 978, 121, 46);


-- Vendedores
INSERT INTO habitante
    (identificador_area, nome, descricao, tipo_habitante, coordenada_x, coordenada_y, moedas_totais, chave_imagem, especialidade)
VALUES
    ('are004', 'Sr. Lee', 'Sr. Lee, o mestre das marmitas rurais! Vende ovos frescos, arroz do planalto e conselhos que parecem saídos de um livro de provérbios... mal traduzido.', 'ven', 288, 151, 500, 'lee_busto', 'com'), -- ven001
    ('are007', 'Sr. Lee', 'No meio do caos urbano, lá está ele com seu carrinho fumegante e um avental engordurado. Sr. Lee serve lanches rápidos e piadas mais rápidas ainda.', 'ven', 236, 196, 500, 'lee', 'com'), -- ven002
    ('are020', 'Sr. Lee', 'Enrolado num cachecol de 3 metros, Sr. Lee vende chocolate amargo e leite alpino — e jura que já enfrentou uma nevasca com uma colher de pau.', 'ven', 288, 151, 500, 'lee_busto', 'com'), -- ven003
    ('are024', 'Sr. Lee', 'Com um turbante improvisado e um leque de papel, Sr. Lee sobrevive ao calor vendendo sucos gelados e histórias que evaporam no ar.', 'ven', 288, 151, 500, 'lee_busto', 'com'), -- ven004
    ('are029', 'Sr. Lee', 'Sr. Lee aparece entre névoas e estalidos de correntes. Vende doces suspeitos e garante que o ‘açúcar estranho’ não morde... mais.', 'ven', 288, 151, 500, 'lee_busto', 'com'), -- ven005
    ('are033', 'Sr. Lee', 'Uniformizado (mais ou menos), Sr. Lee comanda a cantina da fortaleza. Serve café turbinado e carne de rei dos mares com disciplina... e sarcasmo.', 'ven', 288, 151, 500, 'lee_busto', 'com'); -- ven006



INSERT INTO habitante
    (identificador_area, nome, descricao, tipo_habitante, coordenada_x, coordenada_y, moedas_totais, chave_imagem)
VALUES
    ('are034', 'Narrador', null, 'hbt', 0, 0, 0, null), -- hbt001
    ('are001', 'Tião Palha', 'Camponês experiente e bem-humorado, Tião é o primeiro rosto amigável que você encontra. Com seu chapéu surrado e risada fácil, ele esconde sob a simplicidade um olhar atento e um coração generoso.', 'hbt', 2040, 90, 15, 'campones_a'), -- hbt002
    ('are002', 'Tia Cotinha da Cestinha', 'Tia Cotinha é a guardiã não-oficial da vila — e do seu cesto de legumes! Com seu lenço florido, passos curtos e uma memória afiada como faca de cozinha, ela sabe tudo o que acontece por ali. Sempre pronta com um conselho, uma receita ou uma fofoca fresquinha, Cotinha é a primeira a notar quando algo está fora do lugar. Dizem que ela já enfrentou um javali com nada além de uma colher de pau... mas ela nunca confirma nem nega.', 'hbt', 1586, 340, 15, 'camponesa_b'), -- hbt003
    ('are002', 'Signore Bigodini', 'Antigo pizzaiolo de uma vila costeira que trocou o forno à lenha por uma enxada, Signore Bigodini é o único fazendeiro que tempera a terra com orégano. Seu bigode é tão expressivo quanto sua voz, e ele gesticula tanto que já espantou corvos só com as mãos. Fala com paixão, exagero e um sotaque que ninguém sabe se é real ou só charme.', 'rct', 2231, 350, 15, 'campones_b'), -- rct001
    ('are002', 'Lina Panela', 'Jovem cozinheira da vila, entusiasmada, dramática e um pouco desastrada. Sonha em criar o “Omurice Supremo” que vai conquistar o mundo — ou pelo menos o paladar dos camponeses. Fala como se estivesse sempre em um programa de culinária.', 'rct', 300, 306, 15, 'camponesa_a'); -- rct002



INSERT INTO lacaio
    (nome, descricao, vida, nivel, experiencia, tempo_reacao)
VALUES
    ('Corvo',	'Um bico afiado e uma risada sarcástica. Costuma roubar frutas e orgulho.', 8, 1, 10, 750), -- lac001 vida=8(1+0.05*nível)^(1.5)
    ('Lobo',	'Uiva alto, morde forte e adora assustar viajantes desavisados.', 11, 7, 10, 1200), -- lac002
    ('Brutamontes',	'Grande, mal-humorado e com um gosto inusitado por doces.', 16, 12, 15, 900), -- lac003
    ('Marinheiro Corrupto',	'Usa o uniforme da Marinha, mas segue as ordens do bolso.', 20, 17, 17, 900), -- lac004
    ('Pirata Congelado',	'Foi soterrado pela neve... e agora está de volta para esfriar os ânimos.', 24, 22, 22, 900), -- lac005
    ('Alma Soterrada',	'Um espírito inquieto com voz gelada e olhos que brilham no escuro.', 28, 27, 27, 900), -- lac006
    ('Pirata do Deserto',	'Armado com espadas enferrujadas e piadas secas como o clima.', 33, 32, 32, 900), -- lac007
    ('Pirata Iludido',	'Perdeu o rumo e parte da sanidade nas miragens. Ainda acha que está no mar.', 38, 37, 37, 900), -- lac008
    ('Morcego',	'Só aparece no escuro. Detesta luz e adora cabelo desgrenhado.', 43, 42, 42, 900), -- lac009
    ('Aranha',	'Anda silenciosa e deixa rastros de teia e calafrios por onde passa.', 49, 47, 47, 900), -- lac010
    ('Marinheiro',	'Cansado, mal pago, mas ainda tenta manter a postura.', 54, 52, 52, 900), -- lac011
    ('Oficial da Marinha',	'Sabe gritar "atenção!" melhor do que lutar, mas impõe respeito.', 60, 57, 57, 900); -- lac012



INSERT INTO instancia_lacaio
    (identificador_lacaio, identificador_area, coordenada_x, coordenada_y, moedas_totais)
VALUES
    ('lac001', 'are001', 3430, 55, 0),
    ('lac001', 'are001', 4273, 412, 0),
    ('lac001', 'are001', 3600, 427, 0),
    ('lac002', 'are002', 1500, 125, 0),
    ('lac002', 'are002', 1900, 400, 0),
    ('lac002', 'are002', 2360, 210, 0);



INSERT INTO estado_instancia_lacaio
    (identificador_progresso, identificador_instancia_lacaio, identificador_area_atual, vida_atual)
VALUES
    ('pro001', 'ins001', 'are001', 5),
    ('pro001', 'ins002', 'are001', 5),
    ('pro001', 'ins003', 'are001', 5),
    ('pro001', 'ins004', 'are003', 7),
    ('pro001', 'ins005', 'are003', 7),
    ('pro001', 'ins006', 'are003', 7),
    ('pro002', 'ins001', 'are001', 5),
    ('pro002', 'ins002', 'are001', 5),
    ('pro002', 'ins003', 'are001', 5),
    ('pro002', 'ins004', 'are003', 7),
    ('pro002', 'ins005', 'are003', 7),
    ('pro002', 'ins006', 'are003', 7),
    ('pro003', 'ins001', 'are001', 5),
    ('pro003', 'ins002', 'are001', 5),
    ('pro003', 'ins003', 'are001', 5),
    ('pro003', 'ins004', 'are003', 7),
    ('pro003', 'ins005', 'are003', 7),
    ('pro003', 'ins006', 'are003', 7);



INSERT INTO chefe
    (identificador_area, nome, descricao, coordenada_x, coordenada_y, vida, nivel, experiencia, moedas_totais)
VALUES
    ('are001', 'Javali',	'Um tanque com presas. Corre como se tivesse dívida com o vento.', 0, 0, 14, 10, 20, 0),
    ('are009', 'Capitão Renegado',	'Exibido, barulhento e com um corte de cabelo que grita "autoridade duvidosa".', 0, 0, 22, 20, 30, 100),
    ('are015', 'Imediato Espectral',	'Leal até depois da morte. Ainda segue ordens do velho capitão pirata.', 0, 0, 31, 30, 40, 30),
    ('are019', 'Capitão das Areias',	'Tático, traiçoeiro e com um bigode que desafia a gravidade.', 0, 0, 41, 40, 50, 50),
    ('are023', 'Aranha Gigante',	'Gosta de se pendurar no teto e pregar sustos. Tem um ego do tamanho do abdômen.', 0, 0, 52, 50, 60, 0),
    ('are026', 'Vice-Almirante Caelum Drayke',	'Um estrategista implacável... quando sua segunda personalidade não atrapalha.',0, 0, 100, 60, 60, 200),
    ('are026', 'Vice-Almirante Caelum Drayke',	'Um estrategista implacável... quando sua segunda personalidade não atrapalha.',0, 0, 120, 60, 70, 200),
    ('are026', 'Vice-Almirante Caelum Drayke',	'Um estrategista implacável... quando sua segunda personalidade não atrapalha.',0, 0, 150, 60, 80, 200);



INSERT INTO estado_chefe
    (identificador_area_atual, identificador_progresso, identificador_chefe, vida_atual)
VALUES
    ('are001', 'pro001', 'che001', 14),
    ('are009', 'pro001', 'che002', 22),
    ('are015', 'pro001', 'che003', 31),
    ('are019', 'pro001', 'che004', 41),
    ('are023', 'pro001', 'che005', 52),
    ('are026', 'pro001', 'che006', 100),
    ('are026', 'pro001', 'che007', 120),
    ('are026', 'pro001', 'che008', 150),
    ('are001', 'pro002', 'che001', 14),
    ('are009', 'pro002', 'che002', 22),
    ('are015', 'pro002', 'che003', 31),
    ('are019', 'pro002', 'che004', 41),
    ('are023', 'pro002', 'che005', 52),
    ('are026', 'pro002', 'che006', 100),
    ('are026', 'pro002', 'che007', 120),
    ('are026', 'pro002', 'che008', 150),
    ('are001', 'pro003', 'che001', 14),
    ('are009', 'pro003', 'che002', 22),
    ('are015', 'pro003', 'che003', 31),
    ('are019', 'pro003', 'che004', 41),
    ('are023', 'pro003', 'che005', 52),
    ('are026', 'pro003', 'che006', 100),
    ('are026', 'pro003', 'che007', 120),
    ('are026', 'pro003', 'che008', 150);



INSERT INTO habilidade_personagem
    (identificador_personagem, identificador_habilidade)
VALUES
    ('lac001', 'hab043'),
    ('lac002', 'hab044'),
    ('che001', 'hab045'),
    ('lac003', 'hab046'),
    ('lac004', 'hab047'),
    ('che002', 'hab048'),
    ('lac005', 'hab049'),
    ('lac006', 'hab050'),
    ('che003', 'hab051'),
    ('lac007', 'hab052'),
    ('lac008', 'hab053'),
    ('che004', 'hab054'),
    ('lac009', 'hab055'),
    ('lac010', 'hab056'),
    ('che005', 'hab057'),
    ('lac011', 'hab058'),
    ('lac012', 'hab059'),
    ('che006', 'hab060'),
    ('che006', 'hab061'),
    ('che006', 'hab062'),
    ('che006', 'hab063'),
    ('che006', 'hab064');



-- Inventários de inimigos
INSERT INTO inventario
    (identificador_personagem, identificador_progresso)
VALUES
    ('lac001', 'pro001'), -- inv001
    ('lac002', 'pro001'), -- inv002
    ('lac003', 'pro001'), -- inv003
    ('lac004', 'pro001'), -- inv004
    ('lac005', 'pro001'), -- inv005
    ('lac006', 'pro001'), -- inv006
    ('lac007', 'pro001'), -- inv007
    ('lac008', 'pro001'), -- inv008
    ('lac009', 'pro001'), -- inv009
    ('lac010', 'pro001'), -- inv010
    ('lac011', 'pro001'), -- inv011
    ('lac012', 'pro001'), -- inv012
    ('che001', 'pro001'), -- inv013
    ('che002', 'pro001'), -- inv014
    ('che003', 'pro001'), -- inv015
    ('che004', 'pro001'), -- inv016
    ('che005', 'pro001'), -- inv017
    ('che006', 'pro001'), -- inv018
    ('lac001', 'pro002'), -- inv019
    ('lac002', 'pro002'), -- inv020
    ('lac003', 'pro002'), -- inv021
    ('lac004', 'pro002'), -- inv022
    ('lac005', 'pro002'), -- inv023
    ('lac006', 'pro002'), -- inv024
    ('lac007', 'pro002'), -- inv025
    ('lac008', 'pro002'), -- inv026
    ('lac009', 'pro002'), -- inv027
    ('lac010', 'pro002'), -- inv028
    ('lac011', 'pro002'), -- inv029
    ('lac012', 'pro002'), -- inv030
    ('che001', 'pro002'), -- inv031
    ('che002', 'pro002'), -- inv032
    ('che003', 'pro002'), -- inv033
    ('che004', 'pro002'), -- inv034
    ('che005', 'pro002'), -- inv035
    ('che006', 'pro002'), -- inv036
    ('lac001', 'pro003'), -- inv037
    ('lac002', 'pro003'), -- inv038
    ('lac003', 'pro003'), -- inv039
    ('lac004', 'pro003'), -- inv040
    ('lac005', 'pro003'), -- inv041
    ('lac006', 'pro003'), -- inv042
    ('lac007', 'pro003'), -- inv043
    ('lac008', 'pro003'), -- inv044
    ('lac009', 'pro003'), -- inv045
    ('lac010', 'pro003'), -- inv046
    ('lac011', 'pro003'), -- inv047
    ('lac012', 'pro003'), -- inv048
    ('che001', 'pro003'), -- inv049
    ('che002', 'pro003'), -- inv050
    ('che003', 'pro003'), -- inv051
    ('che004', 'pro003'), -- inv052
    ('che005', 'pro003'), -- inv053
    ('che006', 'pro003'); -- inv054



-- Inventários de habitantes
INSERT INTO inventario
    (identificador_personagem, identificador_progresso)
VALUES
    ('ven001', 'pro001'), -- inv055
    ('ven001', 'pro002'), -- inv056
    ('ven001', 'pro003'); -- inv057



-- Itens dos habitantes
INSERT INTO item_inventario
    (identificador_inventario, identificador_item, quantidade)
VALUES
    ('inv055', 'ncn001', 20),
    ('inv055', 'ncn002', 20),
    ('inv055', 'ncn003', 20),
    ('inv056', 'ncn001', 20),
    ('inv056', 'ncn002', 20),
    ('inv056', 'ncn003', 20),
    ('inv057', 'ncn001', 20),
    ('inv057', 'ncn002', 20),
    ('inv057', 'ncn003', 20);



-- Itens dos inimigos
INSERT INTO item_inventario
    (identificador_inventario, identificador_item, quantidade)
VALUES
    ('inv001', 'ncn004', 1),
    ('inv002', 'ncn005', 1),
    ('inv003', 'con008', 1),
    ('inv004', 'ncn009', 1),
    ('inv005', 'ncn011', 1),
    ('inv006', 'ncn012', 1),
    ('inv007', 'ncn013', 1),
    ('inv008', 'ncn014', 1),
    ('inv009', 'ncn018', 1),
    ('inv010', 'ncn019', 1),
    ('inv011', 'con027', 1),
    ('inv012', 'ncn022', 1),
    ('inv019', 'ncn004', 1),
    ('inv020', 'ncn005', 1),
    ('inv021', 'con008', 1),
    ('inv022', 'ncn009', 1),
    ('inv023', 'ncn011', 1),
    ('inv024', 'ncn012', 1),
    ('inv025', 'ncn013', 1),
    ('inv026', 'ncn014', 1),
    ('inv027', 'ncn018', 1),
    ('inv028', 'ncn019', 1),
    ('inv029', 'con027', 1),
    ('inv030', 'ncn022', 1),
    ('inv037', 'ncn004', 1),
    ('inv038', 'ncn005', 1),
    ('inv039', 'con008', 1),
    ('inv040', 'ncn009', 1),
    ('inv041', 'ncn011', 1),
    ('inv042', 'ncn012', 1),
    ('inv043', 'ncn013', 1),
    ('inv044', 'ncn014', 1),
    ('inv045', 'ncn018', 1),
    ('inv046', 'ncn019', 1),
    ('inv047', 'con027', 1),
    ('inv048', 'ncn022', 1);



INSERT INTO missao
    (identificador_area, identificador_missao_dependente, nivel_de_desbloqueio, identificador_recrutador, descricao, nome)
VALUES
    ('are001', 'mis002', 0, null, 'Desperte nesse local desconhecido', 'Acordei e Já Tô Perdido'), -- mis001
    ('are001', 'mis003', 0, null, 'Derrote o lobo que te atacou de repente no caminho para a vila.', 'Lobicho Maldito!'), -- mis002
    ('are002', null, 1, null, 'Chegue na vila.', 'Cadê o Waze Medieval?'), -- mis003
    ('are001', null, 1,'rct001', 'Espante os corvos da plantação', 'Corvo Não Paga Aluguel'), -- mis004
    ('are003', null, 2,'rct001', 'Conserte a cerca danificada', 'Cercando o Prejuízo'), -- mis005
    ('are003', null, 3,'rct001', 'Afugente os lobos', 'Sai Pra Lá, Fido!'), -- mis006
    ('are003', 'mis010', 5, 'rct002', 'Busque água do poço', 'Água Mole, Braço Duro'), -- mis007
    ('are001', 'mis010', 5, 'rct002', 'Colete Arroz do Planalto', 'Grão a Grão, o Saco Enche'), -- mis008
    ('are002', 'mis010', 5, 'rct002', 'Colete Ovo dos Campos', 'Operação: Caça ao Ovo'), -- mis009
    ('are002', null, 5, 'rct002', 'Entregue os ingredientes para o Omurice de Arroz', 'Missão: Omelete Impossível'), -- mis010
    ('are001', null, 10, null, 'Enfrente a fera que está atacando camponeses e destruindo plantações perto da vila.', 'A Fera Tá Solta (E Brava)'), -- mis011
    ('are003', null, 10, null, 'Embarque para a próxima ilha', 'Remando e Rezando'); -- mis012

-- -- Adicione vendedores nas áreas das lojas
-- INSERT INTO habitante
--     (identificador_area, nome, descricao, tipo_habitante, coordenada_x, coordenada_y, especialidade, moedas_totais)
-- VALUES
--     ('are004', 'João das Ferramentas', 'Vendedor de armas e acessórios', 'ven', 400, 300, 'arm', 500),
--     ('are016', 'Vovó Yuba', 'Cozinheira e vendedora de comidas', 'ven', 400, 200, 'com', 300),
--     ('are020', 'Mercador das Dunas', 'Vendedor especializado', 'ven', 400, 300, 'ace', 400),
--     ('are024', 'Comerciante Sombrio', 'Vendedor de itens raros', 'ven', 400, 300, 'com', 600),
--     ('are029', 'Intendente Naval', 'Vendedor militar', 'ven', 400, 300, 'arm', 800);
-- 
-- -- Crie inventários para os vendedores
-- INSERT INTO inventario (identificador_personagem, tipo_inventario)
-- VALUES 
--     ('ven001', 'ger'),
--     ('ven002', 'ger'),
--     ('ven003', 'ger'),
--     ('ven004', 'ger'),
--     ('ven005', 'ger');
-- 
-- -- Adicione itens aos inventários dos vendedores
-- INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
-- VALUES
--     -- Vendedor de Borabóia (armas básicas)
--     ('inv019', 'arm001', 3),
--     ('inv019', 'arm010', 2),
--     ('inv019', 'ace001', 1),
--     
--     -- Vovó Yuba (ingredientes e comidas)
--     ('inv020', 'ncn001', 10),
--     ('inv020', 'ncn002', 8),
--     ('inv020', 'con012', 5),
--     
--     -- Vendedor do Deserto (itens especiais)
--     ('inv021', 'arm002', 2),
--     ('inv021', 'ace002', 1),
--     
--     -- Vendedor Sombrio (itens raros)
--     ('inv022', 'con020', 3),
--     ('inv022', 'con021', 2),
--     
--     -- Intendente Naval (equipamentos militares)  
--     ('inv023', 'arm001', 5),
--     ('inv023', 'con023', 10);
-- 
-- INSERT INTO habitante
--     (identificador_area, nome, descricao, tipo_habitante, coordenada_x, coordenada_y, especialidade, moedas_totais)
-- VALUES
--     ('are004', 'João das Ferramentas', 'Vendedor de armas e acessórios', 'ven', 400, 300, 'arm', 100);
-- 
INSERT INTO area_interativa
    (identificador_area_origem, x, y, largura, altura, tipo_evento, metodo_ativacao, ativa)
VALUES
    ('are004', 700, 500, 100, 100, 'abrir_loja', 'ativo', TRUE);


INSERT INTO estado_missao
    (identificador_missao, identificador_progresso)
VALUES
    ('mis001', 'pro001'),
    ('mis002', 'pro001'),
    ('mis003', 'pro001'),
    ('mis004', 'pro001'),
    ('mis005', 'pro001'),
    ('mis006', 'pro001'),
    ('mis007', 'pro001'),
    ('mis008', 'pro001'),
    ('mis009', 'pro001'),
    ('mis010', 'pro001'),
    ('mis011', 'pro001'),
    ('mis012', 'pro001'),
    ('mis001', 'pro002'),
    ('mis002', 'pro002'),
    ('mis003', 'pro002'),
    ('mis004', 'pro002'),
    ('mis005', 'pro002'),
    ('mis006', 'pro002'),
    ('mis007', 'pro002'),
    ('mis008', 'pro002'),
    ('mis009', 'pro002'),
    ('mis010', 'pro002'),
    ('mis011', 'pro002'),
    ('mis012', 'pro002'),
    ('mis001', 'pro003'),
    ('mis002', 'pro003'),
    ('mis003', 'pro003'),
    ('mis004', 'pro003'),
    ('mis005', 'pro003'),
    ('mis006', 'pro003'),
    ('mis007', 'pro003'),
    ('mis008', 'pro003'),
    ('mis009', 'pro003'),
    ('mis010', 'pro003'),
    ('mis011', 'pro003'),
    ('mis012', 'pro003');



INSERT INTO item_missao
    (identificador_missao, identificador_item, quantidade)
VALUES
    ('mis010', 'con040', 1);



INSERT INTO dialogo
    (identificador_personagem, identificador_missao, sequencia_local, genero, dialogo)
VALUES
    ('hbt001', 'mis001', 1, 'F', 'O som do vento sussurrava entre as altas folhas douradas. O sol da manhã já aquecia a terra quando uma jovem de cabelos bagunçados abriu os olhos pela primeira vez naquele lugar desconhecido.'),
    ('hbt001', 'mis001', 1, 'M', 'O som do vento sussurrava entre as altas folhas douradas. O sol da manhã já aquecia a terra quando um jovem de cabelos bagunçados abriu os olhos pela primeira vez naquele lugar desconhecido.'),
    (null, 'mis001', 2, 'F', 'Ei, garota... está viva?'),
    (null, 'mis001', 2, 'M', 'Ei, garoto... está vivo?'),
    ('hbt001', 'mis001', 3, 'F', 'Silvie piscou, ainda meio zonza. Acima dela, um homem de meia-idade, com um grande chapéu de palha e expressão marcada pelo tempo, a observava atentamente.'),
    ('hbt001', 'mis001', 3, 'M', 'Shuan piscou, ainda meio zonzo. Acima dele, um homem de meia-idade, com um grande chapéu de palha e expressão marcada pelo tempo, o observava atentamente.'),
    ('hbt002', 'mis001', 5, 'F', 'Eu quem devia perguntar isso — o homem deu uma risada breve. — Você estava desmaiada bem no meio do campo. Quase te colhi junto com as abóboras!'),
    ('hbt002', 'mis001', 5, 'M', 'Eu quem devia perguntar isso — o homem deu uma risada breve. — Você estava desmaiado bem no meio do campo. Quase te colhi junto com as abóboras!'),
    ('hbt001', 'mis001', 6, 'F', 'A jovem olhou ao redor. Tudo era novo. Campos vastos se estendiam em todas as direções, dançando sob a brisa. Ela tentou puxar alguma lembrança... mas nada vinha.'),
    ('hbt001', 'mis001', 6, 'M', 'O jovem olhou ao redor. Tudo era novo. Campos vastos se estendiam em todas as direções, dançando sob a brisa. Ele tentou puxar alguma lembrança... mas nada vinha.'),
    ('hbt002', 'mis001', 8, 'F', 'Hm. Perigoso andar por aí sem memória — disse o aldeão, coçando a barba. — Mas se estiver bem, mais à frente tem uma vila. Vá até lá, talvez alguém possa te ajudar.'),
    ('hbt002', 'mis001', 8, 'M', 'Hm. Perigoso andar por aí sem memória — disse o aldeão, coçando a barba. — Mas se estiver bem, mais à frente tem uma vila. Vá até lá, talvez alguém possa te ajudar.'),
    ('hbt001', 'mis001', 9, 'F', 'Silvie assentiu, ainda atordoada, mas determinada. Pegou a pequena bolsa ao seu lado e começou a andar.'),
    ('hbt001', 'mis001', 9, 'M', 'Shuan assentiu, ainda atordoado, mas determinado. Pegou a pequena bolsa ao seu lado e começou a andar.'),
    ('hbt001', 'mis003', 1, 'F', 'Algumas horas depois, ela chegou à Vila de Borabóia, uma comunidade simples, com casas de madeira, plantações e moradores de semblante gentil.'),
    ('hbt001', 'mis003', 1, 'M', 'Algumas horas depois, ele chegou à Vila de Borabóia, uma comunidade simples, com casas de madeira, plantações e moradores de semblante gentil.'),
    (null, 'mis003', 2, 'F', 'Ora, quem é você, jovem?'),
    (null, 'mis003', 2, 'M', 'Ora, quem é você, jovem?'),
    ('rct002', null, 1, 'F', 'Silvie! Minha musa da colher de pau! Estou prestes a criar o prato mais revolucionário da história da culinária camponesa: o Omurice de Arroz! Mas... estou sem ingredientes. E sem tempo. E sem dignidade. Você me ajuda?'),
    ('rct002', null, 1, 'M', 'Shuan! Meu rei da colher de pau! Estou prestes a criar o prato mais revolucionário da história da culinária camponesa: o Omurice de Arroz! Mas... estou sem ingredientes. E sem tempo. E sem dignidade. Você me ajuda?'),
    ('rct002', 'mis007', 1, 'F', 'Antes de tudo, preciso de água do poço. Mas não qualquer água! Tem que ser aquela que brilha sob o sol das 10h e tem gosto de vitória! Ou... pelo menos que não tenha sapo dentro. Vai lá, guerreira!'),
    ('rct002', 'mis007', 1, 'M', 'Antes de tudo, preciso de água do poço. Mas não qualquer água! Tem que ser aquela que brilha sob o sol das 10h e tem gosto de vitória! Ou... pelo menos que não tenha sapo dentro. Vai lá, guerreiro!'),
    ('rct002', 'mis008', 1, 'F', 'Agora o arroz! Mas não é qualquer arroz, é o Arroz do Planalto™ — colhido com suor, lágrimas e, às vezes, picadas de formiga. Traga um punhado... ou dois... ou vinte. Vai queimar umas calorias!'),
    ('rct002', 'mis008', 1, 'M', 'Agora o arroz! Mas não é qualquer arroz, é o Arroz do Planalto™ — colhido com suor, lágrimas e, às vezes, picadas de formiga. Traga um punhado... ou dois... ou vinte. Vai queimar umas calorias!'),
    ('rct002', 'mis009', 1, 'F', 'E por fim... os ovos! Mas cuidado: as galinhas dos Campos são temperamentais. Uma vez, uma me perseguiu por meia hora. Leve um escudo. Ou um pão. Elas respeitam carboidratos.'),
    ('rct002', 'mis009', 1, 'M', 'E por fim... os ovos! Mas cuidado: as galinhas dos Campos são temperamentais. Uma vez, uma me perseguiu por meia hora. Leve um escudo. Ou um pão. Elas respeitam carboidratos.'),
    ('rct002', 'mis010', 1, 'F', 'Você conseguiu! Água cristalina, arroz digno de poesia e ovos mais frescos que fofoca de vila! Agora... silêncio! É hora da alquimia culinária suprema!'),
    ('rct002', 'mis010', 1, 'M', 'Você conseguiu! Água cristalina, arroz digno de poesia e ovos mais frescos que fofoca de vila! Agora... silêncio! É hora da alquimia culinária suprema!'),
    ('hbt001', 'mis010', 2, 'F', 'Ela gira a frigideira com dramaticidade, quase derruba tudo, mas no fim...'),
    ('hbt001', 'mis010', 2, 'M', 'Ela gira a frigideira com dramaticidade, quase derruba tudo, mas no fim...'),
    ('rct002', 'mis010', 3, 'F', '…E… ficou bom. Quase perfeito. Mas ainda não é O Omurice Supremo. Falta algo. Um toque. Um tempero místico? Uma gema de dragão? Um fio de cabelo de chef lendário?'),
    ('rct002', 'mis010', 3, 'M', '…E… ficou bom. Quase perfeito. Mas ainda não é O Omurice Supremo. Falta algo. Um toque. Um tempero místico? Uma gema de dragão? Um fio de cabelo de chef lendário?'),
    ('hbt001', 'mis010', 4, 'F', 'Ela suspira, mas sorri.'),
    ('hbt001', 'mis010', 4, 'M', 'Ela suspira, mas sorri.'),
    ('rct002', 'mis010', 5, 'F', 'Mas não tema, Silvie! A busca continua! Um dia, esse prato vai entrar para os livros de história — ou pelo menos para o cardápio da taverna.'),
    ('rct002', 'mis010', 5, 'M', 'Mas não tema, Shuan! A busca continua! Um dia, esse prato vai entrar para os livros de história — ou pelo menos para o cardápio da taverna.'),
    ('rct002', 'mis010', 6, 'F', 'Tome, Silvie. Um Omurice quase supremo. Feito com suor, lágrimas e um leve toque de frustração criativa. Coma com orgulho — e cuidado, ele ainda tá bufando de quente!'),
    ('rct002', 'mis010', 6, 'M', 'Tome, Shuan. Um Omurice quase supremo. Feito com suor, lágrimas e um leve toque de frustração criativa. Coma com orgulho — e cuidado, ele ainda tá bufando de quente!'),
    ('hbt001', 'mis010', 7, 'F', 'Ela entrega o prato com um guardanapo dobrado em forma de galinha... com uma lágrima desenhada.'),
    ('hbt001', 'mis010', 7, 'M', 'Ela entrega o prato com um guardanapo dobrado em forma de galinha... com uma lágrima desenhada.'),
    ('rct002', 'mis010', 8, 'F', 'Se isso não te der +5 de energia e +1 de esperança, eu nem sou mais Lina Panela!'),
    ('rct002', 'mis010', 8, 'M', 'Se isso não te der +5 de energia e +1 de esperança, eu nem sou mais Lina Panela!'),
    ('rct001', 'mis004', 1, 'F', 'Mamma mia! Esses corvettos tão fazendo piquenique no meu arrozal! Vai lá, bambina, e mostra pra eles que aqui não é trattoria! Vola via, cornacchia!'),
    ('rct001', 'mis004', 1, 'M', 'Mamma mia! Esses corvettos tão fazendo piquenique no meu arrozal! Vai lá, bambino, e mostra pra eles que aqui não é trattoria! Vola via, cornacchia!'),
    ('rct001', 'mis005', 1, 'F', 'A cerca tá mais aberta que o coração da minha nonna! Se não fechar logo, até o vento vai plantar tomate aqui! Anda, anda, martella com amore!'),
    ('rct001', 'mis005', 1, 'M', 'A cerca tá mais aberta que o coração da minha nonna! Se não fechar logo, até o vento vai plantar tomate aqui! Anda, anda, martella com amore!'),
    ('rct001', 'mis006', 1, 'F', 'Lupi na fazenda? Só se for pra fazer serenata! Vai lá, ragazza, e mostra que aqui quem uiva é só o rádio da cozinha!'),
    ('rct001', 'mis006', 1, 'M', 'Lupi na fazenda? Só se for pra fazer serenata! Vai lá, ragazzo, e mostra que aqui quem uiva é só o rádio da cozinha!'),
    ('hbt001', 'mis011', 1, 'F', 'Interior da casa de Tião Palha. A mesa está cheia de pratos fumegantes e moradores animados. Silvie, ainda meio desconfiada, observa tudo com olhos atentos. É sua primeira noite na vila.'),
    ('hbt001', 'mis011', 1, 'M', 'Interior da casa de Tião Palha. A mesa está cheia de pratos fumegantes e moradores animados. Shuan, ainda meio desconfiado, observa tudo com olhos atentos. É sua primeira noite na vila.'),
    ('hbt002', 'mis011', 2, 'F', '(Puxando uma cadeira para ela): — Senta aqui, moça. Primeira regra da vila: ninguém janta sozinho. Segunda regra: cuidado com a Gertrudes.'),
    ('hbt002', 'mis011', 2, 'M', '(Puxando uma cadeira para ele): — Senta aqui, moço. Primeira regra da vila: ninguém janta sozinho. Segunda regra: cuidado com a Gertrudes.'),
    ('rct002', 'mis011', 4, 'F', '(Surgindo com uma travessa): — Uma galinha. Temperamental. E com excelente memória para rostos que mexem nos ovos dela.'),
    ('rct002', 'mis011', 4, 'M', '(Surgindo com uma travessa): — Uma galinha. Temperamental. E com excelente memória para rostos que mexem nos ovos dela.'),
    ('rct001', 'mis011', 5, 'F', '(Erguendo o bigode com orgulho): — E gosto refinado! Uma vez ela bicou um crítico gastronômico. Ou talvez fosse só o padeiro... mas o ponto é: ela tem instinto!'),
    ('rct001', 'mis011', 5, 'M', '(Erguendo o bigode com orgulho): — E gosto refinado! Uma vez ela bicou um crítico gastronômico. Ou talvez fosse só o padeiro... mas o ponto é: ela tem instinto!'),
    ('rct001', 'mis011', 7, 'F', '(Ofendido de brincadeira): — Non è orégano, è tradição! Minha fazenda cheira como a infância... e um pouco como pizza.'),
    ('rct001', 'mis011', 7, 'M', '(Ofendido de brincadeira): — Non è orégano, è tradição! Minha fazenda cheira como a infância... e um pouco como pizza.'),
    ('ven001', 'mis011', 8, 'F', '(Calmo, servindo arroz): — A sabedoria está no prato simples. E no silêncio entre duas colheradas.'),
    ('ven001', 'mis011', 8, 'M', '(Calmo, servindo arroz): — A sabedoria está no prato simples. E no silêncio entre duas colheradas.'),
    ('rct002', 'mis011', 10, 'F', '(Com brilho nos olhos): — É o Omurice quase supremo! Um prato que beira a perfeição... mas sempre escapa. Como um sonho culinário com asas.'),
    ('rct002', 'mis011', 10, 'M', '(Com brilho nos olhos): — É o Omurice quase supremo! Um prato que beira a perfeição... mas sempre escapa. Como um sonho culinário com asas.'),
    ('hbt002', 'mis011', 11, 'F', '(Rindo): — Ou como a Silvie tentando entender o que tá acontecendo desde que chegou.'),
    ('hbt002', 'mis011', 11, 'M', '(Rindo): — Ou como o Shuan tentando entender o que tá acontecendo desde que chegou.'),
    ('hbt001', 'mis011', 13, 'F', 'Nesse momento, Gertrudes entra pela porta e encara Silvie.'),
    ('hbt001', 'mis011', 13, 'M', 'Nesse momento, Gertrudes entra pela porta e encara Shuan.'),
    ('rct002', 'mis011', 15, 'F', '(Gritando): — Oferece pão! Elas respeitam carboidrato!'),
    ('rct002', 'mis011', 15, 'M', '(Gritando): — Oferece pão! Elas respeitam carboidrato!'),
    ('ven001', 'mis011', 16, 'F', '(Entregando um pedaço de pão): — A paz começa com fermento.'),
    ('ven001', 'mis011', 16, 'M', '(Entregando um pedaço de pão): — A paz começa com fermento.'),
    ('hbt001', 'mis011', 18, 'F', 'A galinha aceita o pão e sai com dignidade. Todos aplaudem discretamente.'),
    ('hbt001', 'mis011', 18, 'M', 'A galinha aceita o pão e sai com dignidade. Todos aplaudem discretamente.'),
    ('rct001', 'mis011', 19, 'F', '(Erguendo um copo): — Um brinde à nova viajante! Que sua estadia seja leve, sua comida quente e suas galinhas... diplomáticas!'),
    ('rct001', 'mis011', 19, 'M', '(Erguendo um copo): — Um brinde ao novo viajante! Que sua estadia seja leve, sua comida quente e suas galinhas... diplomáticas!'),
    ('hbt001', 'mis011', 20, 'F', '(Todos): — Viva!'),
    ('hbt001', 'mis011', 20, 'M', '(Todos): — Viva!'),
    ('hbt001', 'mis011', 21, 'F', 'Mais tarde naquela noite'),
    ('hbt001', 'mis011', 21, 'M', 'Mais tarde naquela noite'),
    ('ven001', 'mis011', 22, 'F', 'Ultimamente, uma fera tem aparecido. Grande como um touro, rápida como um raio. Anda destruindo plantações e espantando os trabalhadores.'),
    ('ven001', 'mis011', 22, 'M', 'Ultimamente, uma fera tem aparecido. Grande como um touro, rápida como um raio. Anda destruindo plantações e espantando os trabalhadores.'),
    ('rct001', 'mis011', 24, 'F', 'Já tentaram espantar, mas voltaram com mais medo que gato em dia de banho! Eu te digo, ragazza... essa criatura não tá ali por acaso. Tá guardando alguma coisa, capisce?'),
    ('rct001', 'mis011', 24, 'M', 'Já tentaram espantar, mas voltaram com mais medo que gato em dia de banho! Eu te digo, ragazzo... essa criatura não tá ali por acaso. Tá guardando alguma coisa, capisce?'),
    ('hbt001', 'mis011', 25, 'F', 'A jovem ficou em silêncio por um momento. Depois, se levantou, encarando os aldeões.'),
    ('hbt001', 'mis011', 25, 'M', 'O jovem ficou em silêncio por um momento. Depois, se levantou, encarando os aldeões.'),
    ('hbt001', 'mis011', 27, 'F', 'No dia seguinte, ela partiu com as instruções dos moradores.'),
    ('hbt001', 'mis011', 27, 'M', 'No dia seguinte, ele partiu com as instruções dos moradores.'),
    ('hbt001', 'mis012', 1, 'F', 'De volta à vila, os moradores a receberam com aplausos e sorrisos.'),
    ('hbt001', 'mis012', 1, 'M', 'De volta à vila, os moradores o receberam com aplausos e sorrisos.'),
    ('hbt002', 'mis012', 2, 'F', 'Você... conseguiu mesmo!'),
    ('hbt002', 'mis012', 2, 'M', 'Você... conseguiu mesmo!'),
    ('hbt001', 'mis012', 4, 'F', 'Os moradores ofereceram comida, abrigo, até joias antigas como recompensa. Mas Silvie recusou com um sorriso gentil.'),
    ('hbt001', 'mis012', 4, 'M', 'Os moradores ofereceram comida, abrigo, até joias antigas como recompensa. Mas Shuan recusou com um sorriso gentil.'),
    ('hbt003', 'mis012', 6, 'F', 'Hmm... ninguém com a sua descrição passou por aqui. Mas dizem que na Cidade de Lurien, em uma ilha próxima, há mais movimento. Talvez encontre pistas por lá.'),
    ('hbt003', 'mis012', 6, 'M', 'Hmm... ninguém com a sua descrição passou por aqui. Mas dizem que na Cidade de Lurien, em uma ilha próxima, há mais movimento. Talvez encontre pistas por lá.'),
    ('hbt001', 'mis012', 8, 'F', 'O aldeão de chapéu de palha deu uma risada curta.'),
    ('hbt001', 'mis012', 8, 'M', 'O aldeão de chapéu de palha deu uma risada curta.'),
    ('hbt002', 'mis012', 9, 'F', 'Tenho uma canoa velha. Não vai ganhar nenhuma corrida, mas vai te levar até lá.'),
    ('hbt002', 'mis012', 9, 'M', 'Tenho uma canoa velha. Não vai ganhar nenhuma corrida, mas vai te levar até lá.');
