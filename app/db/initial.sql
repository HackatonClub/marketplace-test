create table customer
(
    id       serial
        constraint customer_pk
            primary key,
    name     varchar(256) not null unique,
    password text         not null
);


create table product
(
    id          serial
        constraint product_pk
            primary key,
    name        varchar(256) not null,
    description varchar(256),
    price       integer,
    avg_rating  float,
    num_reviews integer,
    url jsonb,
    tag_id jsonb
);

create table tags
(
    id   serial
        constraint tags_pk
            primary key,
    name varchar(256) not null
        unique
);

create table tags_product
(
    tag_id integer references tags (id),
    product_id integer references product (id)
);

create table cart_product
(
    id          serial
        constraint cart_product_pk
            primary key,
    customer_id integer references customer (id) on delete cascade,
    product_id  integer references product (id) on delete cascade,
    product_num integer not null,
    unique (customer_id, product_id)
);

create table favourite
(
    id          serial
        constraint favourite_pk
            primary key,
    customer_id integer references customer (id) on delete cascade,
    product_id  integer references product (id) on delete cascade,
    unique (customer_id, product_id)
);

create table review
(
    id          serial
        constraint review_pk
            primary key,
    product_id  integer references product (id) on delete cascade,
    customer_id integer references customer (id) on delete cascade,
    body        varchar(256),
    rating      integer,
    unique (product_id, customer_id)
);

