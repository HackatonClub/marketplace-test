create table customer
(
    id   serial
        constraint customer_pk
            primary key,
    name varchar(256) not null
);

create table cart
(
    id          serial
        constraint cart_pk
            primary key,
    customer_id integer references customer(id)
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
    num_reviews integer
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
    product_id integer references product(id),
    tag_id     integer references tags(id),
    unique (product_id,tag_id)
);

create table product_photo
(
    id         serial
        constraint product_photo_pk
            primary key,
    product_id integer references product(id),
    url        varchar(256)
);

create table cart_product
(
    cart_id integer references cart(id),
    product_id integer references product(id)
);

create table favourite
(
    customer_id integer references customer(id),
    product_id  integer references product(id)
);

create table review
(
    product_id  integer references product(id),
    customer_id integer references customer(id),
    body        varchar(256),
    rating      integer
);

