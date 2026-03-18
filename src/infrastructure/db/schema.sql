-- Paciente
CREATE TABLE IF NOT EXISTS paciente (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  nome       TEXT NOT NULL,
  email      TEXT NOT NULL UNIQUE,
  senha      TEXT NOT NULL,
  criado_em   TEXT NOT NULL DEFAULT (datetime('now'))
);
-- Histórico
CREATE TABLE IF NOT EXISTS historico (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  paciente_id    INTEGER NOT NULL, 
  titulo         TEXT NOT NULL,    
  descricao      TEXT,             
  arquivado      INTEGER NOT NULL DEFAULT 0, 
  criado_em      TEXT NOT NULL DEFAULT (datetime('now')),
  
  FOREIGN KEY (paciente_id) REFERENCES paciente(id)
);
-- Token de acesso
CREATE TABLE IF NOT EXISTS token (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  historico_id  INTEGER NOT NULL,
  valor         TEXT NOT NULL UNIQUE,
  criado_em     TEXT NOT NULL DEFAULT (datetime('now')),
  expira_em     TEXT NOT NULL,
  revogado      INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (historico_id) REFERENCES historico(id)
);
-- registro (append-only)
CREATE TABLE IF NOT EXISTS registro (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  historico_id   INTEGER NOT NULL,
  autor_tipo     TEXT NOT NULL CHECK (autor_tipo IN ('medico','paciente')),
  autor_nome     TEXT NOT NULL,
  autor_crm      TEXT,
  tipo           TEXT NOT NULL CHECK (tipo IN ('diagnostico','conduta','informacao','sintoma')),
  conteudo       TEXT NOT NULL,
  visivel        INTEGER NOT NULL DEFAULT 1,
  criado_em      TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (historico_id) REFERENCES historico(id)
);
-- Arquivo
CREATE TABLE IF NOT EXISTS arquivo (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  historico_id   INTEGER NOT NULL,
  enviado_por    TEXT NOT NULL CHECK (enviado_por IN ('medico','paciente')),
  tipo           TEXT NOT NULL CHECK (tipo IN ('exame','laudo','documento')),
  nome_original  TEXT NOT NULL,
  url            TEXT NOT NULL,
  descricao      TEXT,
  visivel        INTEGER NOT NULL DEFAULT 1,
  criado_em      TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (historico_id) REFERENCES historico(id)
);