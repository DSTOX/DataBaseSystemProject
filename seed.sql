-- Seed data for Campus Recruiting and Finance Event Management System

INSERT INTO COMPANY (name, industry, website) VALUES
    ('Goldman Sachs',   'Finance',    'https://www.goldmansachs.com'),
    ('McKinsey & Co',   'Consulting', 'https://www.mckinsey.com'),
    ('JPMorgan Chase',  'Finance',    'https://www.jpmorganchase.com'),
    ('Deloitte',        'Consulting', 'https://www.deloitte.com'),
    ('BlackRock',       'Finance',    'https://www.blackrock.com');

INSERT INTO ORGANIZER (full_name, email, role) VALUES
    ('Priya Sharma',   'psharma@university.edu',   'Finance Club President'),
    ('Marcus Lee',     'mlee@university.edu',       'Career Events Coordinator'),
    ('Aisha Johnson',  'ajohnson@university.edu',   'Club Vice President');

INSERT INTO STUDENT (full_name, email, major, graduation_year) VALUES
    ('Dev Gajjar',      'dgajjar@student.edu',   'Computer Science',    2026),
    ('Emily Chen',      'echen@student.edu',      'Finance',             2025),
    ('James Okafor',    'jokafor@student.edu',    'Business Analytics',  2026),
    ('Sofia Martinez',  'smartinez@student.edu',  'Accounting',          2027),
    ('Liam Patel',      'lpatel@student.edu',     'Computer Science',    2025),
    ('Nina Russo',      'nrusso@student.edu',     'Economics',           2026),
    ('Tyler Brooks',    'tbrooks@student.edu',    'Finance',             2027),
    ('Mia Nguyen',      'mnguyen@student.edu',    'Marketing',           2025);

INSERT INTO EVENT (title, event_type, event_date, location, capacity, description, company_id, organizer_id) VALUES
    ('Goldman Sachs Info Session',         'info_session', '2025-04-10', 'Business Building 201', 3, 'Learn about summer analyst roles at Goldman Sachs.',              1, 1),
    ('McKinsey Consulting Panel',          'panel',        '2025-04-15', 'Student Center Room A',  5, 'Panel discussion with McKinsey consultants.',                     2, 2),
    ('JPMorgan Networking Night',          'networking',   '2025-04-20', 'Campus Ballroom',         10,'Informal networking with JPMorgan representatives.',             3, 3),
    ('Deloitte Resume Workshop',           'workshop',     '2025-04-25', 'Library Conference Rm',   8, 'Resume review and interview tips from Deloitte recruiters.',     4, 1),
    ('BlackRock Investment Info Session',  'info_session', '2025-05-01', 'Business Building 101',   4, 'Overview of BlackRock full-time and internship opportunities.',  5, 2);

-- RSVPs (event 1 capacity=3, will be full to demo waitlist)
INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES
    (1, 1, 'confirmed'),
    (2, 1, 'confirmed'),
    (3, 1, 'confirmed'),
    (2, 2, 'confirmed'),
    (3, 2, 'confirmed'),
    (1, 3, 'confirmed'),
    (4, 3, 'confirmed'),
    (5, 4, 'confirmed'),
    (6, 4, 'confirmed');

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
    (3, 2, TRUE,  '2025-04-15 17:03:00');

-- Follow-up records
INSERT INTO FOLLOW_UP (student_id, event_id, followup_type, status, notes) VALUES
    (1, 1, 'thank_you',   'completed', 'Sent thank you email to Goldman recruiter.'),
    (2, 1, 'application', 'pending',   'Planning to apply for summer analyst role.'),
    (2, 2, 'interview',   'pending',   'Scheduled first-round interview with McKinsey.'),
    (3, 2, 'thank_you',   'pending',   'Need to send follow-up email.');
