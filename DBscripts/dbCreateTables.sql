--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

-- Started on 2021-12-10 17:50:44

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 212 (class 1259 OID 25958)
-- Name: account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account (
    id bigint NOT NULL,
    "accountBalance" double precision NOT NULL,
    "accountNumber" character varying(20) NOT NULL,
    blocked boolean NOT NULL,
    currency character varying(3) NOT NULL,
    "dateCreated" timestamp with time zone NOT NULL,
    "clientId_id" bigint NOT NULL
);


ALTER TABLE public.account OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 25957)
-- Name: account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_id_seq OWNER TO postgres;

--
-- TOC entry 3423 (class 0 OID 0)
-- Dependencies: 211
-- Name: account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_id_seq OWNED BY public.account.id;


--
-- TOC entry 227 (class 1259 OID 26036)
-- Name: card; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.card (
    id bigint NOT NULL,
    "cardHolder" character varying(100) NOT NULL,
    "cardNumber" character varying(20) NOT NULL,
    cvc character varying(64) NOT NULL,
    pin character varying(64) NOT NULL,
    "cardProcessor" character varying(30) NOT NULL,
    "cardType" character varying(20) NOT NULL,
    "validUntil" date NOT NULL,
    "accountFK_id" bigint NOT NULL
);


ALTER TABLE public.card OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 26035)
-- Name: card_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.card_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.card_id_seq OWNER TO postgres;

--
-- TOC entry 3424 (class 0 OID 0)
-- Dependencies: 226
-- Name: card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.card_id_seq OWNED BY public.card.id;


--
-- TOC entry 225 (class 1259 OID 26017)
-- Name: certificate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.certificate (
    id bigint NOT NULL,
    "authorityName" character varying(50) NOT NULL,
    "cerPath" character varying(200) NOT NULL,
    "pfxPath" character varying(200) NOT NULL,
    "pvkPath" character varying(200) NOT NULL,
    "certificateName" character varying(100) NOT NULL,
    "userId_id" integer NOT NULL
);


ALTER TABLE public.certificate OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 26016)
-- Name: certificate_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.certificate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.certificate_id_seq OWNER TO postgres;

--
-- TOC entry 3425 (class 0 OID 0)
-- Dependencies: 224
-- Name: certificate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.certificate_id_seq OWNED BY public.certificate.id;


--
-- TOC entry 223 (class 1259 OID 26008)
-- Name: client; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client (
    id bigint NOT NULL,
    "userId_id" integer NOT NULL
);


ALTER TABLE public.client OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 26007)
-- Name: client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.client_id_seq OWNER TO postgres;

--
-- TOC entry 3426 (class 0 OID 0)
-- Dependencies: 222
-- Name: client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_id_seq OWNED BY public.client.id;


--
-- TOC entry 210 (class 1259 OID 25949)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 25948)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- TOC entry 3427 (class 0 OID 0)
-- Dependencies: 209
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- TOC entry 213 (class 1259 OID 25964)
-- Name: exchangerate; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exchangerate (
    id integer NOT NULL,
    currency character varying(3) NOT NULL,
    "rateInDinar" double precision NOT NULL
);


ALTER TABLE public.exchangerate OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 25971)
-- Name: iuser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.iuser (
    id integer NOT NULL,
    "fullName" character varying(50) NOT NULL,
    password character varying(64) NOT NULL,
    username character varying(40) NOT NULL,
    "billingAddress" character varying(50) NOT NULL,
    gender character varying(20) NOT NULL,
    jmbg bigint NOT NULL,
    "birthDate" date NOT NULL,
    "userType" character varying(40) NOT NULL
);


ALTER TABLE public.iuser OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 25980)
-- Name: paymentcode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paymentcode (
    code smallint NOT NULL,
    description character varying(100) NOT NULL,
    CONSTRAINT paymentcode_code_check CHECK ((code >= 0))
);


ALTER TABLE public.paymentcode OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 25987)
-- Name: tractransferinfo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tractransferinfo (
    id bigint NOT NULL,
    "accountNumber" character varying(20) NOT NULL,
    "billingAddress" character varying(50) NOT NULL,
    "fullName" character varying(50) NOT NULL
);


ALTER TABLE public.tractransferinfo OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 25986)
-- Name: tractransferinfo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tractransferinfo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tractransferinfo_id_seq OWNER TO postgres;

--
-- TOC entry 3428 (class 0 OID 0)
-- Dependencies: 216
-- Name: tractransferinfo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tractransferinfo_id_seq OWNED BY public.tractransferinfo.id;


--
-- TOC entry 221 (class 1259 OID 26001)
-- Name: transaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transaction (
    id bigint NOT NULL,
    amount double precision NOT NULL,
    "modelCode" integer,
    "paymentPurpose" character varying(70),
    "preciseTime" timestamp with time zone NOT NULL,
    provision double precision,
    "referenceNumber" character varying(50),
    "transactionType" character varying(30) NOT NULL,
    currency character varying(3) NOT NULL,
    "myAccInfoFK_id" bigint NOT NULL,
    "paymentCodeFK_id" smallint NOT NULL,
    "transferAccInfoFK_id" bigint NOT NULL
);


ALTER TABLE public.transaction OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 26000)
-- Name: transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_id_seq OWNER TO postgres;

--
-- TOC entry 3429 (class 0 OID 0)
-- Dependencies: 220
-- Name: transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transaction_id_seq OWNED BY public.transaction.id;


--
-- TOC entry 219 (class 1259 OID 25994)
-- Name: trmyaccountinfo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trmyaccountinfo (
    id bigint NOT NULL,
    "balanceBefore" double precision NOT NULL,
    "balanceAfter" double precision NOT NULL,
    "accountNumber" character varying(20) NOT NULL,
    "billingAddress" character varying(50) NOT NULL,
    "fullName" character varying(50) NOT NULL
);


ALTER TABLE public.trmyaccountinfo OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 25993)
-- Name: trmyaccountinfo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.trmyaccountinfo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trmyaccountinfo_id_seq OWNER TO postgres;

--
-- TOC entry 3430 (class 0 OID 0)
-- Dependencies: 218
-- Name: trmyaccountinfo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.trmyaccountinfo_id_seq OWNED BY public.trmyaccountinfo.id;


--
-- TOC entry 3212 (class 2604 OID 25961)
-- Name: account id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account ALTER COLUMN id SET DEFAULT nextval('public.account_id_seq'::regclass);


--
-- TOC entry 3219 (class 2604 OID 26039)
-- Name: card id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card ALTER COLUMN id SET DEFAULT nextval('public.card_id_seq'::regclass);


--
-- TOC entry 3218 (class 2604 OID 26020)
-- Name: certificate id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certificate ALTER COLUMN id SET DEFAULT nextval('public.certificate_id_seq'::regclass);


--
-- TOC entry 3217 (class 2604 OID 26011)
-- Name: client id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client ALTER COLUMN id SET DEFAULT nextval('public.client_id_seq'::regclass);


--
-- TOC entry 3211 (class 2604 OID 25952)
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- TOC entry 3214 (class 2604 OID 25990)
-- Name: tractransferinfo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tractransferinfo ALTER COLUMN id SET DEFAULT nextval('public.tractransferinfo_id_seq'::regclass);


--
-- TOC entry 3216 (class 2604 OID 26004)
-- Name: transaction id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction ALTER COLUMN id SET DEFAULT nextval('public.transaction_id_seq'::regclass);


--
-- TOC entry 3215 (class 2604 OID 25997)
-- Name: trmyaccountinfo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trmyaccountinfo ALTER COLUMN id SET DEFAULT nextval('public.trmyaccountinfo_id_seq'::regclass);


--
-- TOC entry 3223 (class 2606 OID 26043)
-- Name: account account_clientId_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "account_clientId_id_key" UNIQUE ("clientId_id");


--
-- TOC entry 3225 (class 2606 OID 25963)
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- TOC entry 3271 (class 2606 OID 26041)
-- Name: card card_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);


--
-- TOC entry 3255 (class 2606 OID 26026)
-- Name: certificate certificate_cerPath_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certificate
    ADD CONSTRAINT "certificate_cerPath_key" UNIQUE ("cerPath");


--
-- TOC entry 3258 (class 2606 OID 26032)
-- Name: certificate certificate_certificateName_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certificate
    ADD CONSTRAINT "certificate_certificateName_key" UNIQUE ("certificateName");


--
-- TOC entry 3261 (class 2606 OID 26028)
-- Name: certificate certificate_pfxPath_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certificate
    ADD CONSTRAINT "certificate_pfxPath_key" UNIQUE ("pfxPath");


--
-- TOC entry 3263 (class 2606 OID 26024)
-- Name: certificate certificate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certificate
    ADD CONSTRAINT certificate_pkey PRIMARY KEY (id);


--
-- TOC entry 3266 (class 2606 OID 26030)
-- Name: certificate certificate_pvkPath_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certificate
    ADD CONSTRAINT "certificate_pvkPath_key" UNIQUE ("pvkPath");


--
-- TOC entry 3268 (class 2606 OID 26034)
-- Name: certificate certificate_userId_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certificate
    ADD CONSTRAINT "certificate_userId_id_key" UNIQUE ("userId_id");


--
-- TOC entry 3250 (class 2606 OID 26013)
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- TOC entry 3252 (class 2606 OID 26015)
-- Name: client client_userId_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT "client_userId_id_key" UNIQUE ("userId_id");


--
-- TOC entry 3221 (class 2606 OID 25956)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 3228 (class 2606 OID 25970)
-- Name: exchangerate exchangerate_currency_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exchangerate
    ADD CONSTRAINT exchangerate_currency_key UNIQUE (currency);


--
-- TOC entry 3230 (class 2606 OID 25968)
-- Name: exchangerate exchangerate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exchangerate
    ADD CONSTRAINT exchangerate_pkey PRIMARY KEY (id);


--
-- TOC entry 3232 (class 2606 OID 25979)
-- Name: iuser iuser_jmbg_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iuser
    ADD CONSTRAINT iuser_jmbg_key UNIQUE (jmbg);


--
-- TOC entry 3234 (class 2606 OID 25975)
-- Name: iuser iuser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iuser
    ADD CONSTRAINT iuser_pkey PRIMARY KEY (id);


--
-- TOC entry 3237 (class 2606 OID 25977)
-- Name: iuser iuser_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iuser
    ADD CONSTRAINT iuser_username_key UNIQUE (username);


--
-- TOC entry 3239 (class 2606 OID 25985)
-- Name: paymentcode paymentcode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paymentcode
    ADD CONSTRAINT paymentcode_pkey PRIMARY KEY (code);


--
-- TOC entry 3241 (class 2606 OID 25992)
-- Name: tractransferinfo tractransferinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tractransferinfo
    ADD CONSTRAINT tractransferinfo_pkey PRIMARY KEY (id);


--
-- TOC entry 3247 (class 2606 OID 26006)
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id);


--
-- TOC entry 3243 (class 2606 OID 25999)
-- Name: trmyaccountinfo trmyaccountinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trmyaccountinfo
    ADD CONSTRAINT trmyaccountinfo_pkey PRIMARY KEY (id);


--
-- TOC entry 3269 (class 1259 OID 26088)
-- Name: card_accountFK_id_4d78ca34; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "card_accountFK_id_4d78ca34" ON public.card USING btree ("accountFK_id");


--
-- TOC entry 3253 (class 1259 OID 26079)
-- Name: certificate_cerPath_8c3d2c7e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "certificate_cerPath_8c3d2c7e_like" ON public.certificate USING btree ("cerPath" varchar_pattern_ops);


--
-- TOC entry 3256 (class 1259 OID 26082)
-- Name: certificate_certificateName_97994fd9_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "certificate_certificateName_97994fd9_like" ON public.certificate USING btree ("certificateName" varchar_pattern_ops);


--
-- TOC entry 3259 (class 1259 OID 26080)
-- Name: certificate_pfxPath_20aa36b8_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "certificate_pfxPath_20aa36b8_like" ON public.certificate USING btree ("pfxPath" varchar_pattern_ops);


--
-- TOC entry 3264 (class 1259 OID 26081)
-- Name: certificate_pvkPath_ebce976d_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "certificate_pvkPath_ebce976d_like" ON public.certificate USING btree ("pvkPath" varchar_pattern_ops);


--
-- TOC entry 3226 (class 1259 OID 26049)
-- Name: exchangerate_currency_87e9152b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX exchangerate_currency_87e9152b_like ON public.exchangerate USING btree (currency varchar_pattern_ops);


--
-- TOC entry 3235 (class 1259 OID 26050)
-- Name: iuser_username_a3d2f024_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX iuser_username_a3d2f024_like ON public.iuser USING btree (username varchar_pattern_ops);


--
-- TOC entry 3244 (class 1259 OID 26066)
-- Name: transaction_myAccInfoFK_id_88c887e2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "transaction_myAccInfoFK_id_88c887e2" ON public.transaction USING btree ("myAccInfoFK_id");


--
-- TOC entry 3245 (class 1259 OID 26067)
-- Name: transaction_paymentCodeFK_id_d0c647b8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "transaction_paymentCodeFK_id_d0c647b8" ON public.transaction USING btree ("paymentCodeFK_id");


--
-- TOC entry 3248 (class 1259 OID 26068)
-- Name: transaction_transferAccInfoFK_id_16bb7c1e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX "transaction_transferAccInfoFK_id_16bb7c1e" ON public.transaction USING btree ("transferAccInfoFK_id");


--
-- TOC entry 3272 (class 2606 OID 26044)
-- Name: account account_clientId_id_c037851f_fk_client_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT "account_clientId_id_c037851f_fk_client_id" FOREIGN KEY ("clientId_id") REFERENCES public.client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3278 (class 2606 OID 26083)
-- Name: card card_accountFK_id_4d78ca34_fk_account_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT "card_accountFK_id_4d78ca34_fk_account_id" FOREIGN KEY ("accountFK_id") REFERENCES public.account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3277 (class 2606 OID 26074)
-- Name: certificate certificate_userId_id_ca01cfb6_fk_iuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certificate
    ADD CONSTRAINT "certificate_userId_id_ca01cfb6_fk_iuser_id" FOREIGN KEY ("userId_id") REFERENCES public.iuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3276 (class 2606 OID 26069)
-- Name: client client_userId_id_8601a7ac_fk_iuser_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT "client_userId_id_8601a7ac_fk_iuser_id" FOREIGN KEY ("userId_id") REFERENCES public.iuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3273 (class 2606 OID 26051)
-- Name: transaction transaction_myAccInfoFK_id_88c887e2_fk_trmyaccountinfo_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT "transaction_myAccInfoFK_id_88c887e2_fk_trmyaccountinfo_id" FOREIGN KEY ("myAccInfoFK_id") REFERENCES public.trmyaccountinfo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3274 (class 2606 OID 26056)
-- Name: transaction transaction_paymentCodeFK_id_d0c647b8_fk_paymentcode_code; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT "transaction_paymentCodeFK_id_d0c647b8_fk_paymentcode_code" FOREIGN KEY ("paymentCodeFK_id") REFERENCES public.paymentcode(code) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 3275 (class 2606 OID 26061)
-- Name: transaction transaction_transferAccInfoFK_id_16bb7c1e_fk_tractrans; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT "transaction_transferAccInfoFK_id_16bb7c1e_fk_tractrans" FOREIGN KEY ("transferAccInfoFK_id") REFERENCES public.tractransferinfo(id) DEFERRABLE INITIALLY DEFERRED;


-- Completed on 2021-12-10 17:50:44

--
-- PostgreSQL database dump complete
--

