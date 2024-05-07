use MY_CUSTOM_BOT;

select * from searchresults;

START TRANSACTION;
DELETE FROM searchresults;
COMMIT;  -- Use ROLLBACK; to undo the delete if necessary before committing

UPDATE SearchResults
SET Frequency = 1;

CREATE TABLE searchresults (
    SearchTermID INT,
    URL VARCHAR(255) UNIQUE,
    Frequency INT DEFAULT 1
);

drop table searchresults;
SET SQL_SAFE_UPDATES = 0;

ALTER TABLE searchresults
ADD UNIQUE (URL);
ALTER TABLE searchresults DROP COLUMN SearchTermID;

CREATE TABLE searchresults (
    URL VARCHAR(255) NOT NULL,
    SearchTerm VARCHAR(255) NOT NULL,
    Frequency INT DEFAULT 1,
    PRIMARY KEY (URL),
    UNIQUE (URL)
);

ALTER TABLE searchresults
MODIFY URL VARCHAR(767);

ALTER TABLE searchresults
ADD PRIMARY KEY (URL),
ADD UNIQUE (URL);


select * from SearchTerms;
select * from searchresults order by Frequency DESC;

DELETE FROM searchresults WHERE URL LIKE '/url?%';

ALTER TABLE searchresults ADD COLUMN Description TEXT;
ALTER TABLE searchresults DROP COLUMN Description;


delete from searchresults where SearchTerm is NULL;
CREATE TABLE SearchResults (
    SearchTermID INT,
    URL VARCHAR(255)
);

-- CREATE USER 'root'@'208.97.153.205' IDENTIFIED BY 'IcandoIt@2024';
-- GRANT ALL PRIVILEGES ON *.* TO 'root'@'208.97.153.205' WITH GRANT OPTION;
-- FLUSH PRIVILEGES;

CREATE USER 'dh_vipqax'@'208.97.153.205' IDENTIFIED BY '*8#wDl2dG8';
GRANT ALL PRIVILEGES ON MY_CUSTOM_BOT.* TO 'dh_vipqax'@'208.97.153.205';
FLUSH PRIVILEGES;

