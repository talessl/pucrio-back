-- Paciente de teste (ID 1)
INSERT OR IGNORE INTO paciente (id, nome, email, senha) 
VALUES (1, 'Fernando Solimões', 'paciente@teste.com', 'scrypt:32768:8:1$VbFNgAXIRceOw14b$5018560a6f8b8aa309076caf1102fa83a3f72ead49e75b3dbeed6458b273b7d63e782668850b14a6b729dcec438d1167e3f87a01fe4d3caf130e4800affdb6b9');

-- Históricos
INSERT OR IGNORE INTO historico (id, paciente_id, titulo, descricao, arquivado) VALUES 
  (1, 1, 'Acompanhamento Geral', 'Consultas de rotina e checkups anuais', 0),
  (2, 1, 'Tratamento Dermatológico', 'Acompanhamento de alergia na pele com Roacutan', 0),
  (3, 1, 'Cirurgia do Joelho (2025)', 'Registros do pós-operatório (Finalizado)', 0);

-- Registros — Histórico 1 (Acompanhamento Geral)
INSERT OR IGNORE INTO registro (id, historico_id, autor_tipo, autor_nome, autor_crm, tipo, conteudo) VALUES
  (1, 1, 'medico',   'Dr. Carlos Mendes',  'CRM123456/SP', 'diagnostico', 'Hipertensão arterial leve. PA: 140x90 mmHg.'),
  (2, 1, 'medico',   'Dr. Carlos Mendes',  'CRM123456/SP', 'conduta',     'Prescrito Losartana 50mg, 1x ao dia. Reavaliar em 30 dias.'),
  (3, 1, 'paciente', 'Fernando Solimões',  NULL,           'sintoma',     'Relata dores de cabeça frequentes, especialmente à tarde.'),
  (4, 1, 'medico',   'Dr. Carlos Mendes',  'CRM123456/SP', 'informacao',  'Exames laboratoriais dentro da normalidade. Colesterol total: 190 mg/dL.'),
  (5, 1, 'paciente', 'Fernando Solimões',  NULL,           'sintoma',     'Cansaço excessivo ao subir escadas nos últimos 15 dias.');

-- Registros — Histórico 2 (Tratamento Dermatológico)
INSERT OR IGNORE INTO registro (id, historico_id, autor_tipo, autor_nome, autor_crm, tipo, conteudo) VALUES
  (6,  2, 'medico',   'Dra. Beatriz Lima',  'CRM987654/RJ', 'diagnostico', 'Acne grau III com lesões inflamatórias no rosto e costas.'),
  (7,  2, 'medico',   'Dra. Beatriz Lima',  'CRM987654/RJ', 'conduta',     'Iniciado Isotretinoína (Roacutan) 20mg/dia. Retorno em 45 dias.'),
  (8,  2, 'paciente', 'Fernando Solimões',  NULL,           'sintoma',     'Pele ressecada nos lábios e descamação leve no rosto após 2 semanas de uso.'),
  (9,  2, 'medico',   'Dra. Beatriz Lima',  'CRM987654/RJ', 'conduta',     'Orientado uso de hidratante facial sem óleo e protetor solar diário.'),
  (10, 2, 'medico',   'Dra. Beatriz Lima',  'CRM987654/RJ', 'informacao',  'Melhora significativa após 60 dias. Redução de 70% das lesões ativas.');

-- Registros — Histórico 3 (Cirurgia do Joelho)
INSERT OR IGNORE INTO registro (id, historico_id, autor_tipo, autor_nome, autor_crm, tipo, conteudo) VALUES
  (11, 3, 'medico',   'Dr. Rafael Souza',   'CRM456789/MG', 'diagnostico', 'Ruptura parcial do ligamento cruzado anterior (LCA) joelho direito.'),
  (12, 3, 'medico',   'Dr. Rafael Souza',   'CRM456789/MG', 'conduta',     'Realizada artroscopia com reconstrução do LCA. Procedimento sem intercorrências.'),
  (13, 3, 'paciente', 'Fernando Solimões',  NULL,           'sintoma',     'Dor moderada e edema no joelho no 3º dia de pós-operatório.'),
  (14, 3, 'medico',   'Dr. Rafael Souza',   'CRM456789/MG', 'conduta',     'Fisioterapia iniciada no 7º dia. Protocolo de 3 sessões semanais por 3 meses.'),
  (15, 3, 'medico',   'Dr. Rafael Souza',   'CRM456789/MG', 'informacao',  'Alta médica após 90 dias. Amplitude de movimento completa restaurada.');

-- Tokens
INSERT OR IGNORE INTO token (id, historico_id, valor, descricao, expira_em) VALUES
  (1, 1, 'tok_abc123xyz456def789', 'Dr. Antonio Farias',  datetime('now', '+48 hours')),
  (2, 2, 'tok_bcd234yza567efg890', 'Dra. Camila Torres',  datetime('now', '+24 hours')),
  (3, 1, 'tok_cde345zab678fgh901', 'Dr. Marcos Oliveira', datetime('now', '-1 hours')),
  (4, 3, 'tok_def456abc789ghi012', 'Dra. Lucia Ferreira', datetime('now', '+72 hours'));

-- Arquivos — Histórico 1
INSERT OR IGNORE INTO arquivo (id, historico_id, enviado_por, tipo, nome_original, url, descricao) VALUES
  (1, 1, 'medico',   'exame',     'hemograma_completo.jpg',   'assets/uploads/hemograma_completo.jpg',   'Hemograma completo — Jan 2025'),
  (2, 1, 'paciente', 'documento', 'cartao_convenio.pdf',      'assets/uploads/cartao_convenio.pdf',      'Cartão do convênio médico');

-- Arquivos — Histórico 2
INSERT OR IGNORE INTO arquivo (id, historico_id, enviado_por, tipo, nome_original, url, descricao) VALUES
  (4, 2, 'medico',   'laudo',     'laudo_dermato.png',        'assets/uploads/laudo_dermato.png',        'Laudo dermatológico inicial'),
  (5, 2, 'paciente', 'exame',     'foto_evolucao_pele.jpg',   'assets/uploads/foto_evolucao_pele.jpg',   'Foto evolução tratamento — 30 dias'),
  (6, 2, 'medico',   'documento', 'receita_roacutan.jpg',     'assets/uploads/receita_roacutan.jpg',     'Receita controlada Roacutan');

-- Arquivos — Histórico 3
INSERT OR IGNORE INTO arquivo (id, historico_id, enviado_por, tipo, nome_original, url, descricao) VALUES
  (8, 3, 'medico',   'laudo',     'laudo_cirurgia.png',       'assets/uploads/laudo_cirurgia.png',       'Relatório cirúrgico'),
  (9, 3, 'paciente', 'documento', 'autorizacao_plano.png',    'assets/uploads/autorizacao_plano.png',    'Autorização do plano de saúde');