--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0
-- Dumped by pg_dump version 14.0

-- Started on 2021-12-11 19:45:09

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3344 (class 0 OID 16428)
-- Dependencies: 219
-- Data for Name: exchangerate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exchangerate (id, currency, "rateInDinar") FROM stdin;
1	EUR	117.5851
2	CHF	112.5971
3	USD	104.0576
4	GBP	137.5425
5	AUD	74.3786
6	CAD	81.8382
7	RUB	1.4111
\.


-- Completed on 2021-12-11 19:45:10

--
-- PostgreSQL database dump complete
--

