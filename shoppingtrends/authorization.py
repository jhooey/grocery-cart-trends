from globalmethods import ask_yes_no_question
import Tkinter as tk
import ttk
import user

TITLE_FONT = ("Helvetica", 18, "bold")
BG_COLOR = "alice blue"

class Authorzation(tk.Tk):
    def __init__(self, session, *args, **kwargs):
        
        self.session = session
        
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ttk.Frame(self)
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
        
        self.configure(background=BG_COLOR)
        
        
        label = ttk.Label(
                          self, 
                          text="Shopping Cart Trends", 
                          font=TITLE_FONT, 
                          background=BG_COLOR
                          )
        label.pack(side="top", fill="x", pady=10)
        
        #Create the Username field
        label_username = ttk.Label(self, text="username", background=BG_COLOR)
        label_username.pack()
        self.username = tk.StringVar()
        tk.Entry(self, textvariable=self.username).pack()
        
        #Create the password field
        label_password = ttk.Label(self, text="password", background=BG_COLOR)
        label_password.pack()
        self.password = tk.StringVar()
        tk.Entry(self, textvariable=self.password).pack()
        
        self.error_message = tk.StringVar()
        self.error_message.set("")
        
        label_error_message = ttk.Label(
                                       self, 
                                       textvariable = self.error_message, 
                                       foreground="red",
                                       background=BG_COLOR
                                       )
        label_error_message.pack()
        
        
        login_btn = ttk.Button(
                              self, 
                              text="Login", 
                              command=self._check_credentials
                              )
        login_btn.pack(pady=5)
        
        reg_btn = ttk.Button(
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
        self.controller = controller
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text="Registration", font=TITLE_FONT)
        label.grid(row=0, columnspan=2, pady=10)
    
        #Create the First name field
        self.label_first_name = ttk.Label(self, text="Enter your first name")
        self.label_first_name.grid(row=1, column=0, padx=(15, 0), sticky='W')
        self.first_name = tk.StringVar()
        tk.Entry(self, textvariable=self.first_name).grid(
                                                          row=1, 
                                                          column=1, 
                                                          padx=(0,15)
                                                          )
        
        #Create the Last name field
        self.label_last_name = ttk.Label(self, text="Enter your last name")
        self.label_last_name.grid(row=2, column=0, padx=(15, 0), sticky='W')
        self.last_name = tk.StringVar()
        tk.Entry(self, textvariable=self.last_name).grid(
                                                         row=2, 
                                                         column=1, 
                                                         padx=(0,15)
                                                         )
    
        #Create the Username field
        self.label_username = ttk.Label(self, text="Enter a desired username")
        self.label_username.grid(row=3, column=0, padx=(15, 0), sticky='W')
        self.username = tk.StringVar()
        tk.Entry(self, textvariable=self.username).grid(
                                                        row=3, 
                                                        column=1, 
                                                        padx=(0,15)
                                                        )
        
        #Create the password field
        self.label_password = ttk.Label(self, text="Enter a password")
        self.label_password.grid(row=4, column=0, padx=(15, 0), sticky='W')
        self.password = tk.StringVar()
        tk.Entry(self, textvariable=self.password).grid(
                                                        row=4, 
                                                        column=1, 
                                                        padx=(0,15)
                                                        )
        
        #Create the confirm password field
        self.label_confirm_pwd = ttk.Label(self, text="Confirm password")
        self.label_confirm_pwd.grid(row=5, column=0, padx=(15, 0), sticky='W')
        self.confirm_pwd = tk.StringVar()
        tk.Entry(self, textvariable=self.confirm_pwd).grid(
                                                           row=5, 
                                                           column=1, 
                                                           padx=(0,15)
                                                           )
        
        self.error_message = tk.StringVar()
        self.error_message.set("")
    
        self.label_error_message = ttk.Label(
                                            self, 
                                            textvariable = self.error_message, 
                                            foreground="red"
                                            )
        self.label_error_message.grid(row=6, columnspan=2)
        
        
        return_button = ttk.Button(self, text="Back to Login", 
                           command=lambda: self.controller.show_frame(Login))
        return_button.grid(row=7, column=0, padx=10, pady=10)
        
        register_button = ttk.Button(self, text="Register", 
                           command=self._register)
        register_button.grid(row=7, column=1, padx=10, pady=10)
        
    def _register(self):
        
        if not self.first_name.get() or len(self.first_name.get()) > 50:
            self.error_message\
                    .set("You must enter your first name (max 50 chars).")
            return
        elif not self.last_name.get() or len(self.last_name.get()) > 50:
            self.error_message\
                    .set("You must enter your last name (max 50 chars).")
            return
        elif not self.username.get() or len(self.username.get()) > 50:
            self.error_message.set("You must enter a username (max 50 chars).")
            return
        elif not self.password.get():
            self.error_message.set("You must enter a password")
            return
        elif not self.confirm_pwd.get():
            self.error_message.set("You must confirm your password")
            return
            
        existing_user = self.controller.session.query(user.User)\
                            .filter_by(username=self.username.get().lower())\
                             .first()
        
        if existing_user:
            self.error_message.set("Sorry, that username already exists")
            return
        
        if self.password.get() != self.confirm_pwd.get():
            self.password.set("")
            self.confirm_pwd.set("")
            self.error_message.set("Your passwords don't match!")
            return
            
        print("Awesome!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        self.controller.session.add(user.User(
                                         self.first_name.get(),
                                         self.last_name.get(),
                                         self.username.get(),
                                         self.password.get()
                                         ))
        self.controller.session.commit()
        
        self.controller.show_frame(Login)
        
            
    def reset_form(self):
        self.first_name.set("")
        self.last_name.set("")
        self.username.set("")
        self.password.set("")
        self.confirm_pwd.set("")
    
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