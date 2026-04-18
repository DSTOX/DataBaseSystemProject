from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'campus_recruiting_secret')

DB_NAME = os.getenv('DB_NAME', 'campus_recruiting')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')

# helper to run queries without repeating connection logic every time
def query(sql, params=(), fetchone=False, fetchall=False, commit=False):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    conn.autocommit = False
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql, params)
    result = None
    if fetchone:
        result = cur.fetchone()
    elif fetchall:
        result = cur.fetchall()
    if commit:
        conn.commit()
    cur.close()
    conn.close()
    return result


@app.route('/')
def index():
    event_count = query("SELECT COUNT(*) FROM EVENT", fetchone=True)[0]
    student_count = query("SELECT COUNT(*) FROM STUDENT", fetchone=True)[0]
    rsvp_count = query("SELECT COUNT(*) FROM RSVP WHERE rsvp_status = 'confirmed'", fetchone=True)[0]
    waitlist_count = query("SELECT COUNT(*) FROM WAITLIST", fetchone=True)[0]
    return render_template('index.html',
                           event_count=event_count,
                           student_count=student_count,
                           rsvp_count=rsvp_count,
                           waitlist_count=waitlist_count)


# --- companies ---

@app.route('/companies')
def companies():
    all_companies = query("SELECT * FROM COMPANY ORDER BY name", fetchall=True)
    return render_template('companies/list.html', companies=all_companies)

@app.route('/companies/new', methods=['GET', 'POST'])
def new_company():
    if request.method == 'POST':
        query("INSERT INTO COMPANY (name, industry, website) VALUES (%s, %s, %s)",
              (request.form['name'], request.form['industry'], request.form['website']),
              commit=True)
        flash('Company added.')
        return redirect(url_for('companies'))
    return render_template('companies/form.html', company=None)

@app.route('/companies/<int:company_id>/edit', methods=['GET', 'POST'])
def edit_company(company_id):
    if request.method == 'POST':
        query("UPDATE COMPANY SET name=%s, industry=%s, website=%s WHERE company_id=%s",
              (request.form['name'], request.form['industry'], request.form['website'], company_id),
              commit=True)
        flash('Company updated.')
        return redirect(url_for('companies'))
    company = query("SELECT * FROM COMPANY WHERE company_id = %s", (company_id,), fetchone=True)
    return render_template('companies/form.html', company=company)

@app.route('/companies/<int:company_id>/delete', methods=['POST'])
def delete_company(company_id):
    query("DELETE FROM COMPANY WHERE company_id = %s", (company_id,), commit=True)
    flash('Company deleted.')
    return redirect(url_for('companies'))


# --- organizers ---

@app.route('/organizers')
def organizers():
    all_organizers = query("SELECT * FROM ORGANIZER ORDER BY full_name", fetchall=True)
    return render_template('organizers/list.html', organizers=all_organizers)

@app.route('/organizers/new', methods=['GET', 'POST'])
def new_organizer():
    if request.method == 'POST':
        query("INSERT INTO ORGANIZER (full_name, email, role) VALUES (%s, %s, %s)",
              (request.form['full_name'], request.form['email'], request.form['role']),
              commit=True)
        flash('Organizer added.')
        return redirect(url_for('organizers'))
    return render_template('organizers/form.html', organizer=None)

@app.route('/organizers/<int:organizer_id>/edit', methods=['GET', 'POST'])
def edit_organizer(organizer_id):
    if request.method == 'POST':
        query("UPDATE ORGANIZER SET full_name=%s, email=%s, role=%s WHERE organizer_id=%s",
              (request.form['full_name'], request.form['email'], request.form['role'], organizer_id),
              commit=True)
        flash('Organizer updated.')
        return redirect(url_for('organizers'))
    organizer = query("SELECT * FROM ORGANIZER WHERE organizer_id = %s", (organizer_id,), fetchone=True)
    return render_template('organizers/form.html', organizer=organizer)

@app.route('/organizers/<int:organizer_id>/delete', methods=['POST'])
def delete_organizer(organizer_id):
    query("DELETE FROM ORGANIZER WHERE organizer_id = %s", (organizer_id,), commit=True)
    flash('Organizer deleted.')
    return redirect(url_for('organizers'))


# --- students ---

@app.route('/students')
def students():
    all_students = query("SELECT * FROM STUDENT ORDER BY full_name", fetchall=True)
    return render_template('students/list.html', students=all_students)

@app.route('/students/new', methods=['GET', 'POST'])
def new_student():
    if request.method == 'POST':
        query("INSERT INTO STUDENT (full_name, email, major, graduation_year) VALUES (%s, %s, %s, %s)",
              (request.form['full_name'], request.form['email'],
               request.form['major'], request.form['graduation_year']),
              commit=True)
        flash('Student added.')
        return redirect(url_for('students'))
    return render_template('students/form.html', student=None)

@app.route('/students/<int:student_id>')
def student_detail(student_id):
    student = query("SELECT * FROM STUDENT WHERE student_id = %s", (student_id,), fetchone=True)

    # get all events this student RSVPed for
    rsvps = query("""
        SELECT e.title, e.event_date, e.event_type, c.name AS company_name,
               r.rsvp_status, r.created_at
        FROM RSVP r
        JOIN EVENT e ON r.event_id = e.event_id
        LEFT JOIN COMPANY c ON e.company_id = c.company_id
        WHERE r.student_id = %s
        ORDER BY e.event_date DESC
    """, (student_id,), fetchall=True)

    attendance = query("""
        SELECT e.title, e.event_date, a.attended_flag, a.checkin_time
        FROM ATTENDANCE a
        JOIN EVENT e ON a.event_id = e.event_id
        WHERE a.student_id = %s
        ORDER BY e.event_date DESC
    """, (student_id,), fetchall=True)

    followups = query("""
        SELECT f.followup_type, f.status, f.notes, f.created_at, e.title AS event_title
        FROM FOLLOW_UP f
        JOIN EVENT e ON f.event_id = e.event_id
        WHERE f.student_id = %s
        ORDER BY f.created_at DESC
    """, (student_id,), fetchall=True)

    return render_template('students/detail.html',
                           student=student,
                           rsvps=rsvps,
                           attendance=attendance,
                           followups=followups)

@app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        query("UPDATE STUDENT SET full_name=%s, email=%s, major=%s, graduation_year=%s WHERE student_id=%s",
              (request.form['full_name'], request.form['email'],
               request.form['major'], request.form['graduation_year'], student_id),
              commit=True)
        flash('Student updated.')
        return redirect(url_for('students'))
    student = query("SELECT * FROM STUDENT WHERE student_id = %s", (student_id,), fetchone=True)
    return render_template('students/form.html', student=student)

@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    query("DELETE FROM STUDENT WHERE student_id = %s", (student_id,), commit=True)
    flash('Student deleted.')
    return redirect(url_for('students'))


# --- events ---

@app.route('/events')
def events():
    search = request.args.get('search', '').strip()
    event_type = request.args.get('event_type', '').strip()

    sql = """
        SELECT e.*, c.name AS company_name,
               COUNT(CASE WHEN r.rsvp_status = 'confirmed' THEN 1 END) AS confirmed_count
        FROM EVENT e
        LEFT JOIN COMPANY c ON e.company_id = c.company_id
        LEFT JOIN RSVP r ON e.event_id = r.event_id
        WHERE 1=1
    """
    params = []

    if search:
        sql += " AND (e.title ILIKE %s OR c.name ILIKE %s)"
        params += ['%' + search + '%', '%' + search + '%']
    if event_type:
        sql += " AND e.event_type = %s"
        params.append(event_type)

    sql += " GROUP BY e.event_id, c.name ORDER BY e.event_date"

    all_events = query(sql, params, fetchall=True)
    return render_template('events/list.html', events=all_events, search=search, event_type=event_type)

@app.route('/events/<int:event_id>')
def event_detail(event_id):
    event = query("""
        SELECT e.*, c.name AS company_name, o.full_name AS organizer_name
        FROM EVENT e
        LEFT JOIN COMPANY c ON e.company_id = c.company_id
        LEFT JOIN ORGANIZER o ON e.organizer_id = o.organizer_id
        WHERE e.event_id = %s
    """, (event_id,), fetchone=True)

    rsvps = query("""
        SELECT s.student_id, s.full_name, s.email, s.major, r.created_at
        FROM RSVP r
        JOIN STUDENT s ON r.student_id = s.student_id
        WHERE r.event_id = %s AND r.rsvp_status = 'confirmed'
        ORDER BY r.created_at
    """, (event_id,), fetchall=True)

    waitlist = query("""
        SELECT s.full_name, s.email, w.waitlist_position, w.joined_at
        FROM WAITLIST w
        JOIN STUDENT s ON w.student_id = s.student_id
        WHERE w.event_id = %s
        ORDER BY w.waitlist_position
    """, (event_id,), fetchall=True)

    attendance_summary = query("""
        SELECT
            COUNT(CASE WHEN attended_flag = TRUE THEN 1 END) AS attended,
            COUNT(CASE WHEN attended_flag = FALSE THEN 1 END) AS absent
        FROM ATTENDANCE
        WHERE event_id = %s
    """, (event_id,), fetchone=True)

    followups = query("""
        SELECT f.*, s.full_name AS student_name
        FROM FOLLOW_UP f
        JOIN STUDENT s ON f.student_id = s.student_id
        WHERE f.event_id = %s
        ORDER BY f.created_at DESC
    """, (event_id,), fetchall=True)

    all_students = query("SELECT * FROM STUDENT ORDER BY full_name", fetchall=True)

    return render_template('events/detail.html',
                           event=event,
                           rsvps=rsvps,
                           waitlist=waitlist,
                           attendance_summary=attendance_summary,
                           followups=followups,
                           all_students=all_students)

@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if request.method == 'POST':
        company_id = request.form['company_id'] or None
        organizer_id = request.form['organizer_id'] or None
        query("""INSERT INTO EVENT (title, event_type, event_date, location, capacity, description, company_id, organizer_id)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
              (request.form['title'], request.form['event_type'], request.form['event_date'],
               request.form['location'], request.form['capacity'], request.form['description'],
               company_id, organizer_id),
              commit=True)
        flash('Event created.')
        return redirect(url_for('events'))
    all_companies = query("SELECT * FROM COMPANY ORDER BY name", fetchall=True)
    all_organizers = query("SELECT * FROM ORGANIZER ORDER BY full_name", fetchall=True)
    return render_template('events/form.html', event=None, companies=all_companies, organizers=all_organizers)

@app.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    if request.method == 'POST':
        company_id = request.form['company_id'] or None
        organizer_id = request.form['organizer_id'] or None
        query("""UPDATE EVENT SET title=%s, event_type=%s, event_date=%s, location=%s,
                                  capacity=%s, description=%s, company_id=%s, organizer_id=%s
                 WHERE event_id=%s""",
              (request.form['title'], request.form['event_type'], request.form['event_date'],
               request.form['location'], request.form['capacity'], request.form['description'],
               company_id, organizer_id, event_id),
              commit=True)
        flash('Event updated.')
        return redirect(url_for('events'))
    event = query("SELECT * FROM EVENT WHERE event_id = %s", (event_id,), fetchone=True)
    all_companies = query("SELECT * FROM COMPANY ORDER BY name", fetchall=True)
    all_organizers = query("SELECT * FROM ORGANIZER ORDER BY full_name", fetchall=True)
    return render_template('events/form.html', event=event, companies=all_companies, organizers=all_organizers)

@app.route('/events/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    query("DELETE FROM EVENT WHERE event_id = %s", (event_id,), commit=True)
    flash('Event deleted.')
    return redirect(url_for('events'))


# --- rsvp + waitlist (advanced feature) ---

@app.route('/events/<int:event_id>/rsvp', methods=['POST'])
def rsvp(event_id):
    student_id = int(request.form['student_id'])

    # check if they already signed up or are on the waitlist
    existing = query("SELECT rsvp_status FROM RSVP WHERE student_id=%s AND event_id=%s",
                     (student_id, event_id), fetchone=True)
    on_waitlist = query("SELECT 1 FROM WAITLIST WHERE student_id=%s AND event_id=%s",
                        (student_id, event_id), fetchone=True)

    if existing:
        flash('This student already has an RSVP for this event.')
    elif on_waitlist:
        flash('This student is already on the waitlist.')
    else:
        event = query("SELECT capacity FROM EVENT WHERE event_id = %s", (event_id,), fetchone=True)
        confirmed = query("SELECT COUNT(*) FROM RSVP WHERE event_id=%s AND rsvp_status='confirmed'",
                          (event_id,), fetchone=True)[0]

        if confirmed < event['capacity']:
            query("INSERT INTO RSVP (student_id, event_id, rsvp_status) VALUES (%s, %s, 'confirmed')",
                  (student_id, event_id), commit=True)
            flash('RSVP confirmed!')
        else:
            # event is full so put them on the waitlist
            next_pos = query("SELECT COALESCE(MAX(waitlist_position), 0) + 1 FROM WAITLIST WHERE event_id=%s",
                             (event_id,), fetchone=True)[0]
            query("INSERT INTO WAITLIST (student_id, event_id, waitlist_position) VALUES (%s, %s, %s)",
                  (student_id, event_id, next_pos), commit=True)
            flash('Event is full. Student added to waitlist at position ' + str(next_pos) + '.')

    return redirect(url_for('event_detail', event_id=event_id))


@app.route('/events/<int:event_id>/cancel/<int:student_id>', methods=['POST'])
def cancel_rsvp(event_id, student_id):
    # deleting from RSVP fires the postgres trigger which promotes the next waitlisted student automatically
    query("DELETE FROM RSVP WHERE student_id=%s AND event_id=%s AND rsvp_status='confirmed'",
          (student_id, event_id), commit=True)
    flash('RSVP cancelled. The next student on the waitlist has been automatically promoted.')
    return redirect(url_for('event_detail', event_id=event_id))


# --- attendance ---

@app.route('/events/<int:event_id>/attendance', methods=['POST'])
def mark_attendance(event_id):
    student_id = int(request.form['student_id'])
    attended_flag = request.form.get('attended_flag') == 'on'
    checkin_time = request.form.get('checkin_time') or None

    # upsert so you can update attendance if you made a mistake
    query("""
        INSERT INTO ATTENDANCE (student_id, event_id, attended_flag, checkin_time)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (student_id, event_id)
        DO UPDATE SET attended_flag = EXCLUDED.attended_flag, checkin_time = EXCLUDED.checkin_time
    """, (student_id, event_id, attended_flag, checkin_time), commit=True)
    flash('Attendance updated.')
    return redirect(url_for('event_detail', event_id=event_id))


# --- follow-ups ---

@app.route('/followups')
def followups():
    all_followups = query("""
        SELECT f.*, s.full_name AS student_name, e.title AS event_title
        FROM FOLLOW_UP f
        JOIN STUDENT s ON f.student_id = s.student_id
        JOIN EVENT e ON f.event_id = e.event_id
        ORDER BY f.created_at DESC
    """, fetchall=True)
    return render_template('events/followups.html', followups=all_followups)

@app.route('/followups/new', methods=['POST'])
def new_followup():
    event_id = request.form['event_id']
    query("""INSERT INTO FOLLOW_UP (student_id, event_id, followup_type, status, notes)
             VALUES (%s, %s, %s, 'pending', %s)""",
          (request.form['student_id'], event_id,
           request.form['followup_type'], request.form['notes']),
          commit=True)
    flash('Follow-up added.')
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/followups/<int:followup_id>/update', methods=['POST'])
def update_followup(followup_id):
    query("UPDATE FOLLOW_UP SET status=%s, notes=%s WHERE followup_id=%s",
          (request.form['status'], request.form['notes'], followup_id), commit=True)
    flash('Follow-up updated.')
    return redirect(url_for('followups'))

@app.route('/followups/<int:followup_id>/delete', methods=['POST'])
def delete_followup(followup_id):
    query("DELETE FROM FOLLOW_UP WHERE followup_id = %s", (followup_id,), commit=True)
    flash('Follow-up deleted.')
    return redirect(url_for('followups'))


# --- reports ---

@app.route('/reports')
def reports():
    # how many students attended vs were absent per company
    attendance_by_company = query("""
        SELECT c.name AS company_name,
               COUNT(CASE WHEN a.attended_flag = TRUE THEN 1 END) AS attended,
               COUNT(CASE WHEN a.attended_flag = FALSE THEN 1 END) AS absent
        FROM COMPANY c
        JOIN EVENT e ON e.company_id = c.company_id
        LEFT JOIN ATTENDANCE a ON a.event_id = e.event_id
        GROUP BY c.name
        ORDER BY attended DESC
    """, fetchall=True)

    pending_followups = query("""
        SELECT s.full_name, s.email, COUNT(f.followup_id) AS pending_count
        FROM STUDENT s
        JOIN FOLLOW_UP f ON f.student_id = s.student_id
        WHERE f.status = 'pending'
        GROUP BY s.full_name, s.email
        ORDER BY pending_count DESC
    """, fetchall=True)

    # shows fill % for each event
    fill_rates = query("""
        SELECT e.title, e.capacity,
               COUNT(CASE WHEN r.rsvp_status = 'confirmed' THEN 1 END) AS confirmed,
               ROUND(100.0 * COUNT(CASE WHEN r.rsvp_status = 'confirmed' THEN 1 END) / e.capacity, 1) AS fill_pct
        FROM EVENT e
        LEFT JOIN RSVP r ON e.event_id = r.event_id
        GROUP BY e.event_id, e.title, e.capacity
        ORDER BY fill_pct DESC
    """, fetchall=True)

    # students who RSVPed but never showed up
    no_shows = query("""
        SELECT s.full_name, s.email, e.title AS event_title
        FROM RSVP r
        JOIN STUDENT s ON r.student_id = s.student_id
        JOIN EVENT e ON r.event_id = e.event_id
        LEFT JOIN ATTENDANCE a ON a.student_id = r.student_id AND a.event_id = r.event_id
        WHERE r.rsvp_status = 'confirmed'
          AND (a.attended_flag = FALSE OR a.attended_flag IS NULL)
        ORDER BY e.title, s.full_name
    """, fetchall=True)

    return render_template('events/reports.html',
                           attendance_by_company=attendance_by_company,
                           pending_followups=pending_followups,
                           fill_rates=fill_rates,
                           no_shows=no_shows)


if __name__ == '__main__':
    app.run(debug=True)
