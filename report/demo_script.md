# Demo Script — Campus Recruiting & Finance Event Management System
## 20-Minute Recorded Walkthrough

---

## BEFORE YOU HIT RECORD

- App is running at http://localhost:5000
- Browser is open to the home page
- Make your browser window large — full screen if possible
- Keep this script open on your phone or a second monitor
- Talk at a normal pace — you have 20 minutes, don't rush

---

## SECTION 1 — Introduction (2 minutes)

**[Screen: home page — http://localhost:5000]**

> "Hi, my name is Dev Gajjar and this is my database systems project —
> a Campus Recruiting and Finance Event Management System.
>
> The idea behind this app is pretty straightforward — on college campuses,
> finance and consulting clubs host a lot of recruiting events: info sessions,
> networking nights, panels, workshops. Right now most of that gets tracked
> in spreadsheets or group chats, which gets messy fast. So I built a web app
> backed by a PostgreSQL database to manage all of it in one place.
>
> The system tracks companies, organizers, students, events, RSVPs,
> attendance, and follow-up tasks. As you can see on the home page right now,
> we have 10 events, 10 students, 36 confirmed RSVPs, and 3 students on a
> waitlist in the database.
>
> I built this using Python and Flask for the backend, PostgreSQL 17 for
> the database, and plain HTML and CSS for the front end.
>
> I'll walk through all the basic functions first — insert, search, queries,
> update, and delete — and then show the advanced feature at the end."

---

## SECTION 2 — INSERT (4 minutes)

> "Let me start with inserting records. I'll add a new company, a new student,
> and then create a new event and RSVP that student to it."

**[Click: Companies in the nav bar]**

> "Here's the companies list — Goldman Sachs, JPMorgan, McKinsey and so on.
> I'll add a new one."

**[Click: + New Company]**

> "I'll add Citi as a new company."

**[Type in the form:]**
- Name: `Citigroup`
- Industry: `Finance`
- Website: `https://www.citi.com`

**[Click: Add Company]**

> "You can see it shows up in the list right away — that's a live insert
> into the COMPANY table in PostgreSQL."

**[Click: Students in the nav bar]**

> "Now I'll add a new student."

**[Click: + New Student]**

**[Type:]**
- Full Name: `Alex Turner`
- Email: `aturner@student.edu`
- Major: `Finance`
- Graduation Year: `2026`

**[Click: Add Student]**

> "Student added. Now let me create a new event for Citi and RSVP Alex to it."

**[Click: Events → + New Event]**

**[Type:]**
- Title: `Citi Sales & Trading Info Session`
- Type: `info_session`
- Date: `2025-06-05`
- Location: `Business Building 201`
- Capacity: `5`
- Description: `Overview of Citi sales and trading internship programs.`
- Company: select `Citigroup`
- Organizer: select any

**[Click: Create]**

> "Event created. Now let me go into that event and RSVP Alex to it."

**[Click on the new Citi event from the list]**

> "This is the event detail page. It shows all the confirmed RSVPs,
> the waitlist, attendance, and follow-up tasks. Right now it's empty
> because we just created it."

**[Under RSVP a Student — select Alex Turner → Click: Submit RSVP]**

> "Alex is now confirmed. You can see him show up in the RSVPs table
> with the timestamp. That's an insert into the RSVP table.
>
> I'll also log a follow-up task — let's say Alex needs to send a
> thank you email after this event."

**[Under Follow-Up Tasks — select Alex Turner, Type: thank_you, Notes: Send thank you to Citi recruiter → Click: Add Follow-Up]**

> "Follow-up logged. So in just a few clicks I've inserted records
> into four different tables — COMPANY, STUDENT, EVENT, RSVP, and FOLLOW_UP."

---

## SECTION 3 — SEARCH AND LIST (2 minutes)

> "Now let me show the search functionality."

**[Click: Events in the nav]**

> "On the events page I can search by event name or company name,
> and I can filter by event type."

**[Type 'Goldman' in the search box → Click: Search]**

> "That filters down to just the Goldman Sachs events. The SQL behind this
> uses an ILIKE query so it's case-insensitive — so 'goldman' lowercase
> would give the same result."

**[Clear the search → set Type filter to 'workshop' → Click: Search]**

> "Now I'm filtering to just workshops — Deloitte Resume Workshop,
> Morgan Stanley Finance Workshop, and the McKinsey Case Interview Workshop."

**[Click: Clear]**

> "And clear brings everything back. Let me also show the students list."

**[Click: Students]**

> "Students are listed alphabetically. Each name is a link — I'll click
> one to show the student detail page."

**[Click on any student name, e.g. Emily Chen]**

> "This pulls up Emily's full recruiting profile — every event she's RSVPed
> for, her attendance record, and any follow-up tasks. This query joins
> across RSVP, EVENT, COMPANY, ATTENDANCE, and FOLLOW_UP all at once."

---

## SECTION 4 — QUERIES: JOIN AND AGGREGATE (4 minutes)

> "Now I want to show the reporting queries, which are where the
> more interesting database work happens."

**[Click: Reports in the nav]**

> "The reports page runs four separate queries against the database.
> Let me walk through each one."

**[Point to Attendance by Company table]**

> "The first one is Attendance by Company. This is an aggregate query —
> it groups attendance records by company and counts how many students
> attended versus were absent. The SQL joins COMPANY, EVENT, and ATTENDANCE,
> then uses a GROUP BY with conditional COUNT to split attended and absent
> into separate columns.
>
> So for example Goldman Sachs had 2 attendees and 1 absent across their events."

**[Point to Event Fill Rates table]**

> "The fill rates query shows what percentage of capacity each event filled.
> This uses COUNT and ROUND with a GROUP BY on each event. Goldman Sachs
> Info Session is at 100% — it's completely full, which we'll come back to
> for the advanced feature."

**[Point to No-Shows table]**

> "The no-shows query is the most complex one — it joins four tables:
> RSVP, STUDENT, EVENT, and ATTENDANCE, using a LEFT JOIN on attendance
> so we can catch students who RSVPed confirmed but either never got
> marked as attended or were marked absent. This is useful for
> following up with students after events."

**[Point to Pending Follow-Ups table]**

> "And the last one counts pending follow-up tasks per student —
> another aggregate query with GROUP BY and COUNT, joining STUDENT and FOLLOW_UP."

---

## SECTION 5 — UPDATE (2 minutes)

> "Now let me show updating records."

**[Click: Students]**

**[Click Edit next to any student, e.g. Tyler Brooks]**

> "I'll update Tyler's major — let's say he switched from Finance to Economics."

**[Change Major field to `Economics` → Click: Update]**

> "Updated. Let me also show updating an event."

**[Click: Events → Click Edit on the Citi event we just created]**

> "I'll increase the capacity from 5 to 8."

**[Change capacity to 8 → Click: Update]**

> "And I can update a follow-up status too — let me go to the Follow-Ups page."

**[Click: Follow-Ups in the nav]**

> "Here are all the follow-up tasks across every event. I can update the
> status and notes inline."

**[Find any pending follow-up → change status to 'completed' → Click: Save]**

> "Status changed to completed. That's an UPDATE on the FOLLOW_UP table."

---

## SECTION 6 — DELETE (1 minute)

> "Deletes work the same way — let me quickly show a few."

**[Click: Companies]**

> "I'll delete the Citigroup company we added at the start."

**[Click Delete next to Citigroup → confirm]**

> "Deleted. The schema uses ON DELETE SET NULL on the EVENT table's company_id
> foreign key, so the Citi event we created still exists — it just no longer
> has a company linked to it. I designed it this way so you don't accidentally
> lose all your event records just because a company gets removed."

---

## SECTION 7 — ADVANCED FEATURE: WAITLIST AUTO-PROMOTION (4 minutes)

> "Now the advanced feature — the automatic waitlist promotion system.
>
> This was the most technically challenging part of the project, and it's
> implemented using a PostgreSQL trigger function.
>
> Here's the situation: some events have limited capacity. When an event
> fills up, new RSVPs automatically go to a waitlist with a numbered
> position. The challenge is: what happens when someone cancels?
> Someone has to get promoted off the waitlist into the confirmed spot —
> and that needs to happen automatically, atomically, without any manual
> steps."

**[Click: Events → Click on Goldman Sachs Info Session]**

> "Goldman Sachs Info Session has a capacity of 3. You can see it's
> completely full right now — Dev Gajjar, Emily Chen, and James Okafor
> are all confirmed. And down in the waitlist section, Sofia Martinez
> is position 1, Liam Patel is position 2, Nina Russo is position 3."

**[Scroll down to show the waitlist clearly]**

> "Watch what happens when I cancel one of the confirmed RSVPs."

**[Click Cancel next to Dev Gajjar → Confirm]**

> "Dev's RSVP is cancelled — and look at the waitlist. Sofia Martinez,
> who was position 1, is now gone from the waitlist and has a confirmed
> RSVP. Liam Patel moved from position 2 to position 1.
> Nina Russo moved from position 3 to position 2.
> All of that happened in one database operation — no extra button clicks,
> no manual promotion step."

**[Scroll to show RSVPs — Sofia should now appear as confirmed]**

> "So how does this work? I wrote a PostgreSQL trigger function called
> promote_from_waitlist. It fires AFTER a DELETE on the RSVP table.
>
> When it fires, it finds the student with the lowest waitlist_position
> for that event, inserts a confirmed RSVP for them, deletes them from
> the waitlist, and then decrements all remaining positions by 1 to
> close the gap — all in the same transaction.
>
> The reason I implemented this as a database trigger rather than in
> the Flask application code is that a trigger runs inside PostgreSQL
> and is guaranteed to execute atomically. If I had written this in Python,
> there would be a window between the delete and the insert where the data
> could be in an inconsistent state. The trigger eliminates that risk entirely.
>
> I'd argue this qualifies as an advanced function for three reasons:
> first, it's useful — users never have to manually manage a waitlist;
> second, it's technically challenging — it required learning PostgreSQL
> procedural language and trigger mechanics; and third, it's not something
> you see in basic CRUD apps — most applications either don't have a waitlist
> at all or handle it manually."

---

## SECTION 8 — WRAP UP (1 minute)

> "So to summarize what I've built: a full-stack web application using
> Flask and PostgreSQL with 8 database tables, complete CRUD for all
> entities, event search and filtering, four reporting queries including
> multi-table joins and aggregates, a student profile page that pulls
> recruiting history across multiple tables, and an automatic waitlist
> promotion system implemented as a PostgreSQL trigger.
>
> The code is available on GitHub — the link is in my report.
>
> That's the demo, thanks for watching."

---

## TIMING GUIDE

| Section | Target Time | Cumulative |
|---------|-------------|------------|
| Introduction | 2 min | 2 min |
| Insert | 4 min | 6 min |
| Search & List | 2 min | 8 min |
| Queries | 4 min | 12 min |
| Update | 2 min | 14 min |
| Delete | 1 min | 15 min |
| Advanced Feature | 4 min | 19 min |
| Wrap Up | 1 min | 20 min |

---

## THINGS TO KNOW IN CASE THE PROFESSOR ASKS

**"Why a trigger instead of handling it in Flask?"**
Triggers run inside PostgreSQL and are atomic — no window for inconsistency.
Python code between a delete and an insert could leave data in a bad state.

**"What happens if the waitlist is empty when someone cancels?"**
The trigger checks first with `SELECT student_id INTO next_student_id`.
If nothing is found, `next_student_id` is NULL and the trigger just exits
without doing anything. The cancel still goes through fine.

**"What tables are involved in the no-shows query?"**
RSVP, STUDENT, EVENT, and ATTENDANCE — four tables, three joins.

**"Why ON DELETE SET NULL for company on events?"**
So deleting a company doesn't cascade and wipe out all the events
associated with it. Events are a record of history.

**"What does ILIKE do?"**
Case-insensitive LIKE — a PostgreSQL-specific operator.
So searching "goldman" matches "Goldman Sachs".
