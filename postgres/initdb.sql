CREATE TABLE tickets (
    ticket_id serial,
    title text,
    assignee text,
    description text,
    created timestamp default now(),
    due text
    );