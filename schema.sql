-- Campus Recruiting and Finance Event Management System
-- PostgreSQL Schema

DROP TABLE IF EXISTS FOLLOW_UP CASCADE;
DROP TABLE IF EXISTS WAITLIST CASCADE;
DROP TABLE IF EXISTS ATTENDANCE CASCADE;
DROP TABLE IF EXISTS RSVP CASCADE;
DROP TABLE IF EXISTS EVENT CASCADE;
DROP TABLE IF EXISTS STUDENT CASCADE;
DROP TABLE IF EXISTS ORGANIZER CASCADE;
DROP TABLE IF EXISTS COMPANY CASCADE;

-- Core entities
CREATE TABLE COMPANY (
    company_id  SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    industry    VARCHAR(100),
    website     VARCHAR(255)
);

CREATE TABLE ORGANIZER (
    organizer_id SERIAL PRIMARY KEY,
    full_name    VARCHAR(100) NOT NULL,
    email        VARCHAR(100) UNIQUE NOT NULL,
    role         VARCHAR(100)
);

CREATE TABLE STUDENT (
    student_id      SERIAL PRIMARY KEY,
    full_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    major           VARCHAR(100),
    graduation_year INT
);

CREATE TABLE EVENT (
    event_id     SERIAL PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    event_type   VARCHAR(50),   -- e.g. 'panel', 'networking', 'workshop', 'info_session'
    event_date   DATE NOT NULL,
    location     VARCHAR(200),
    capacity     INT NOT NULL CHECK (capacity > 0),
    description  TEXT,
    company_id   INT REFERENCES COMPANY(company_id) ON DELETE SET NULL,
    organizer_id INT REFERENCES ORGANIZER(organizer_id) ON DELETE SET NULL
);

-- Junction / participation tables
CREATE TABLE RSVP (
    student_id  INT REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    event_id    INT REFERENCES EVENT(event_id) ON DELETE CASCADE,
    rsvp_status VARCHAR(20) NOT NULL DEFAULT 'confirmed'
                CHECK (rsvp_status IN ('confirmed', 'cancelled')),
    created_at  TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (student_id, event_id)
);

CREATE TABLE WAITLIST (
    student_id        INT REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    event_id          INT REFERENCES EVENT(event_id) ON DELETE CASCADE,
    waitlist_position INT NOT NULL,
    joined_at         TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (student_id, event_id)
);

CREATE TABLE ATTENDANCE (
    student_id    INT REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    event_id      INT REFERENCES EVENT(event_id) ON DELETE CASCADE,
    attended_flag BOOLEAN DEFAULT FALSE,
    checkin_time  TIMESTAMP,
    PRIMARY KEY (student_id, event_id)
);

CREATE TABLE FOLLOW_UP (
    followup_id   SERIAL PRIMARY KEY,
    student_id    INT REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    event_id      INT REFERENCES EVENT(event_id) ON DELETE CASCADE,
    followup_type VARCHAR(50),   -- e.g. 'thank_you', 'application', 'interview'
    status        VARCHAR(50) DEFAULT 'pending',
    notes         TEXT,
    created_at    TIMESTAMP DEFAULT NOW()
);

-- =============================================================
-- ADVANCED FEATURE: Automatic Waitlist Seat Promotion
--
-- When a confirmed RSVP is deleted (cancellation), this trigger
-- fires and automatically promotes the first student on the
-- waitlist (lowest waitlist_position) to a confirmed RSVP.
-- The promoted student is removed from WAITLIST and all
-- remaining positions are decremented by 1.
-- All steps run in a single transaction for data integrity.
-- =============================================================

CREATE OR REPLACE FUNCTION promote_from_waitlist()
RETURNS TRIGGER AS $$
DECLARE
    next_student_id INT;
BEGIN
    -- Only run promotion when a *confirmed* RSVP is removed
    IF OLD.rsvp_status <> 'confirmed' THEN
        RETURN OLD;
    END IF;

    -- Find the student with the lowest waitlist position for this event
    SELECT student_id INTO next_student_id
    FROM WAITLIST
    WHERE event_id = OLD.event_id
    ORDER BY waitlist_position ASC
    LIMIT 1;

    IF next_student_id IS NOT NULL THEN
        -- Promote: insert a confirmed RSVP for the waitlisted student
        INSERT INTO RSVP (student_id, event_id, rsvp_status, created_at)
        VALUES (next_student_id, OLD.event_id, 'confirmed', NOW());

        -- Remove the promoted student from WAITLIST
        DELETE FROM WAITLIST
        WHERE student_id = next_student_id AND event_id = OLD.event_id;

        -- Reorder remaining waitlist positions (close the gap)
        UPDATE WAITLIST
        SET waitlist_position = waitlist_position - 1
        WHERE event_id = OLD.event_id;
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_promote_waitlist
AFTER DELETE ON RSVP
FOR EACH ROW
EXECUTE FUNCTION promote_from_waitlist();
