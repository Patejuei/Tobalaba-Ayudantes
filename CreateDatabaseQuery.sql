CREATE DATABASE asistencia_anual;
CREATE TABLE actos
(
corr_cia integer primary key not null,
acto varchar(10),
corr_gral integer,
fecha date,
direccion varchar(100),
lista varchar(2)
);

CREATE TABLE bomberos
(
reg_gral varchar(5) primary key not null,
nombres varchar(50),
apellidoP varchar(30),
apellidoM varchar(30),
email varchar(50),
rut integer,
dv char,
reg_cia integer,
f_ingreso date
);

CREATE TABLE asistencia
(
id integer primary key auto_increment not null,
corr_cia_acto integer,
reg_gral_voluntario varchar(5)
);

ALTER TABLE asistencia
ADD FOREIGN KEY (corr_cia_acto) REFERENCES actos(corr_cia),
ADD foreign key (reg_gral_voluntario) REFERENCES bomberos(reg_gral);