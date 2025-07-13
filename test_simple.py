import sys
import traceback

def main():
    print("Starting test application...")
    
    try:
        print("Importing tkinter...")
        import tkinter as tk
        print("Tkinter imported successfully!")
        
        print("Creating root window...")
        root = tk.Tk()
        root.title("Test App")
        root.geometry("300x200")
        
        print("Adding widgets...")
        label = tk.Label(root, text="Hello World!")
        label.pack(pady=50)
        
        button = tk.Button(root, text="Close", command=root.quit)
        button.pack()
        
        print("Starting mainloop...")
        root.mainloop()
        print("Application closed normally")
        
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()