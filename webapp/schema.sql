


CREATE TABLE supporters (
    id bigserial UNIQUE NOT NULL,
    created timestamp with time zone DEFAULT NOW(),
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    town character varying(25) NOT NULL,
    emailaddress character varying(100) UNIQUE NOT NULL,
    publicvisible boolean DEFAULT false NOT NULL,
    campaign_info boolean DEFAULT false NOT NULL,
    post_data text NOT NULL
);

ALTER TABLE ONLY supporters ADD CONSTRAINT supporters_pkey PRIMARY KEY (id);

