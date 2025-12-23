#1. Vytvoření schématu pro data s dopravními nehodami ČR
/*
CREATE SCHEMA dopravni_nehody_cr;
/*

#2. Vytvoření tabulek a přiřazení datových typů sloupců. 
    -- Datové typy byly určeny na základě dokumentace
/* CREATE TABLE dopravni_nehody_cr.chodci (p1 VARCHAR (255),
                                        p29 VARCHAR,
                                        p29a VARCHAR,
                                        p29b VARCHAR,
                                        p30 VARCHAR,
                                        p30a VARCHAR,
                                        p30b VARCHAR,
                                        p31 VARCHAR,
                                        p32 VARCHAR,
                                        p33c VARCHAR,
                                        p33d VARCHAR,
                                        p33e VARCHAR,
                                        p33f VARCHAR,
                                        p33g VARCHAR
);

CREATE TABLE dopravni_nehody_cr.nasledky (p1 VARCHAR (255),
                                          id_vozidla VARCHAR,
                                          p59a VARCHAR,
                                          p59b VARCHAR,
                                          p59c VARCHAR,
                                          p59d INT,
                                          p59e VARCHAR,
                                          p59f VARCHAR,
                                          p59g VARCHAR
);

CREATE TABLE dopravni_nehody_cr.gps (p1 VARCHAR (255),
                                     d INT,
                                     e INT,
                                     h VARCHAR,
                                     i VARCHAR,
                                     j INT,
                                     k VARCHAR
);

CREATE TABLE dopravni_nehody_cr.vozidla (p1 VARCHAR (255),
                                         id_vozidla VARCHAR,
                                         p44 VARCHAR,
                                         p45a VARCHAR,
                                         p45b INT,
                                         p45d VARCHAR,
                                         p45f VARCHAR,
                                         p47 VARCHAR,
                                         p48a VARCHAR,
                                         p48b VARCHAR,
                                         p49 VARCHAR,
                                         p50a VARCHAR,
                                         p50b VARCHAR,
                                         p51 VARCHAR,
                                         p52 VARCHAR,
                                         p53 VARCHAR,
                                         p55a VARCHAR,
                                         p55b VARCHAR,
                                         p56 VARCHAR,
                                         p57 VARCHAR,
                                         p58 VARCHAR
); 

CREATE TABLE dopravni_nehody_cr.column_names (code VARCHAR, 
                                              descr VARCHAR, 
                                              name_column_en VARCHAR, 
                                              table_name VARCHAR);
CREATE TABLE dopravni_nehody_cr.data_description(column_code VARCHAR,
                                                 id_detail VARCHAR, 
                                                 description_detail VARCHAR, 
                                                 description_detail_2 VARCHAR, 
                                                 EN VARCHAR);

*/

#3. Převedení souborů XLS na XLSX
#4. Import dat ze souborů XLSX do tabulek v databázi PostgreSQL
#5. Přidání komentáře ke všem sloupcům
--CHODCI
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p1 IS 'identifikační číslo nehody';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p29 IS 'kategorie chodce';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p29a IS 'reflexní prvky u chodce';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p29b IS 'chodec na osobním přepravníku';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p30 IS 'stav chodce';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p30a IS 'alkohol u chodce přítomen';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p30b IS 'druh drogy u chodce';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p31 IS 'chování chodce';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p32 IS 'situace v místě nehody';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p33c IS 'pohlaví zraněné osoby';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p33d IS 'věk zraněného chodce';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p33e IS 'státní příslušnost (stát) zraněného';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p33f IS 'poskytnutí první pomoci zraněnému';
COMMENT ON COLUMN dopravni_nehody_cr.chodci.p33g IS 'následky na zraněném';
--NASLEDKY
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.p1 IS 'identifikační číslo nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.id_vozidla IS 'identifikační číslo vozidla u nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.p59a IS 'označení osoby';
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.p59b IS 'bližší označení osoby';
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.p59c IS 'pohlaví osoby';
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.p59d IS 'věk osoby';
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.p59e IS 'státní příslušnost (stát)';
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.p59f IS 'poskytnutí první pomoci';
COMMENT ON COLUMN dopravni_nehody_cr.nasledky.p59g IS 'následky';
--NEHODY
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p1 IS 'identifikační číslo nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p2a IS 'den, měsíc, rok';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p2b IS 'čas ';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p4a IS 'kraj';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p4b IS 'okres';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p4c IS 'útvar';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p5a IS 'lokalita nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p6 IS 'druh nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p7 IS 'druh srážky jedoucích vozidel';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p8 IS 'druh pevné překážky';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p8a IS 'druh zvěře / zvířete';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p9 IS 'charakter nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p10 IS 'zavinění nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p11 IS 'alkohol u viníka nehody přítomen';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p11a IS 'drogy u viníka nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p12 IS 'hlavní příčiny nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p13a IS 'usmrceno osob';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p13b IS 'těžce zraněno osob';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p13c IS 'lehce zraněno osob';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p14 IS 'celková hmotná škoda v kč';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p15 IS 'druh povrchu vozovky';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p16 IS 'stav povrchu vozovky v době nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p17 IS 'stav komunikace';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p18 IS 'povětrnostní podmínky v době nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p19 IS 'viditelnost';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p20 IS 'rozhledové poměry';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p21 IS 'dělení komunikace';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p22 IS 'situování nehody na komunikaci';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p23 IS 'řízení provozu v době nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p24 IS 'místní úprava přednosti v jízdě';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p27 IS 'specifická místa a objekty v místě nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p28 IS 'směrové poměry';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p34 IS 'počet zúčastněných vozidel';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p35 IS 'místo dopravní nehody';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p36 IS 'druh pozemní komunikace';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p37 IS 'číslo pozemní komunikace';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p38 IS 'CHYBÍ DOKUMENTACE';
COMMENT ON COLUMN dopravni_nehody_cr.nehody.p39 IS 'druh křižující komunikace';
--GPS
COMMENT ON COLUMN dopravni_nehody_cr.gps.p1 IS 'identifikační číslo nehody';
COMMENT ON COLUMN dopravni_nehody_cr.gps.d IS 'souřadnice x';
COMMENT ON COLUMN dopravni_nehody_cr.gps.e IS 'souřadnice y';
COMMENT ON COLUMN dopravni_nehody_cr.gps.h IS 'město';
COMMENT ON COLUMN dopravni_nehody_cr.gps.i IS 'ulice';
COMMENT ON COLUMN dopravni_nehody_cr.gps.j IS 'číslo popisné';
COMMENT ON COLUMN dopravni_nehody_cr.gps.k IS 'typ komunikace';
--VOZIDLA
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p1 IS 'identifikační číslo nehody';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.id_vozidla IS 'identifikační číslo vozidla u nehody';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p44 IS 'druh vozidla';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p45a IS 'výrobní značka motorového vozidla';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p45b IS 'údaje o vozidle';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p45d IS 'druh pohonu / paliva';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p45f IS 'druh pneumatik na vozidle';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p47 IS 'rok výroby vozidla';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p48a IS 'charakteristika vozidla';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p48b IS 'CHYBÍ DOKUMENTACE';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p49 IS 'smyk';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p50a IS 'vozidlo po nehodě';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p50b IS 'únik provozních, přepravovaných hmot';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p51 IS 'způsob vyproštění osob z vozidla';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p52 IS 'směr jízdy nebo postavení vozidla';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p53 IS 'škoda na vozidle';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p55a IS 'kategorie řidiče';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p55b IS 'CHYBÍ DOKUMENTACE';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p56 IS 'CHYBÍ DOKUMENTACE';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p57 IS 'stav řidiče';
COMMENT ON COLUMN dopravni_nehody_cr.vozidla.p58 IS 'vnější ovlivnění řidiče';

#6. Přidání primárního klíče na nehody 'p1'
    -- Byla odstraněna duplicitní hodnota '161425000002' v tabulce nehody před přidáním primárního klíče (zvolila jsem hodnotu z 2025 protože data z 2025 nejsou v momentě tvorby této databáze kompletní 21.12.2025)

DELETE FROM dopravni_nehody_cr.nehody
WHERE p1 = '161425000002' AND p8 = '6';

ALTER TABLE dopravni_nehody_cr.nehody
ADD CONSTRAINT pk_nehody_p1 PRIMARY KEY (p1);

ALTER TABLE dopravni_nehody_cr.column_names
ADD CONSTRAINT pk_column_code PRIMARY KEY (code);


#7. Přidání cizích klíčů
ALTER TABLE dopravni_nehody_cr.chodci
ADD CONSTRAINT fk_chodci_p1 FOREIGN KEY (p1)
REFERENCES dopravni_nehody_cr.nehody (p1);

ALTER TABLE dopravni_nehody_cr.gps
ADD CONSTRAINT fk_gps_p1 FOREIGN KEY (p1)
REFERENCES dopravni_nehody_cr.nehody (p1);

ALTER TABLE dopravni_nehody_cr.nasledky
ADD CONSTRAINT fk_nasledky_p1 FOREIGN KEY (p1)
REFERENCES dopravni_nehody_cr.nehody (p1);

ALTER TABLE dopravni_nehody_cr.vozidla
ADD CONSTRAINT fk_vozidla_p1 FOREIGN KEY (p1)
REFERENCES dopravni_nehody_cr.nehody (p1);

ALTER TABLE dopravni_nehody_cr.data_description
ADD CONSTRAINT fk_column_code FOREIGN KEY (column_code)
REFERENCES dopravni_nehody_cr.column_names (code);

#8. Vytvoření indexů pro zrychlení dotazů
CREATE INDEX CONCURRENTLY idx_chodci_p1 ON dopravni_nehody_cr.chodci (p1);
CREATE INDEX CONCURRENTLY idx_gps_p1 ON dopravni_nehody_cr.gps (p1);
CREATE INDEX CONCURRENTLY idx_nasledky_vozidla_p1 ON dopravni_nehody_cr.nasledky (p1, id_vozidla);
CREATE INDEX CONCURRENTLY idx_vozidla_p1 ON dopravni_nehody_cr.vozidla (p1, id_vozidla);
CREATE INDEX CONCURRENTLY idx_columns_description ON dopravni_nehody_cr.data_description (column_code, id_detail);

#9. Oprava datumů a času
-- Změna formátu data v tabulce nehody. Formát se při nahrátí konvertoval a k datu se automativky přidal časový udaj.
-- Změna formátu  času v tabulce nehody.
-- Hodnota 2560 neodpovídá reálnému času - jde pravděpodobně o chybějící data a v celé tabulce jich chybí 15%
ALTER TABLE dopravni_nehody_cr.nehody
ALTER COLUMN p2b TYPE VARCHAR USING CASE 
                                        WHEN p2b = '2560' THEN NULL
                                        WHEN length(p2b) = 4 THEN SUBSTRING(p2b FROM 1 FOR 2) || ':' || SUBSTRING(p2b FROM 3 FOR 2)
                                        WHEN length(p2b) = 3 THEN '0' || SUBSTRING(p2b FROM 1 FOR 1) || ':' || SUBSTRING(p2b FROM 2 FOR 2)
                                        WHEN length(p2b) = 2 THEN '00:' || p2b
                                        WHEN length(p2b) = 1 THEN '00:0' || p2b  
                                        ELSE NULL  
                                        END;


SELECT p2b, 
       COUNT(*) AS casove_hodnoty,
       100.0 * COUNT(*)/SUM(COUNT(*)) OVER() AS procentualní_zastoupení
FROM dopravni_nehody_cr.nehody
GROUP BY p2b
ORDER BY procentualní_zastoupení DESC;

--kontrola prázdných hodnot proběhne v pythonu

#10 Vytvoření viws
--Koncentrace nehod v čase
CREATE OR REPLACE VIEW accidents_in_time AS 
    SELECT n.p1, 
           p2a,
           p2b, 
           d,
           e,
           p5a, 
           p6, 
           p9, 
           p13a, 
           p13b, 
           p13c, 
           p14, 
           p34,
           p36
    FROM dopravni_nehody_cr.nehody AS n
    LEFT JOIN dopravni_nehody_cr.gps ON gps.p1 = n.p1


--Nehody s účastí chodců, stav chodce, dle zavinění, nejčastější příčiny zavinění
CREATE OR REPLACE VIEW pedestrian_involvement AS
    SELECT c.p1,
           p2a,
           p2b,
           d,
           e,
           p5a,
           p29,
           p29a,
           p29b,
           p30,
           p30a,
           p30b,
           p31,
           p32,
           p33c,
           p33d,
           p33f,
           p33g,
           p10,
           p11,
           p11a,
           p12,
           p13a,
           p13b,
           p13c,
           p17,
           p18,
           p27,
           p34
    FROM dopravni_nehody_cr.chodci as c
    LEFT JOIN dopravni_nehody_cr.nehody as n ON n.p1 = c.p1
    LEFT JOIN dopravni_nehody_cr.gps ON gps.p1 = c.p1

--Nehody s účastí zvěře
CREATE OR REPLACE VIEW animal_involvement AS 
SELECT n.p1,
       p2a,
       p2b,
       d,
       e,
       p4a,
       p5a,
       p8a,
       p9,
       p10,
       p11,
       p11a,
       p13a,
       p13b,
       p13c,
       p14,
       p18,
       p20,
       p21,
       p28,
       p34,
       p36,
       p59a,
       p59b,
       p59c,
       p59d,
       p59g
FROM dopravni_nehody_cr.nehody as n
LEFT JOIN dopravni_nehody_cr.nasledky as ns ON ns.p1 = n.p1
LEFT JOIN dopravni_nehody_cr.gps ON gps.p1 = n.p1
WHERE p6 = '5' OR p6 = '6'

--Analýza srážek a havárií
CREATE OR REPLACE VIEW accidents_crash AS 
    SELECT n.p1,
           p2a,
           p4a,
           p4b,
           d,
           e,
           h,
           p5a,
           p8,
           p9,
           p10,
           p11,
           p11a,
           p12,
           p13a,
           p13b,
           p13c,
           p14,
           p15,
           p16,
           p17,
           p18,
           p19,
           p20,
           p21,
           p22,
           p24,
           p27,
           p28,
           p33c,
           p33g,
           p34,
           p36,
           p44,
           p45a,
           p45d,
           p45f,
           p48a,
           p49,
           p50a,
           p51,
           p55a,
           p57,
           p58,
           p59a,
           p59g
    FROM dopravni_nehody_cr.nehody as n
    LEFT JOIN dopravni_nehody_cr.chodci as ch ON ch.p1 = n.p1
    LEFT JOIN dopravni_nehody_cr.vozidla as v ON v.p1 = n.p1
    LEFT JOIN dopravni_nehody_cr.nasledky as ns ON ns.p1 = n.p1 AND ns.id_vozidla = v.id_vozidla
    LEFT JOIN dopravni_nehody_cr.gps ON gps.p1 = n.p1;

--Analýza poskytování první pomoci
CREATE OR REPLACE VIEW first_aid AS
    SELECT n.p1,
           p5a,
           p6,
           p13a,
           p13b,
           p13c,
           p21,
           p33c,
           p33d,
           p33g,
           p33f,
           p59a,
           p59c,
           p59d,
           p59g,
           p59f
    FROM dopravni_nehody_cr.nehody as n
    LEFT JOIN dopravni_nehody_cr.chodci as c ON c.p1 = n.p1
    LEFT JOIN dopravni_nehody_cr.nasledky as ns ON ns.p1 = n.p1

--Analýza řidučů 

CREATE OR REPLACE VIEW drivers AS
    SELECT v.p1,
           v.id_vozidla,
           p6,
           p10,
           p34,
           p44,
           p45a,
           p45d,
           p48a,
           p51,
           p53,
           p55a,
           p57,
           p58,
           p59a,
           p59c,
           p59d,
           p59g,
           p13a,
           p16,
           p17,
           p18
    FROM dopravni_nehody_cr.nehody as n
    JOIN dopravni_nehody_cr.vozidla as v ON v.p1 = n.p1
    LEFT JOIN dopravni_nehody_cr.nasledky as ns ON ns.p1 = v.p1 AND ns.id_vozidla = v.id_vozidla
    WHERE p59a = '1';

