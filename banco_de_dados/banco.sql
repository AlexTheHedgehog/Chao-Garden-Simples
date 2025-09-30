create table usuarios(
	id integer not null primary key autoincrement,
	nome varchar not null,
	senha varchar not null
);

drop table usuarios;

create table chao(
	id integer not null primary key autoincrement,
	nome varchar not null,
	carinho int not null,
	higiene int not null,
	diversao int not null,
	sono int not null,
	fome int not null,
	jog_id int not null,
	
	foreign key (jog_id) references usuarios (id)
);

drop table chao;