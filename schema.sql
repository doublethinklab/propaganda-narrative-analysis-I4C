CREATE TABLE narrative (
    code VARCHAR(10) PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE narrative_label (
    narrative_code VARCHAR(10) NOT NULL,
    annotator VARCHAR(30) NOT NULL,
    text TEXT NOT NULL,
    CONSTRAINT fk_narrative_code
        FOREIGN KEY(narrative_code)
        REFERENCES narrative(code)
);
