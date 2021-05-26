--------------------------------------------------------
-- Miscelaneous data to be inserted at database creation
--------------------------------------------------------

INSERT INTO config_t(section, property, value) 
VALUES ( 'global', 'language', 'en');

INSERT INTO config_t(section, property, value) 
VALUES ( 'database', 'version', '01');

-- Per-table SQL Debugging
INSERT INTO config_t(section, property, value) 
VALUES ( 'tables', 'config_t', 'info');
