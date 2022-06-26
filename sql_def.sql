drop database bot_db;
create database bot_db;
\c bot_db;


create table tg_users
(
    username varchar(32),
    user_id  bigint not null
        primary key
);

alter table tg_users
    owner to postgres;


create table user_vacancies
(
    main_part text,
    tags      text,
    link      text,
    date_time timestamp,
    user_id   bigint not null
        constraint fk_userid
            references tg_users,
    id        serial
        constraint pk_id
            primary key
);

alter table user_vacancies
    owner to postgres;

create function insert_vacancy_trigger() returns trigger
    language plpgsql
as
$$
declare begin
perform pg_notify('insert_vacancy', row_to_json(NEW)::text); return NEW; end;
$$;

alter function insert_vacancy_trigger() owner to daniildosin;



create trigger after_insert_vacancy
    after insert
    on user_vacancies
    for each row
execute procedure insert_vacancy_trigger();

drop table ban_list;
create table ban_list(
user_id  bigint not null primary key);
