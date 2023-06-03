create table if not exists users
(
    id       serial
        constraint customer_pk
            primary key,
    name     varchar(256) not null unique,
    password text         not null,
    role integer not null
);


create table if not exists product
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

create table if not exists tags
(
    id   serial
        constraint tags_pk
            primary key,
    name varchar(256) not null
        unique
);

create table if not exists tags_product
(
    tag_id integer references tags (id) on delete cascade,
    product_id integer references product (id) on delete cascade,
    unique (tag_id,product_id)
);

create table if not exists cart_product
(
    id          serial
        constraint cart_product_pk
            primary key,
    customer_id integer references users (id) on delete cascade,
    product_id  integer references product (id) on delete cascade,
    product_num integer not null,
    unique (customer_id, product_id)
);

create table if not exists favourite
(
    id          serial
        constraint favourite_pk
            primary key,
    customer_id integer references users (id) on delete cascade,
    product_id  integer references product (id) on delete cascade,
    unique (customer_id, product_id)
);

create table if not exists review
(
    id          serial
        constraint review_pk
            primary key,
    product_id  integer references product (id) on delete cascade,
    customer_id integer references users (id) on delete cascade,
    body        varchar(256),
    rating      integer,
    unique (product_id, customer_id)
);

CREATE OR REPLACE FUNCTION get_favorites_u(customer integer, previous integer,lim integer )
RETURNS table (product_id integer,previous_id integer) AS $$
#variable_conflict use_column
BEGIN
  return query
   SELECT product_id,id AS previous_id
               FROM favourite
               WHERE customer_id = $1 AND id > $2
               LIMIT $3;
END
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_cart_products( customer integer, previous integer,lim integer)
RETURNS table (product_id integer,name varchar(256), price integer,url jsonb, love text,product_num integer, previous_id integer) AS $$
#variable_conflict use_column
BEGIN
  return query
   SELECT p.id AS product_id,
                      p.name,
                      p.price,
                      p.url,
                      CASE
                        WHEN favourite.product_id = p.id THEN 'Yes'
                        ELSE 'No'
                      END AS Love,
                      cart_product.product_num,
                      cart_product.id AS previous_id
               FROM cart_product
               JOIN product p ON p.id = cart_product.product_id
               AND customer_id = customer
               LEFT JOIN favourite ON favourite.customer_id = customer
                AND favourite.product_id = p.id
               WHERE  cart_product.id > previous
               LIMIT lim ;
END
$$ LANGUAGE plpgsql;


CREATE PROCEDURE insert_data_cart(customer integer, product_id integer,product_num integer)
LANGUAGE SQL
AS $$
INSERT INTO cart_product(customer_id, product_id, product_num)
               VALUES (customer,product_id ,product_num);
$$;
