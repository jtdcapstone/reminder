import streamlit as st
from datetime import datetime, time, date
from pytz import timezone, utc
from threading import Timer
import plyer

# In-memory storage for reminders
reminders = []

# Reminder class to hold reminder information
class Reminder:
    def __init__(self, text, date_time):
        self.text = text
        self.date_time = date_time

# Function to add a reminder
def add_reminder(reminder):
    reminders.append(reminder)

# Function to list reminders
def list_reminders():
    return reminders

# Function to remove a reminder
def remove_reminder(reminder):
    reminders.remove(reminder)

# Function to edit a reminder
def edit_reminder(old_reminder, new_text, new_date_time):
    old_reminder.text = new_text
    old_reminder.date_time = new_date_time

# Function to send notification for a reminder
#def send_notification(reminder):
    #st.success(f"Reminder: {reminder.text} at {reminder.date_time}")
    

# Function to send notification for a reminder
def send_notification(reminder):
    plyer.notification.notify(
        title="Reminder",
        message=f"{reminder.text} at {reminder.date_time}",
        timeout=10  # Notification timeout in seconds
    )

# Streamlit UI
def main():
    st.title("Reminder System")

    # Sidebar for adding reminders
    with st.sidebar:
        st.header("Add Reminder")
        reminder_input = st.text_input("Enter your reminder:")
        reminder_date = st.date_input("Reminder date:")
        reminder_time = st.time_input("Reminder time:")
        reminder_datetime = datetime.combine(reminder_date, reminder_time)
        if st.button("Add"):
            if reminder_input:
                reminder = Reminder(reminder_input, reminder_datetime)
                add_reminder(reminder)
                st.success("Reminder added successfully!")
            else:
                st.warning("Please enter a reminder!")

    # Main content to list, edit, and delete reminders
    st.header("Your Reminders")
    all_reminders = list_reminders()
    if all_reminders:
        for idx, reminder in enumerate(all_reminders, start=1):
            st.write(f"{idx}. {reminder.text} - {reminder.date_time}")
            # Edit and delete options
            edit_text = st.text_input("Edit reminder:")
            edit_date = st.date_input("Edit date:")
            edit_time = st.time_input("Edit time:")
            edit_datetime = datetime.combine(edit_date, edit_time)
            if st.button("Edit"):
                edit_reminder(reminder, edit_text, edit_datetime)
                st.success("Reminder edited successfully!")
            if st.button("Delete"):
                remove_reminder(reminder)
                st.success("Reminder deleted successfully!")
    else:
        st.write("No reminders set yet.")

    # Send notifications for reminders at their scheduled time
    now = datetime.now(utc)  # Get current time in UTC
    for reminder in all_reminders:
        reminder_time_utc = reminder.date_time.replace(tzinfo=utc)  # Make reminder datetime timezone-aware
        reminder_time_local = reminder_time_utc.astimezone(timezone('US/Pacific'))  # Convert to local timezone
        if now >= reminder_time_local:
            send_notification(reminder)




if __name__ == "__main__":
    main()
