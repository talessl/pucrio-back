-- Paciente de teste (ID 1)
INSERT OR IGNORE INTO paciente (id, nome, email, senha) 
VALUES (1, 'Fernando Solimões', 'paciente@teste.com', 'scrypt:32768:8:1$VbFNgAXIRceOw14b$5018560a6f8b8aa309076caf1102fa83a3f72ead49e75b3dbeed6458b273b7d63e782668850b14a6b729dcec438d1167e3f87a01fe4d3caf130e4800affdb6b9');

-- Históricos (IDs 1, 2 e 3)
INSERT OR IGNORE INTO historico (id, paciente_id, titulo, descricao, arquivado) 
VALUES 
  (1, 1, 'Acompanhamento Geral', 'Consultas de rotina e checkups anuais', 0),
  (2, 1, 'Tratamento Dermatológico', 'Acompanhamento de alergia na pele com Roacutan', 0),
  (3, 1, 'Cirurgia do Joelho (2025)', 'Registros do pós-operatório (Finalizado)', 1);

-- Alguns registros (IDs 1, 2 e 3)
INSERT OR IGNORE INTO registro (id, historico_id, autor_tipo, autor_nome, autor_crm, tipo, conteudo)
VALUES (1, 1, 'medico', 'Dr. Carlos', 'CRM12345', 'diagnostico', 'Hipertensão leve.');

INSERT OR IGNORE INTO registro (id, historico_id, autor_tipo, autor_nome, autor_crm, tipo, conteudo)
VALUES (2, 1, 'medico', 'Dr. Carlos', 'CRM12345', 'conduta', 'Losartana 50mg, 1x ao dia.');

-- Corrigido o erro de digitação de "sOR IGNORE intoma" para "sintoma" e a coluna duplicada
INSERT OR IGNORE INTO registro (id, historico_id, autor_tipo, autor_nome, autor_crm, tipo, conteudo)
VALUES (3, 1, 'paciente', 'João Silva', NULL, 'sintoma', 'Dor de cabeça frequente.');

-- Token ativo (ID 1)
INSERT OR IGNORE INTO token (id, historico_id, valor, descricao, expira_em)
VALUES (1, 1, 'tok_abc123xyz456def789', 'Dr. Antonio', datetime('now', '+48 hours'));