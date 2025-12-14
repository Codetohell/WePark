# WePark Startup Guide 🚀

To get the entire system running from scratch, you should follow this specific order. This ensures that each component has what it needs (database, message broker, etc.) before it starts.

## 1. Infrastructure First (The Foundation)
**Why?** The backend and workers will crash or throw errors if they can't find Redis or the Email server.

### Step 1: Redis Server
*The Message Broker & Cache*
Check if it's running:
```bash
redis-cli ping
# If it says "PONG", you are good.
# If not, start it:
sudo service redis-server start
```

### Step 2: MailHog
*The Fake Email Server*
This catches all emails sent by the system so they don't go to real people.
```bash
./mailhog
```
*   **View Inbox:** [http://localhost:8025](http://localhost:8025)

---

## 2. The Application Core

### Step 3: Backend API
*The Brain*
Now that Redis and MailHog are up, the backend can connect to them.
```bash
cd backend
python run.py
```
*   **API Status:** [http://localhost:1437](http://localhost:1437)

---

## 3. Background Workers

### Step 4: Celery Worker
*The Muscle*
This listens to Redis for tasks (like "send email" or "export CSV") and executes them.
```bash
cd backend
celery -A run.celery worker --loglevel=info
```

### Step 5: Celery Beat
*The Clock*
This schedules periodic tasks (like "Daily Reminder at 5 PM") and adds them to the queue.
```bash
cd backend
celery -A run.celery beat --loglevel=info
```

---

## 4. The User Interface

### Step 6: Frontend
*The Face*
Finally, start the UI that users interact with.
```bash
cd frontend
npm run dev
```
*   **App URL:** [http://localhost:5173](http://localhost:5173)

---

## 🎯 Summary of Tabs
You will have 5 terminal tabs open:
1.  **MailHog**: `./mailhog`
2.  **Backend**: `cd backend && python run.py`
3.  **Worker**: `cd backend && celery -A run.celery worker --loglevel=info`
4.  **Beat**: `cd backend && celery -A run.celery beat --loglevel=info`
5.  **Frontend**: `cd frontend && npm run dev`
