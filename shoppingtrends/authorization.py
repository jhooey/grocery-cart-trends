from globalmethods import ask_yes_no_question
import Tkinter as tk
import tkFont
import user

TITLE_FONT = ("Helvetica", 18, "bold")

class Authorzation(tk.Tk):
    def __init__(self, session, *args, **kwargs):
        
        self.session = session
        
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Register):
            frame = F(container, self)
            self.frames[F] = frame
            # put all of the pages in the same location; 
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, c):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.tkraise()


class Login(tk.Frame):
    
    #this variable will be set once a user has successfully logged in
    session_user = None
    
    def __init__(self, parent, controller):
        self.controller = controller
        
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="Shopping Cart Trends", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        
        #Create the Username field
        label_username = tk.Label(self, text="username")
        label_username.pack()
        self.username = tk.StringVar()
        tk.Entry(self, textvariable=self.username).pack()
        
        #Create the password field
        label_password = tk.Label(self, text="password")
        label_password.pack()
        self.password = tk.StringVar()
        tk.Entry(self, textvariable=self.password).pack()
        
        self.error_message = tk.StringVar()
        self.error_message.set("")
        
        label_error_message = tk.Label(
                                       self, 
                                       textvariable = self.error_message, 
                                       fg="red"
                                       )
        label_error_message.pack()
        
        
        login_btn = tk.Button(
                              self, 
                              text="Login", 
                              command=self._check_credentials
                              )
        login_btn.pack(pady=5)
        
        reg_btn = tk.Button(
                            self, 
                            text="Registration", 
                            command=lambda:self.controller.show_frame(Register)
                            )
        reg_btn.pack(pady=10)
        
    def _check_credentials(self):
        """
        Checks to see if the credentials match values pulled from the db
        """
        session_user = self.controller.session.query(user.User)\
                            .filter_by(username=self.username.get().lower())\
                             .first() 
        
        if session_user and session_user.check_pwd(self.password.get()):
            self.controller.session_user = session_user
            self.quit()
        else:
            self.username.set("")
            self.password.set("")
            self.error_message.set("Incorrect username or password")


class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
    
        #Create the First name field
        self.label_first_name = tk.Label(self, text="Enter your first name")
        self.label_first_name.pack()
        self.first_name = tk.StringVar()
        tk.Entry(self, textvariable=self.first_name).pack()
        
        #Create the Last name field
        self.label_last_name = tk.Label(self, text="Enter your last name")
        self.label_last_name.pack()
        self.last_name = tk.StringVar()
        tk.Entry(self, textvariable=self.last_name).pack()
    
        #Create the Username field
        self.label_username = tk.Label(self, text="Enter a desired username")
        self.label_username.pack()
        self.username = tk.StringVar()
        tk.Entry(self, textvariable=self.username).pack()
        
        #Create the password field
        self.label_password = tk.Label(self, text="Enter a password")
        self.label_password.pack()
        self.password = tk.StringVar()
        tk.Entry(self, textvariable=self.password).pack()
        
        #Create the confirm password field
        self.label_confirm_pwd = tk.Label(self, text="confirm password")
        self.label_confirm_pwd.pack()
        self.confirm_pwd = tk.StringVar()
        tk.Entry(self, textvariable=self.confirm_pwd).pack()
        
        self.error_message = tk.StringVar()
        self.error_message.set("")
    
        self.label_error_message = tk.Label(
                                            self, 
                                            textvariable = self.error_message, 
                                            fg="red"
                                            )
        self.label_error_message.pack()
        
        
        button = tk.Button(self, text="Back to Login", 
                           command=lambda: controller.show_frame(Login))
        button.pack(pady=10)
    
def create_user(session):
    """Gathers the info necessary to create a new user"""
    print("What's your first name?")
    first_name = raw_input('> ')
    print("What's your last name?")
    last_name = raw_input('> ')
    print("What do you want as your username?")
    username = raw_input('> ')
    
    session.add(user.User(first_name, last_name, username))
    session.commit()