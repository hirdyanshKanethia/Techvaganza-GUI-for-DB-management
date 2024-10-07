import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import END
import mysql.connector
from mysql.connector import Error

import cv2
from pyzbar import pyzbar
import time


event_info = []

try:
    # Establish a connection
    connection = mysql.connector.connect(
        host='localhost',        # Replace with your host, e.g., 'localhost'
        database='techvaganza_test',  # Replace with your database name
        user='hirdyansh',      # Replace with your username
        password='hirdyansh10'    # Replace with your password
    )


except Error as e:
    print(f"Error: {e}")
    exit(0)



class IDVerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EVENT SELECTION")  # Set window title
        self.root.geometry("300x150")  # Set window size

        # Step 1: Create a label for instructions
        self.label = tk.Label(root, text="Enter your event ID:")
        self.label.pack(pady=10)  # Pack the label

        # Step 2: Create an entry box for user input
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=10)  # Pack the entry box

        # Step 3: Create a submit button
        self.submit_button = tk.Button(root, text="Verify ID", command=self.verify_id)
        self.submit_button.pack(pady=10)  # Pack the button

    def verify_id(self):
        global event_info
        global user_input

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events")
        events_data = cursor.fetchall()

        # Step 4: Get the user input
        user_input = self.entry.get()
        try:
            if user_input:  # Check if the entry is not empty
                for event in events_data:
                    if int(event[0]) == int(user_input):  
                        event_info = list(event)
                        root.destroy()
                        break
                else:
                    messagebox.show("Event ID not found", "Please enter a valid event ID.")
        except:
            messagebox.showerror("Event ID not found", "Please enter a valid event ID.")


# Step 5: Create the main window
root = tk.Tk()
app = IDVerificationApp(root)

# Step 6: Start the Tkinter event loop
root.mainloop()


std1 = []
std2 = []
table_data = []


cursor = connection.cursor()
cursor.execute(f"SELECT * FROM participating where eventid = {user_input}")
event_desc = cursor.fetchall()


# Function to open barcode scanner
def scan_barcode():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
        
    start_time = time.time()
    timeout = 30  # Timeout after 30 seconds
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Find barcodes in the frame
        barcodes = pyzbar.decode(frame)
        
        for barcode in barcodes:
            # Extract the barcode data
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            
            # Draw a rectangle around the barcode
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Put the barcode data and type on the image
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(frame, text, (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Release everything and return the barcode data
            cap.release()
            cv2.destroyAllWindows()
            verify_barcode(barcode_data)
            update_table()
        
        # Display the frame
        cv2.imshow('Barcode Scanner', frame)
        
        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Check for timeout
        if time.time() - start_time > timeout:
            messagebox.showerror("ERROR", "No barcode detected")
            break
    
    # Release everything if no barcode is found
    cap.release()
    cv2.destroyAllWindows()
    return None

# Function to verify and update the barcode input
def verify_barcode(barcode):
    cursor = connection.cursor()
    sql_query = '''SELECT * FROM attendees WHERE BandID = %s'''
    query_data = [barcode]
    try:
        cursor.execute(sql_query, query_data)
    except:
        messagebox.showinfo("Error", "Unexpected error occured")
        return 
    student_data = cursor.fetchall()
    # [(1, 'John', 'Doe', 'john.doe@email.com', '123-456-7890', 50001)] 
    if student_data == []:
        messagebox.showerror("ERROR", "Invalid Input")
        return
    sql_query = '''SELECT * FROM participating WHERE UserID = %s AND EventID = %s'''
    query_data = [student_data[0][0], user_input]
    cursor.execute(sql_query, query_data)

    attendance_data = cursor.fetchall()
    # [(1, 1, 1)]
    if attendance_data == []:
        messagebox.showerror("ERROR", "Invalid Input")
        return

    try:
        if int(attendance_data[0][2]) == 0:
            new_window = tk.Toplevel()
            new_window.title("STUDENT INFORMATION")
            new_window.geometry("500x400")  # Set window size (optional)

            def update_std_info():
                cursor = connection.cursor()
                update_query = f"""UPDATE participating
                                        SET attended = %s 
                                        WHERE UserID = %s
                                        AND EventID = %s"""
                std_data = (1, attendance_data[0][1], attendance_data[0][0])
                cursor.execute(update_query, std_data)
                try:
                    connection.commit()
                    messagebox.showinfo("Update Done", "Student Information has been updated")
                except Exception as e:
                    # Handle any other unexpected errors
                    messagebox.showerror("Error", f"An unexpected error occurred: {e}")
                    connection.rollback()
                update_table()



                new_window.destroy()

            # Configure grid layout for the new window
            new_window.grid_rowconfigure(0, weight=1)
            new_window.grid_rowconfigure(1, weight=1)
            new_window.grid_rowconfigure(2, weight=1)
            new_window.grid_rowconfigure(3, weight=1)
            new_window.grid_rowconfigure(4, weight=1)                        
            new_window.grid_rowconfigure(5, weight=1)
            new_window.grid_columnconfigure(0, weight=1)
            new_window.grid_columnconfigure(1, weight=1)

            # Create three label boxes for text in the top rows
            label1 = tk.Label(new_window, text=f"Student UserID: {attendance_data[0][1]}")
            label1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            label2 = tk.Label(new_window, text=f"Student BandID: {student_data[0][5]}")
            label2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            label3 = tk.Label(new_window, text= f"Student Name: {student_data[0][1]} {student_data[0][2]}")
            label3.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            label4 = tk.Label(new_window, text= "Student has not entered/participated the event yet")
            label4.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


            button1 = tk.Button(new_window, text="Mark student as participated/entered", command=update_std_info)
            button1.grid(row=4, column=0, padx=10, pady=10, sticky = 'e')

        elif int(attendance_data[0][2]) == 1:
            new_window = tk.Toplevel()
            new_window.title("STUDENT INFORMATION")
            new_window.geometry("500x400")  # Set window size (optional)

            # Configure grid layout for the new window
            new_window.grid_rowconfigure(0, weight=1)
            new_window.grid_rowconfigure(1, weight=1)
            new_window.grid_rowconfigure(2, weight=1)
            new_window.grid_rowconfigure(3, weight=1)
            new_window.grid_rowconfigure(4, weight=1)
            new_window.grid_columnconfigure(0, weight=1)
            new_window.grid_columnconfigure(1, weight=1)

            # Create three label boxes for text in the top rows
            label1 = tk.Label(new_window, text=f"Student UserID: {attendance_data[0][1]}")
            label1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            label2 = tk.Label(new_window, text=f"Student BandID: {student_data[0][5]}")
            label2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            label3 = tk.Label(new_window, text= f"Student Name: {student_data[0][1]} {student_data[0][2]}")
            label3.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            label4 = tk.Label(new_window, text= "Student has already entered/participated the event")
            label4.grid(row=3, column=0, columnspan=2, padx=10, pady=10) 

            update_table()

    except:
        def add_participant():
            cursor = None
            new_window.destroy()
            cursor = connection.cursor()
            sql_query = '''INSERT INTO participating(EventID, UserID, attended)
                            VALUES (%s, %s, %s);'''
            query_data = [user_input, student_data[0][0], 1]
            cursor.execute(sql_query, query_data)
            try:
                connection.commit()
                cursor.fetchall()
                messagebox.showinfo("Update complete", f"Student {student_data[0][1]} {student_data[0][2]} is now registered to this event")
                update_table()
                new_window.destroy()
            except Error as e:
                connection.rollback()
                messagebox.showerror("ERROR", f"User could not be registered to the event {e}")
            
            
        new_window = tk.Toplevel()
        new_window.title("STUDENT INFORMATION")
        new_window.geometry("400x200")  # Set window size (optional)

        # Configure grid layout for the new window
        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_rowconfigure(1, weight=1)
        new_window.grid_rowconfigure(2, weight=1)
        new_window.grid_rowconfigure(3, weight=1)
        new_window.grid_rowconfigure(4, weight=1)
        new_window.grid_columnconfigure(0, weight=1)
        new_window.grid_columnconfigure(1, weight=1)

        # Create three label boxes for text in the top rows
        label1 = tk.Label(new_window, text=f"Student BandID: {barcode}, Name: {student_data[0][1]} {student_data[0][2]} not registered in this event")
        label1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        add_participant_button = tk.Button(new_window, text="Add Student to this event", command=add_participant)
        add_participant_button.grid(row=4, column=0, columnspan=2, pady=20)

# Function to get student data from table
def getTableData():
        global std1
        global std2
        global table_data
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM participating WHERE EventID = {user_input} and attended = 0")
        std1 = cursor.fetchall()
        std1 = list(std1)

        cursor.execute(f"SELECT * FROM participating WHERE EventID = {user_input} and attended = 1")
        std2 = cursor.fetchall()
        std2 = list(std2)

# Function to exit the application
def exit_app():
    root.destroy()  # Close the Tkinter window

# Function to create or update table data
def update_table():
        global std1, std2, table_data
        getTableData()

        names_std1 = []
        names_std2 = []
        attendance_info_std1 = []
        attendance_info_std2 = []

        for data in std1:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM attendees WHERE UID = {data[1]} AND BandID IS NOT NULL")
            temp = cursor.fetchall()
            names_std1.append(temp)

        for data in std2:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM attendees WHERE UID = {data[1]} AND BandID IS NOT NULL")
            temp = cursor.fetchall()
            names_std2.append(temp)

        for student in names_std1:
            for data in std1:
                try: 
                    if student[0][0] == data[1]:
                        temp = (f"{student[0][1]} {student[0][2]}", student[0][5])
                        attendance_info_std1.append(temp)
                        break
                except:
                    continue

        for student in names_std2:
            for data in std2:
                try: 
                    if student[0][0] == data[1]:
                        temp = (f"{student[0][1]} {student[0][2]}", student[0][5])
                        attendance_info_std2.append(temp)
                        break
                except:
                    continue


        # Clearing the contents of the entry box
        entry.delete(0, END)

        # Clear existing content
        for widget in item_frame.winfo_children():
            widget.destroy()

        # Redraw the table
        for index, row in enumerate(attendance_info_std1, start=1):
            st_id1 = row[0]
            st_name1 = row[1]

            item_id_label = tk.Label(item_frame, text=str(st_id1), bg="light grey")
            item_id_label.grid(row=index, column=1, padx=(0,20), pady=5, sticky = 'w')

            item_name_label = tk.Label(item_frame, text=str(st_name1), bg="light grey")
            item_name_label.grid(row=index, column=2, padx=(20, 60), pady=5, sticky = 'e')
        
        item_id_label = tk.Label(item_frame, text="                 ", bg="light grey")
        item_id_label.grid(row=len(std1)+1, column=1, padx=(0,20), pady=5, sticky = 'w')

        item_name_label = tk.Label(item_frame, text="                   ", bg="light grey")
        item_name_label.grid(row=len(std1)+1, column=2, padx=(20, 60), pady=5, sticky = 'e')
            
        for index, row in enumerate(attendance_info_std2, start=1):
            st_id1 = row[0]
            st_name1 = row[1]

            item_id_label = tk.Label(item_frame, text=str(st_id1), bg="light grey")
            item_id_label.grid(row=index, column=3, padx=(100, 10), pady=5, sticky = 'w')

            item_name_label = tk.Label(item_frame, text=str(st_name1), bg="light grey")
            item_name_label.grid(row=index, column=4, padx=(10, 10), pady=5, sticky = 'e')

        item_id_label = tk.Label(item_frame, text=" ", bg="light grey")
        item_id_label.grid(row=len(std2)+1, column=3, padx=(100, 10), pady=5, sticky = 'w')

        item_name_label = tk.Label(item_frame, text=" ", bg="light grey")
        item_name_label.grid(row=len(std2)+1, column=4, padx=(10, 10), pady=5, sticky = 'e')

        # Update the canvas scroll region
        canvas.configure(scrollregion=canvas.bbox("all"))

# Function to verify the entered uid
def verify_uid(uid):
    cursor = connection.cursor()
    sql_query = '''SELECT * FROM attendees WHERE UID = %s'''
    query_data = [uid]
    try:
        cursor.execute(sql_query, query_data)
    except:
        messagebox.showinfo("Error", "Unexpected error occured")
        return 
    
    student_data = cursor.fetchall()
    # [(1, 'John', 'Doe', 'john.doe@email.com', '123-456-7890', 50001)] 
    if student_data == []:
        messagebox.showerror("ERROR", "Invalid Input")
        return
    sql_query = '''SELECT * FROM participating WHERE UserID = %s AND EventID = %s'''
    query_data = [uid, user_input]
    cursor.execute(sql_query, query_data)

    attendance_data = cursor.fetchall()
    # [(1, 1, 1)]
    if attendance_data == []:
        messagebox.showerror("ERROR", "Invalid Input")
        return
    try:
        if int(attendance_data[0][2]) == 0:
            new_window = tk.Toplevel()
            new_window.title("STUDENT INFORMATION")
            new_window.geometry("500x400")  # Set window size (optional)

            def update_std_info():
                cursor = connection.cursor()
                update_query = f"""UPDATE participating
                                        SET attended = %s 
                                        WHERE UserID = %s
                                        AND EventID = %s"""
                std_data = (1, attendance_data[0][1], attendance_data[0][0])
                cursor.execute(update_query, std_data)
                try:
                    connection.commit()
                    update_table()
                    messagebox.showinfo("Update Done", "Student Information has been updated")
                except Exception as e:
                    # Handle any other unexpected errors
                    messagebox.showerror("Error", f"An unexpected error occurred: {e}")
                    connection.rollback()

                new_window.destroy()

            # Configure grid layout for the new window
            new_window.grid_rowconfigure(0, weight=1)
            new_window.grid_rowconfigure(1, weight=1)
            new_window.grid_rowconfigure(2, weight=1)
            new_window.grid_rowconfigure(3, weight=1)
            new_window.grid_rowconfigure(4, weight=1)                        
            new_window.grid_rowconfigure(5, weight=1)
            new_window.grid_columnconfigure(0, weight=1)
            new_window.grid_columnconfigure(1, weight=1)

            # Create three label boxes for text in the top rows
            label1 = tk.Label(new_window, text=f"Student UserID: {uid}")
            label1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            label2 = tk.Label(new_window, text=f"Student BandID: {student_data[0][5]}")
            label2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            label3 = tk.Label(new_window, text= f"Student Name: {student_data[0][1]} {student_data[0][2]}")
            label3.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            label4 = tk.Label(new_window, text= "Student has not entered/participated the event yet")
            label4.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


            button1 = tk.Button(new_window, text="Mark student as participated/entered", command=update_std_info)
            button1.grid(row=4, column=0, padx=10, pady=10, sticky = 'e')

        elif int(attendance_data[0][2]) == 1:
            new_window = tk.Toplevel()
            new_window.title("STUDENT INFORMATION")
            new_window.geometry("500x400")  # Set window size (optional)

            # Configure grid layout for the new window
            new_window.grid_rowconfigure(0, weight=1)
            new_window.grid_rowconfigure(1, weight=1)
            new_window.grid_rowconfigure(2, weight=1)
            new_window.grid_rowconfigure(3, weight=1)
            new_window.grid_rowconfigure(4, weight=1)
            new_window.grid_columnconfigure(0, weight=1)
            new_window.grid_columnconfigure(1, weight=1)

            # Create three label boxes for text in the top rows
            label1 = tk.Label(new_window, text=f"Student UserID: {attendance_data[0][1]}")
            label1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            label2 = tk.Label(new_window, text=f"Student BandID: {student_data[0][5]}")
            label2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            label3 = tk.Label(new_window, text= f"Student Name: {student_data[0][1]} {student_data[0][2]}")
            label3.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            label4 = tk.Label(new_window, text= "Student has already entered/participated the event")
            label4.grid(row=3, column=0, columnspan=2, padx=10, pady=10) 

            update_table()

    except:
        def add_participant():
            cursor = None
            new_window.destroy()
            cursor = connection.cursor()
            sql_query = '''INSERT INTO participating(EventID, UserID, attended)
                            VALUES (%s, %s, %s);'''
            query_data = [user_input, student_data[0][0], 1]
            cursor.execute(sql_query, query_data)
            try:
                connection.commit()
                cursor.fetchall()
                messagebox.showinfo("Update complete", f"Student {student_data[0][1]} {student_data[0][2]} is now registered to this event")
                update_table()
                new_window.destroy()
            except Error as e:
                connection.rollback()
                messagebox.showerror("ERROR", f"User could not be registered to the event {e}")
            
            
        new_window = tk.Toplevel()
        new_window.title("STUDENT INFORMATION")
        new_window.geometry("400x200")  # Set window size (optional)

        # Configure grid layout for the new window
        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_rowconfigure(1, weight=1)
        new_window.grid_rowconfigure(2, weight=1)
        new_window.grid_rowconfigure(3, weight=1)
        new_window.grid_rowconfigure(4, weight=1)
        new_window.grid_columnconfigure(0, weight=1)
        new_window.grid_columnconfigure(1, weight=1)

        # Create three label boxes for text in the top rows
        label1 = tk.Label(new_window, text=f"Student UID: {uid}, Name: {student_data[0][1]} {student_data[0][2]} not registered in this event")
        label1.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        add_participant_button = tk.Button(new_window, text="Add Student to this event", command=add_participant)
        add_participant_button.grid(row=4, column=0, columnspan=2, pady=20)


if connection.is_connected():
    getTableData()
    # Create the main window
    root = tk.Tk()
    root.title(f"Barcode Scanner for {event_info[1]}")
    root.geometry("800x400")
    
    # Configure grid layout for the main window
    for row in range(5):
        root.grid_rowconfigure(row, weight=1)
    for col in range(5):
        root.grid_columnconfigure(col, weight=1)
    
    # Create visible grid frames
    for row in range(5):
        for col in range(5):
            frame = tk.Frame(root, borderwidth=1, relief="solid", bg="light gray")
            frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            
            # Add label to show grid coordinates (optional, for debugging)
            tk.Label(frame, bg="light gray").place(relx=0.5, rely=0.5, anchor="center")
    
    # Headers
    header1 = tk.Label(root, text="NOT ATTENDED", font=("Arial", 10, "bold"), bg="white")
    header1.grid(row=0, column=0, padx=(15,0), pady=5, sticky="w")
    
    header3 = tk.Label(root, text="ATTENDED", font=("Arial", 10, "bold"), bg="white")
    header3.grid(row=0, column=1, padx=(50,0), pady=5, sticky="e")
    
    # Exit button
    exit_button = tk.Button(root, text="Exit", command=exit_app, width=10)
    exit_button.grid(row=0, column=4, padx=10, pady=5, sticky="ne")
    
    # Scrollable area
    scrollable_frame = tk.Frame(root)
    scrollable_frame.grid(row=1, column=0, columnspan=3, rowspan=3, padx=10, pady=5, sticky="nsew")
    
    canvas = tk.Canvas(scrollable_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    item_frame = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=item_frame, anchor="nw")
    
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    item_frame.bind("<Configure>", configure_scroll_region)
    
    # Right side controls
    control_frame = tk.Frame(root)
    control_frame.grid(row=1, column=3, columnspan=2, rowspan=2, padx=10, pady=5, sticky="nsew")
    
    label = tk.Label(control_frame, text="Enter the BARCODE", font=("Arial", 10, "bold"))
    label.pack(pady=10)
    
    entry = tk.Entry(control_frame, width=30)
    entry.pack(pady=10)
    
    submit_button = tk.Button(control_frame, text="Verify", command=lambda: verify_barcode(entry.get()), width=15)
    submit_button.pack(pady=5)
    
    scan_button = tk.Button(control_frame, text="Scan Barcode", command=scan_barcode, width=15)
    scan_button.pack(pady=5)

    webcam_info = tk.Label(control_frame, text="(Press 'q' to exit webcam window)", font=("Arial", 8, "italic"))
    webcam_info.pack()
    
    bottom_frame = tk.Frame(root)
    bottom_frame.grid(row=3, column=3, columnspan=2, padx=10, pady=5, sticky="nsew")

    bottom_label = tk.Label(bottom_frame, text="Enter UID here:", font=("Arial", 10, "bold"))
    bottom_label.pack(anchor="w")

    bottom_entry = tk.Entry(bottom_frame, width=25)
    bottom_entry.pack(fill=tk.X, expand=True, pady=2, )

    action_button = tk.Button(bottom_frame, text="Verify", command=lambda: verify_uid(bottom_entry.get()))
    action_button.pack(pady=5)
    
    update_table()
    root.mainloop()

if connection.is_connected():
    connection.close()