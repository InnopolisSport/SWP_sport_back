-- max group capacity checks
CREATE OR REPLACE FUNCTION check_group_capacity() RETURNS trigger AS
$$
BEGIN
    IF (SELECT count(*) FROM enroll WHERE group_id = new.group_id) >
       (SELECT capacity FROM "group" WHERE id = new.group_id) THEN
        RAISE EXCEPTION 'exceed group capacity';
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS check_group_capacity_trigger
    ON enroll;
CREATE CONSTRAINT TRIGGER check_group_capacity_trigger
    AFTER INSERT
    ON enroll
    FOR EACH ROW
EXECUTE FUNCTION check_group_capacity();



-- valid time intervals
ALTER TABLE schedule DROP CONSTRAINT IF EXISTS start_before_end;
ALTER TABLE training DROP CONSTRAINT IF EXISTS start_before_end;
ALTER TABLE training DROP CONSTRAINT IF EXISTS same_date;
ALTER TABLE schedule
    ADD CONSTRAINT start_before_end CHECK (start < "end");
ALTER TABLE training
    ADD CONSTRAINT start_before_end CHECK (start < "end");
ALTER TABLE training
    ADD CONSTRAINT same_date CHECK (date(start) = date("end"));
