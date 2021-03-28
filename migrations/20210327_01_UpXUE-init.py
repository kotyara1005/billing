from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        create table wallet (
            id serial primary key,
            client_id int UNIQUE NOT NULL,
            amount decimal(12, 2) NOT NULL,
            currency varchar(4) NOT NULL
        );
        create table transaction (
            id serial primary key,
            from_wallet_id int NULL,
            to_wallet_id int NOT NULL,
            amount decimal(12, 2) NOT NULL,
            currency varchar(4) NOT NULL,
            request_id uuid UNIQUE NOT NULL
        );
        """,
        """
            drop table wallet;
            drop table transaction;
        """,
    )
]
