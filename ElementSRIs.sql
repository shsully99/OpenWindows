BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "ElementSRIs" (
	"UniqueID"	INTEGER,
	"ElementType"	TEXT,
	"Description"	TEXT,
	"Reference"	TEXT,
	"Metric"	TEXT,
	"Octave"	TEXT,
	"Spectra"	TEXT,
	"OpenArea"	INTEGER
);
INSERT INTO "ElementSRIs" VALUES (2,'Glazing','6mm single glazing','BRE','Rw','Octave','0-20-24-31-35-27-27;',0);
INSERT INTO "ElementSRIs" VALUES (9,'Glazing','Pilkington Insulight 6/12/6.4 PVB (Rw = 34 dB)','Pilkington','Rw',NULL,'0-21-20-31-39-37-37;',0);
INSERT INTO "ElementSRIs" VALUES (10,'Roof','6/12/14 glazing','BRE','Rw',NULL,'0-23-22-30-36-37-37;',0);
INSERT INTO "ElementSRIs" VALUES (11,'Roof','10mm single glazing','BRE','Rw',NULL,'0-26-27-34-35-36-36;',0);
INSERT INTO "ElementSRIs" VALUES (12,'Roof','Double glazing - 7/16/6','Insul','Rw',NULL,'0-19-21-38-45-45-45;',0);
INSERT INTO "ElementSRIs" VALUES (13,'Roof','Pilkington Insulight 10/12/4 (Rw = 36 dB)','Pilkington','Rw',NULL,'0-25-22-33-40-43-43;',0);
INSERT INTO "ElementSRIs" VALUES (14,'Roof','Pilkington Insulight 10/12/6 (Rw = 38 dB)','Pilkington','Rw',NULL,'0-26-27-34-40-38-38;',0);
INSERT INTO "ElementSRIs" VALUES (15,'Roof','10/12/6 double glazing','BRE','Rw',NULL,'0-26-27-34-40-38-38;',0);
INSERT INTO "ElementSRIs" VALUES (16,'Roof','Upgraded windows 6/8/4/50/10','Insul','Rw',NULL,'13-13-33-39-43-49-49;',0);
INSERT INTO "ElementSRIs" VALUES (17,'Roof','Pilkington Insulight 10/12/6.4 PVB (Rw = 40 dB)','Pilkington','Rw',NULL,'0-27-29-36-41-42-42;',0);
INSERT INTO "ElementSRIs" VALUES (18,'Roof','10/200/6 double window','BRE','Rw',NULL,'0-35-46-47-48-35-35;',0);
INSERT INTO "ElementSRIs" VALUES (19,'Roof','Pilkington Optiphon 6/16/8.8 (Rw = 41 dB)','Pilkington','Rw',NULL,'0-25-27-38-48-47-47;',0);
INSERT INTO "ElementSRIs" VALUES (20,'Roof','6/100/4 or 6/100/6 double window','BRE','Rw',NULL,'0-26-34-44-44-38-38;',0);
INSERT INTO "ElementSRIs" VALUES (21,'Roof','Upgraded windows 6/8/4/100/10','Insul','Rw',NULL,'8-25-35-40-44-49-49;',0);
INSERT INTO "ElementSRIs" VALUES (22,'Roof','Pilkington Optiphon 10/20/8.8 (Rw = 46 dB)','Pilkington','Rw',NULL,'0-28-36-43-47-49-49;',0);
INSERT INTO "ElementSRIs" VALUES (23,'Roof','Upgraded windows 6/8/4/200/12','Insul','Rw',NULL,'9-29-37-41-44-50-50;',0);
INSERT INTO "ElementSRIs" VALUES (24,'Roof','Upgraded windows 6/8/4/22/15','Insul','Rw',NULL,'14-30-38-41-45-52-52;',0);
INSERT INTO "ElementSRIs" VALUES (25,'Roof','Pilkington Optiphon 8.8/16/12.8 (Rw = 48 dB)','Pilkington','Rw',NULL,'0-28-36-45-53-56-56;',0);
INSERT INTO "ElementSRIs" VALUES (26,'Roof','6/150/4 double window','BRE','Rw',NULL,'0-29-35-45-56-52-52;',0);
INSERT INTO "ElementSRIs" VALUES (27,'Roof','Glazing upgraded to external wall','Insul','Rw',NULL,'25-43-57-68-76-70-70;',0);
INSERT INTO "ElementSRIs" VALUES (28,'Roof','Current Windows','Insul','Rw',NULL,'21-24-21-31-40-43-43;',0);
INSERT INTO "ElementSRIs" VALUES (29,'Roof','Pilkington Optiphon 6/16/6.8 (Rw = 40 dB)','Pilkington','Rw',NULL,'0-21-28-37-48-48-48;',0);
INSERT INTO "ElementSRIs" VALUES (30,'Roof','Pilkington Optiphon 8/16/8.8 (Rw = 42 dB)','Pilkington','Rw',NULL,'0-21-30-39-47-50-50;',0);
INSERT INTO "ElementSRIs" VALUES (31,'Roof','Pilkington Optiphon 10/16/8.8 (Rw = 44 dB)','Pilkington','Rw',NULL,'0-28-31-42-45-50-50;',0);
INSERT INTO "ElementSRIs" VALUES (32,'Roof','Pilkington Optiphon 10.8/24/16.8 (Rw = 52 dB)','Pilkington','Rw',NULL,'0-35-41-48-53-55-55;',0);
INSERT INTO "ElementSRIs" VALUES (33,'Roof','Pilkington Optiphon 12.8/20/16.8 (Rw = 51 dB)','Pilkington','Rw',NULL,'0-35-45-49-50-54-54;',0);
INSERT INTO "ElementSRIs" VALUES (34,'Roof','Tile/slate 12.5mm plbd ceiling no absorbing layer above ceiling','BRE','Rw',NULL,'0-21-26-33-33-35-35;',0);
INSERT INTO "ElementSRIs" VALUES (35,'Roof','Tile/slate 12.5mm plbd ceiling absorbing layer above ceiling','BRE','Rw',NULL,'0-24-34-40-45-49-49;',0);
INSERT INTO "ElementSRIs" VALUES (36,'Roof','Flat timber joist','BRE','Rw',NULL,'0-22-37-43-49-57-57;',0);
INSERT INTO "ElementSRIs" VALUES (37,'Roof','Tile/slate 25mm plbd ceiling, sound absorbing layer','BRE','Rw',NULL,'0-27-37-43-48-52-52;',0);
INSERT INTO "ElementSRIs" VALUES (38,'Roof','7mm slate /100mm void/2layersoundblock','Insul','Rw',NULL,'0-22-40-48-52-51-51;',0);
INSERT INTO "ElementSRIs" VALUES (39,'Roof','Flat roof 100mm reinforced concrete','BRE','Rw','Octave','0-39-40-49-53-57-57;',0);
INSERT INTO "ElementSRIs" VALUES (40,'Roof','7mm slate /150mm void/resilient studs/ 2layersoundblock','Insul','Rw',NULL,'0-40-51-57-62-59-59;',0);
INSERT INTO "ElementSRIs" VALUES (41,'Vent','Trickle vent with indirect air path (4000mm^2)','BRE','Dnew',NULL,'0-30-31-31-32-28-28;',4000);
INSERT INTO "ElementSRIs" VALUES (42,'Vent','R5000 - Rytons Window Trickle Ventilator (497mm L - 5000mm^2)','SRL','Dnew',NULL,'0-34-33-35-33-28-28;',5000);
INSERT INTO "ElementSRIs" VALUES (43,'Vent','Hit and miss trickle (4000mm^2)','BRE','Dnew',NULL,'0-34-27-37-35-34-34;',4000);
INSERT INTO "ElementSRIs" VALUES (44,'Vent','Acoustic trickle vent (4000mm^2)','BRE','Dnew',NULL,'0-30-33-38-37-36-36;',4000);
INSERT INTO "ElementSRIs" VALUES (45,'Vent','Greenwood Acoustic Window Ventilator (5000EA) Dnew 42 dB (vent + 2 acoustic modules)','Greenwood','Dnew',NULL,'0-41-39-38-47-43-43;',5000);
INSERT INTO "ElementSRIs" VALUES (46,'Vent','Wind scoop passive stack roof terminals (indicative min.)','BRE','Dnew',NULL,'0-14-16-17-15-17-17;',4000);
INSERT INTO "ElementSRIs" VALUES (47,'Vent','Through wall attenuated air vents (indicative min.)','BRE','Dnew',NULL,'0-18-19-22-28-32-32;',4000);
INSERT INTO "ElementSRIs" VALUES (49,'Vent','Wind scoop passive stack roof terminals (indicative max.)','BRE','Dnew',NULL,'0-20-26-31-36-44-44;',4000);
INSERT INTO "ElementSRIs" VALUES (50,'Vent','Through wall attenuated air vents (indicative max.)','BRE','Dnew',NULL,'0-20-24-31-41-46-46;',4000);
INSERT INTO "ElementSRIs" VALUES (52,'Vent','TAL9H&M - Rytons 9x9 Acoustic air liner through wall vent with hit&miss ventilator (12,800 mm^2)','BRE','Dnew',NULL,'0-38-30-31-38-45-45;',12800);
INSERT INTO "ElementSRIs" VALUES (53,'Vent','Passive attenuated inwall vent (4000mm^2)','BRE','Dnew',NULL,'0-35-34-33-38-49-49;',4000);
INSERT INTO "ElementSRIs" VALUES (54,'Vent','Passivent Fresh 90dB Acoustic Through Wall Vent (external dB wall sleeve cowl can be used to achieve upto an additional 2 dB Dn,e,w)','Passivent','Dnew',NULL,'0-45-30-40-42-49-49;',4000);
INSERT INTO "ElementSRIs" VALUES (55,'Vent','Passivent Fresh TLFdB Acoustic Through Wall Vent (external dB wall sleeve cowl can be used to achieve upto an additional 2 dB Dn,e,w)','Passivent','Dnew',NULL,'0-37-36-47-46-47-47;',4000);
INSERT INTO "ElementSRIs" VALUES (56,'Vent','Fresh 80-200mm wall pipe','Fresh','Dnew',NULL,'0-47-37-40-47-57-57;',4000);
INSERT INTO "ElementSRIs" VALUES (57,'Vent','Passivent Fresh TLFdB (Including Wall Sleeve Cowl)','Passivent','Dnew',NULL,'0-39-38-49-48-49-49;',4000);
INSERT INTO "ElementSRIs" VALUES (58,'Vent','Fresh 80-300mm wall pipe','Fresh','Dnew',NULL,'0-47-37-44-54-68-68;',4000);
INSERT INTO "ElementSRIs" VALUES (59,'Vent','Powered attenuated vent - NIR 1975 (4000mm^2)','BRE','Dnew',NULL,'0-38-38-46-53-60-60;',4000);
INSERT INTO "ElementSRIs" VALUES (60,'Vent','Fresh 80-400mm wall pipe','Fresh','Dnew',NULL,'0-47-42-48-58-77-77;',4000);
INSERT INTO "ElementSRIs" VALUES (61,'Vent','Greenwood AAB4000 through wall acoustic ventilator','Greenwood','Dnew',NULL,'0-33-35-37-43-47-47;',4000);
INSERT INTO "ElementSRIs" VALUES (62,'Vent','Greenwood Airvac MA 3051 through wall acoustic ventilator','Greenwood','Dnew',NULL,'0-46-46-49-55-66-66;',4000);
INSERT INTO "ElementSRIs" VALUES (63,'Wall','Timber frame wall with lightweight cladding','BRE','Rw',NULL,'0-24-34-40-45-49-49;',0);
INSERT INTO "ElementSRIs" VALUES (64,'Wall','Brick/block cavity','BRE','Rw',NULL,'0-41-45-45-54-58-58;',0);
INSERT INTO "ElementSRIs" VALUES (65,'Wall','Brick wall','BRE','Rw',NULL,'0-41-46-52-58-64-64;',0);
INSERT INTO "ElementSRIs" VALUES (66,'OpenArea','A-1 Open Window 200,000 mm2',NULL,'Dnew',NULL,'18.7-14-12-18.7-14-19.9-19.9;',200000);
INSERT INTO "ElementSRIs" VALUES (69,'OpenArea','3% of floor area','ProPG','Rw','Octave','0-0-0-0-0-0-0;','3%');
INSERT INTO "ElementSRIs" VALUES (71,'Door','Standard door','BRE','Rw','Octave','0-20-25-27-28-32-32;',0);
INSERT INTO "ElementSRIs" VALUES (72,'Glazing','Pilkington Insulight 4/12/4 (Rw = 31 dB)','Pilkington','Rw','Octave','0-24-20-25-35-38-38;',0);
INSERT INTO "ElementSRIs" VALUES (73,'Glazing','4mm single glazing','BRE','Rw','Octave','0-20-22-28-32-33-33;',0);
INSERT INTO "ElementSRIs" VALUES (74,'Glazing','4/12/4 double glazing','BRE','Rw',NULL,'0-24-20-25-34-37-37;',0);
INSERT INTO "ElementSRIs" VALUES (75,'Glazing','6/12/6 double glazing','BRE','Rw',NULL,'0-20-19-29-38-34-34;',0);
INSERT INTO "ElementSRIs" VALUES (76,'Glazing','6mm single glazing','BRE','Rw',NULL,'0-24.5-27-30-33-30-30;',0);
INSERT INTO "ElementSRIs" VALUES (77,'Glazing','Pilkington Insulight 6/12/6 (Rw = 33 dB)','Pilkington','Rw',NULL,'0-20-19-29-38-36-36;',0);
INSERT INTO "ElementSRIs" VALUES (78,'Vent','Air vents','BRE','Rw',NULL,'0-33-28-30-43-49-49;',4000);
INSERT INTO "ElementSRIs" VALUES (79,'OpenArea','1% of floor area','ProPG','Rw','Octave','0-0-0-0-0-0-0;','2%');
INSERT INTO "ElementSRIs" VALUES (80,'OpenArea','2% of floor area','ProPG','Rw','Octave','0-0-0-0-0-0-0;','3%');
COMMIT;
