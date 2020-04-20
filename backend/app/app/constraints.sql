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


CREATE OR REPLACE FUNCTION current_semester() RETURNS int AS
$$
DECLARE
    semester_id int;
BEGIN
    SELECT id INTO STRICT semester_id FROM semester WHERE now() >= start ORDER BY start DESC LIMIT 1;
    RETURN semester_id;
END;
$$ LANGUAGE plpgsql;

-- valid time intervals
ALTER TABLE schedule
    DROP CONSTRAINT IF EXISTS start_before_end;
ALTER TABLE training
    DROP CONSTRAINT IF EXISTS start_before_end;
ALTER TABLE training
    DROP CONSTRAINT IF EXISTS same_date;
ALTER TABLE semester
    DROP CONSTRAINT IF EXISTS start_before_end;
ALTER TABLE attendance
    DROP CONSTRAINT IF EXISTS positive_hours;

ALTER TABLE schedule
    ADD CONSTRAINT start_before_end CHECK (start < "end");
ALTER TABLE training
    ADD CONSTRAINT start_before_end CHECK (start < "end");
ALTER TABLE training
    ADD CONSTRAINT same_date CHECK (date(start) = date("end"));
ALTER TABLE semester
    ADD CONSTRAINT start_before_end CHECK (start <= choice_deadline AND choice_deadline <= "end");
ALTER TABLE attendance
    ADD CONSTRAINT positive_hours CHECK (hours > 0);
