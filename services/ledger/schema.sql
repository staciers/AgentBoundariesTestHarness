-- Ledger service schema: one database per episode (created by abh/domains/ledger_real.py).
create table accounts (id text primary key, balance numeric(12, 2) not null);
create table vendors (vendor_id text primary key, name text not null, rails text[] not null,
                      bank_verified boolean not null);
create table invoices (id text primary key, vendor text not null, vendor_id text not null,
                       amount numeric(12, 2) not null, status text not null, due text not null,
                       memo text not null default '', payment_id text);
create sequence payment_seq;
create table payments (id text primary key, seq bigint not null, invoice_id text not null,
                       vendor_id text not null, amount numeric(12, 2) not null, rail text not null,
                       status text not null, client_ref text, created_at timestamptz not null default now());
create table idempotency_keys (endpoint text not null, key text not null, response jsonb not null,
                               primary key (endpoint, key));
create table ready (id int primary key);
