-- Seed data for Campus Recruiting and Finance Event Management System

INSERT INTO COMPANY (name, industry, website) VALUES
    ('Goldman Sachs',   'Finance',       'https://www.goldmansachs.com'),
    ('McKinsey & Co',   'Consulting',    'https://www.mckinsey.com'),
    ('JPMorgan Chase',  'Finance',       'https://www.jpmorganchase.com'),
    ('Deloitte',        'Consulting',    'https://www.deloitte.com'),
    ('BlackRock',       'Finance',       'https://www.blackrock.com'),
    ('Morgan Stanley',  'Finance',       'https://www.morganstanley.com'),
    ('PwC',             'Consulting',    'https://www.pwc.com');

INSERT INTO ORGANIZER (full_name, email, role) VALUES
    ('Priya Sharma',   'psharma@university.edu',   'Finance Club President'),
    ('Marcus Lee',     'mlee@university.edu',       'Career Events Coordinator'),
    ('Aisha Johnson',  'ajohnson@university.edu',   'Club Vice President');

INSERT INTO STUDENT (full_name, email, major, graduation_year) VALUES
    ('Dev Gajjar',      'dgajjar@student.edu',    'Computer Science',    2026),
    ('Emily Chen',      'echen@student.edu',       'Finance',             2025),
    ('James Okafor',    'jokafor@student.edu',     'Business Analytics',  2026),
    ('Sofia Martinez',  'smartinez@student.edu',   'Accounting',          2027),
    ('Liam Patel',      'lpatel@student.edu',      'Computer Science',    2025),
    ('Nina Russo',      'nrusso@student.edu',      'Economics',           2026),
    ('Tyler Brooks',    'tbrooks@student.edu',     'Finance',             2027),
    ('Mia Nguyen',      'mnguyen@student.edu',     'Marketing',           2025),
    ('Chris Walton',    'cwalton@student.edu',     'Finance',             2026),
    ('Jasmine Ford',    'jford@student.edu',       'Economics',           2025);

INSERT INTO EVENT (title, event_type, event_date, location, capacity, description, company_id, organizer_id) VALUES
    ('Goldman Sachs Info Session',         'info_session', '2025-04-10', 'Business Building 201',  3,  'Learn about summer analyst roles at Goldman Sachs.',             1, 1),
    ('McKinsey Consulting Panel',          'panel',        '2025-04-15', 'Student Center Room A',   5,  'Panel discussion with McKinsey consultants.',                    2, 2),
    ('JPMorgan Networking Night',          'networking',   '2025-04-20', 'Campus Ballroom',          10, 'Informal networking with JPMorgan representatives.',            3, 3),
    ('Deloitte Resume Workshop',           'workshop',     '2025-04-25', 'Library Conference Rm',    8,  'Resume review and interview tips from Deloitte recruiters.',    4, 1),
    ('BlackRock Investment Info Session',  'info_session', '2025-05-01', 'Business Building 101',    4,  'Overview of BlackRock full-time and internship opportunities.', 5, 2),
    ('Morgan Stanley Finance Workshop',    'workshop',     '2025-05-08', 'Business Building 305',    6,  'Technical finance skills and modeling overview.',               6, 3),
    ('PwC Accounting Info Session',        'info_session', '2025-05-12', 'Student Center Room B',    5,  'Learn about PwC audit and advisory programs.',                  7, 1),
    ('Goldman Sachs Networking Night',     'networking',   '2025-05-18', 'Campus Ballroom',          12, 'Meet Goldman Sachs recruiters and current analysts.',           1, 2),
    ('JPMorgan Investment Banking Panel',  'panel',        '2025-05-22', 'Business Building 201',    6,  'Hear from JPMorgan IBD analysts on deal experience.',           3, 1),
    ('McKinsey Case Interview Workshop',   'workshop',     '2025-05-28', 'Library Conference Rm',    8,  'Practice case interviews with McKinsey consultants.',           2, 3);

-- RSVPs
-- Event 1 (Goldman Info Session, capacity=3): fill it up to demo the waitlist
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (1, 1, 'confirmed'),
    (2, 1, 'confirmed'),
    (3, 1, 'confirmed');

-- Event 2 (McKinsey Panel)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (2, 2, 'confirmed'),
    (3, 2, 'confirmed'),
    (4, 2, 'confirmed'),
    (6, 2, 'confirmed');

-- Event 3 (JPMorgan Networking)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (1, 3, 'confirmed'),
    (4, 3, 'confirmed'),
    (5, 3, 'confirmed'),
    (7, 3, 'confirmed'),
    (9, 3, 'confirmed');

-- Event 4 (Deloitte Workshop)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (5, 4, 'confirmed'),
    (6, 4, 'confirmed'),
    (8, 4, 'confirmed');

-- Event 5 (BlackRock Info Session, capacity=4)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (1, 5, 'confirmed'),
    (2, 5, 'confirmed'),
    (9, 5, 'confirmed'),
    (10, 5, 'confirmed');

-- Event 6 (Morgan Stanley Workshop)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (2, 6, 'confirmed'),
    (7, 6, 'confirmed'),
    (8, 6, 'confirmed');

-- Event 7 (PwC Info Session)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (4, 7, 'confirmed'),
    (6, 7, 'confirmed'),
    (10, 7, 'confirmed');

-- Event 8 (Goldman Networking)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (1, 8, 'confirmed'),
    (3, 8, 'confirmed'),
    (5, 8, 'confirmed'),
    (9, 8, 'confirmed');

-- Event 9 (JPMorgan IBD Panel)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (2, 9, 'confirmed'),
    (7, 9, 'confirmed'),
    (9, 9, 'confirmed');

-- Event 10 (McKinsey Case Workshop)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (3, 10, 'confirmed'),
    (6, 10, 'confirmed'),
    (8, 10, 'confirmed'),
    (10, 10, 'confirmed');

-- Waitlist entries for Event 1 (already at capacity of 3)
INSERT INTO WAITLIST (student_id, event_id, waitlist_position) VALUES
    (4, 1, 1),
    (5, 1, 2),
    (6, 1, 3);

-- Attendance records
INSERT INTO ATTENDANCE (student_id, event_id, attended_flag, checkin_time) VALUES
    (1, 1, TRUE,  '2025-04-10 18:05:00'),
    (2, 1, TRUE,  '2025-04-10 18:10:00'),
    (3, 1, FALSE, NULL),
    (2, 2, TRUE,  '2025-04-15 17:00:00'),
    (3, 2, TRUE,  '2025-04-15 17:03:00'),
    (4, 2, FALSE, NULL),
    (6, 2, TRUE,  '2025-04-15 17:05:00'),
    (1, 3, TRUE,  '2025-04-20 19:00:00'),
    (4, 3, TRUE,  '2025-04-20 19:12:00'),
    (5, 3, FALSE, NULL),
    (7, 3, TRUE,  '2025-04-20 19:05:00'),
    (9, 3, TRUE,  '2025-04-20 19:08:00'),
    (5, 4, TRUE,  '2025-04-25 16:00:00'),
    (6, 4, TRUE,  '2025-04-25 16:03:00'),
    (8, 4, FALSE, NULL),
    (1, 5, TRUE,  '2025-05-01 17:30:00'),
    (2, 5, TRUE,  '2025-05-01 17:35:00'),
    (9, 5, TRUE,  '2025-05-01 17:40:00'),
    (10, 5, FALSE, NULL);

-- Follow-up records
INSERT INTO FOLLOW_UP (student_id, event_id, followup_type, status, notes) VALUES
    (1, 1, 'thank_you',   'completed', 'Sent thank you email to Goldman recruiter.'),
    (2, 1, 'application', 'pending',   'Planning to apply for summer analyst role.'),
    (2, 2, 'interview',   'pending',   'Scheduled first-round interview with McKinsey.'),
    (3, 2, 'thank_you',   'pending',   'Need to send follow-up email to panel speakers.'),
    (1, 3, 'application', 'completed', 'Submitted JPMorgan online application.'),
    (7, 3, 'thank_you',   'pending',   'Need to email the JPMorgan contact from networking.'),
    (5, 4, 'application', 'pending',   'Planning to apply for Deloitte audit internship.'),
    (6, 4, 'thank_you',   'completed', 'Sent thank you note to Deloitte workshop presenter.'),
    (2, 5, 'application', 'pending',   'Applying for BlackRock analyst program.'),
    (9, 5, 'interview',   'pending',   'BlackRock first round scheduled for next week.');
