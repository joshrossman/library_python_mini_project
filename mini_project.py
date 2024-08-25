import re, random
class BookOpperations:
    def __init__(self, title, author,  genre, publication_date, available,*on_loan_to):
        self._title=title
        self._author=author
        self._genre=genre
        self._publication_date=publication_date
        self.availability=available
        self.on_loan_to=on_loan_to

    #Create book okbject and add book object to libarary. Run new data through regex_checker to check that the user input is correct.
    def set_book(self,library):
        self._title=regex_checker(input("Book Name:"),r"^[a-zA-Z1-9.%+-]+","Please input a valid book title")
        self._author=regex_checker(input("Author:"),r"^[a-zA-Z]+\s*(a-zA-Z]+)?.*\s[A-Za-z]+$","Please input a valid name")
        self._genre=regex_checker(input("Genre:"),r"^[a-zA-Z]+$","Please input a valid genre")
        self._publication_date=regex_checker(input("Publication Date: MM/DD/YYYY:"),r"^[0-1][0-9]/[0-3][0-9]/[1-2][0-9][0-9][0-9]$","Please enter a valid date in the following format MM/DD/YYYY")
        library.append(BookOpperations(title,author,genre,publication_date,"Available"))

    #function to borrow book. Changes status of book to borrowed and adds a User object to "on_loan_to", to keep track of who currently has the book.         
    def borrow_book(library, *users):
        in_database=False
        is_available=False
        if len(users[0])>=1:
            my_book=input("What book would you like to take out?")
            for book in library:
                if my_book.lower() ==book.title.lower():
                    in_database=True
                    if book.availability=="Available":
                        in_database=True
                        book.availability="Borrowed"
                        #runs a borrow book function with a UserOperations object, to keep track of which books a user currently has.
                        my_user=UserOperations.borrow_book(users,book)
                        book.on_loan_to=my_user
                        print(f"{book.title} is currently available, and is being checked out to {my_user.name}")
                        return in_database, is_available,book,library     
            if in_database and not is_available:
                print("We do carry this book in our library. However, the book is currently checked out. Please check back in a few days and it may be avialable.")
            if not in_database:
                print("Sorry, but we could not find that title in our library database.")
        else:
            print("We cannot check out any books, as there are currently no users listed in our database. Please first add a user into the system.")      
            
    #Function to return a book to the libary. Changes status to avialbable. Removes the User object from "on_loan_to", and runs the return book function of the UserOpertations object.
    def return_book(library):
        my_book=input("What book are you returning?")
        is_found=False
        is_available=False
        for book in library:
            if my_book.lower()==book.title.lower():
                is_found=True
                my_book=book.title
                if book.availability=="Borrowed":
                    is_available=True
                    print(f"Thank you for returning {book.title} to the library!")
                    book.availability="Available"
                    UserOperations.return_book(book.on_loan_to,book.title)
                    book.on_loan_to=''
                    return library,is_found,is_available
        if is_found and not is_available:  
            print(f"Thank you for trying to return {my_book}. According to our records, that book has not been checked out. Perhaps you are returning it to the wrong library.")
        if not is_found:
            print("We do not have that book in our database. Please check spelling to ensure you are searching correctly.")
    
    #Search library for a book. Return the book if found, or a message indicating that it was not found.
    def get_book(library):
        my_book=input("What book would you like to search for?")
        is_found=False
        for book in library:
            if my_book.lower()==book.title.lower():
                is_found=True
                print(f"\nTitle:{book._title},\nAuthor:{book._author},\nGenre:{book._genre},\nPublication Date:{book._publication_date}\nAvailabiliy: {book.availability}")
                return is_found
        if not is_found:
            print("Sorry we could not find the book you are searching for in our database.")

    #Display all books in the library
    def gets_books(library):
        for book in library:
            print(f"\nTitle:{book._title},\nAuthor:{book._author},\nGenre:{book._genre},\nPublication Date:{book._publication_date}\nAvailabiliy: {book.availability}")

    #user interface for the BookOpperations object. Called from the main function. Writes to the user and book doc after a given oppertation.
    def UI_book_options(library,users):
        while True:
            my_choice=input("Please choose an option by selecting the corresponding number:\n[1]Add a book to the library database\n[2]Check out a book\n[3]Return a book\n[4]Search for a book\n[5]Display all library books.\n[6]Return to main menu\nUser Input:")
            if my_choice=="1":
                BookOpperations.set_book(library)
            elif my_choice=="2":
                BookOpperations.borrow_book(library,users)
            elif my_choice=="3":
                BookOpperations.return_book(library)
            elif my_choice=="4":
                BookOpperations.get_book(library)
            elif my_choice=="5":
                BookOpperations.get_books(library)
            elif my_choice=="6":
                break
            else:
                print("Not a valid choice. Please try again.")
            write_file("book_info.txt", library)
            write_file("user_info.txt", users)

class UserOperations:
    def __init__(self,name,lib_id,borrowed_books):
        self.name=name
        self.lib_id=lib_id
        self.borrowed_books=borrowed_books

    #Keeps track of borrowed books in a list "borrowed_books"
    def borrow_book(users,book):
        while True:
            user_name=input("Please enter the name of the user that is checking out this book:")
            for user in users:
                for my_keys, my_items in user.items():
                    if my_items[0].lower() ==user_name.lower():
                        my_items[2].append(book.title)
                        return my_keys
                    else:
                        continue
            print("Sorry, we could not find that user in our database!")

    #removes borrowed books from list borrowed_books                            
    def return_book(users,book):
        if type(users)==tuple:    
            my_index=users[0].borrowed_books.index(book)
            users[0].borrowed_books.pop(my_index)
            return users[0].name
        else:
            my_index=users.borrowed_books.index(book)
            users.borrowed_books.pop(my_index)
            return users.name

    #Creates a new user Object. Var in_users used to check if user already exsists in list.       
    def new_user(users):
        name=input("Please enter new user's full name:")
        in_users=False
        for user in users:  
            if user.name.lower()==name.lower():  
                in_users=True
                new_user=user

        if in_users==False:   
            new_user=UserOperations(name,UserOperations.create_lib_id(users),[])
            users[new_user]=(new_user.name,new_user.lib_id,new_user.borrowed_books)
            print(f"\nNew User Created!\nName: {new_user.name}\nID:{new_user.lib_id}")
            return users
        else:
            print(f"Cannot create account. This patron already has a library account.\nAccount number: {new_user.lib_id}") 

    #Creates a unique random user ID for new user.    
    def create_lib_id(users):
        while True:  
            max=9999999999
            if len(users)==max:
                raise NoIdsAvailable("All available IDs have been used. Please consider clearing old users/ID, or adjusting program to allow more numbers to be generated(not reccomended.)")     
            lib_id=str(random.randint(0,max))
            floating_zero_filler=''
            for i in range(10-len(lib_id)):
                floating_zero_filler+='0'
            lib_id=floating_zero_filler+lib_id
            lib_ids=[users.values()]
            if not lib_id in lib_ids:
                return lib_id
    #Printe all user details including name, user ID and borrowed books.                         
    def user_details(users):
        in_users=False
        if len(users)>0:
            my_user=input("Which user would you like to retrieve information about?")
            for userinfo in users.values():
                my_books=''
                for book in userinfo[2]:
                    my_books+="\n"+book
                if userinfo[0].lower()==my_user.lower():
                    print(f"\nUser:{userinfo[0]}\nUser ID:{userinfo[1]}\nBorrowed Books:{my_books}")
                    in_users=True
            if in_users==False:
                print("Sorry, but we could not find that user in our system.")
                
        else:
            print("There are currently not users in the system to display.")

    #Diplays details of all users.
    def display_all(users):
        if len(users)>0:
            for user, userinfo in users.items():
                my_books=''
                for book in user.borrowed_books:
                    my_books+=("\n" +book)
                print(f"\nUser: {userinfo[0]}\nLibrary Id:{userinfo[1]}\nBorrowed Books:{my_books}")
        else:
            print("There are currently no users in the system to display.")

    #User interfact of UserOperations object
    def UI_user_operations(users):
        while True:
            my_choice=input("Please choose an option by selecting the corresponding number:\n[1]Add a new user\n[2]Display user details\n[3]Display all users\n[4]Return to main menu\nUser Input:")
            if my_choice=="1":
                UserOperations.new_user(users)
            elif my_choice=="2":
                UserOperations.user_details(users)
            elif my_choice=="3":
                UserOperations.display_all(users)
            elif my_choice=="4":
                break
            else:
                print("Not a valid choice. Please try again.")
            write_file("user_info.txt", users)

# Creates error if no more unique IDs able to be created       
class NoIdsAvailable(Exception):
    def __init__(self,error):
        print(error)

class AuthorOperations:
    def __init__(self, name, biography):
        self.name=name
        self.biography = biography

    #creates a new author and biography
    def add_author(authors):
        author=input("What is the name of the author?")
        biography=input("Please include a short biography about the author:")
        authors.append(AuthorOperations(author, biography))
        write_file("author_info.txt", authors)

    #Displays author information
    def view_details(authors):
        my_author=input("What is the name of the author you would like to search for?")
        in_database=False
        for author in authors:
            if author.name.lower()==my_author.lower():
                in_database=True
                print(f"\nAuthor's name:{my_author}\nBiography:{author.biography}\n")
        if not in_database:
            print("Sorry, we do not have any information about that author in our database!")

    #Displays information of all authors in the system.
    def diplay_all(authors):
        for author in authors:
            print(f"Author: {author.name}\nBiography:{author.biography}")

    #User interface for Authors object
    def UI_Author_Operations(authors):
        while True:  
            my_choice=input("What would you like to do?\n[1]Add new author information\n[2]Search for an author\n[3]Print all authors\n[4]Return to main menu\nUser Input:")
            if my_choice=="1":
                AuthorOperations.add_author(authors)
            elif my_choice=="2":
                AuthorOperations.view_details(authors)
            elif my_choice=="3":
                AuthorOperations.diplay_all(authors)
            elif my_choice=="4":
                break
            else:
                print("Not a valid choice. Please choose from the listed menu items.")

#Variables to hold objects that are created.
users={}
authors=[]
library=[]

#Regex checker to check user inpputed data.
def regex_checker(text,pattern,error):
    while True:
        month= text[0:2]
        days= text[3:5]
        if re.match(pattern,text) and text!='':
            #Extra check to make sure that each month has valid amount of days (leap years not currently taken into account.)
            if pattern==r"^[0-1][0-9]/[0-3][0-9]/[1-2][0-9][0-9][0-9]$":
                if ((month == "09" or month == "04" or month == "06" or month == "11") and (0<int(days)<31)) or (month=="02" and 0<int(days)<30) or ((month=="01" or month=="03" or month=="05" or month=="07" or month =="08" or month =="10" or month=="12") and (0<int(days)<32)):
                    return text
                else:
                    print(month, " ", days)
                    #print(error)
                    text=input("New Input:")   
            else:
                return text
        else:
            print(error)
            text=input("New Input:")

#FileHandling --> Save data to a file
def write_file(file_name, my_data):
    with open(file_name,"w") as file:
        if type(my_data)==dict:
            for my_data in my_data.values():
                my_books=''
                for book in my_data[2]:
                    my_books+=book+"#"
                file.write(str(my_data[0])+":"+str(my_data[1])+":"+str(my_books)+"\n")
        elif type(my_data)==list and file_name=="book_info.txt":
            for an_item in my_data:
                try:
                    file.write(an_item.title+":"+an_item.author+":"+an_item.genre+":"+an_item.publication_date+":"+an_item.availability+":" + an_item.on_loan_to.name+"\n")
                except:
                    file.write(an_item.title+":"+an_item.author+":"+an_item.genre+":"+an_item.publication_date+":"+an_item.availability+":"+"\n")
        elif type(my_data)==list and file_name=="author_info.txt":
            for an_item in my_data:
                file.write(an_item.name+":"+an_item.biography+"\n")
        else:
            print("Error inputting data to text file. The data has not been saved.")        
#DataHandling --> Read the saved data into a dictionary/list when the program opens.
def read_file(file_name,*book):
    global authors, library, users
    with open(file_name, "r") as file:
        if file_name=="author_info.txt":
            try:
                authors=[]
                for line in file:
                    author,biography=line.strip().split(":") 
                    authors.append(AuthorOperations(author, biography))
                    return authors
            except Exception as e:
                authors=[]
                print(f"Error:{e}. Was unable to read file {file_name}. Please check the data to make sure formatting is correct")
        elif file_name=="book_info.txt":
            try:   
                library=[]
                for line in file:
                    title,author,genre,publication_date,available,on_loan_to=line.strip().split(":")
                    on_loan_to=on_loan_to.lower()
                    added=False
                    for user in users:
                        if on_loan_to==user.name.lower():
                            library.append(BookOpperations(title,author,genre,publication_date,available,user))
                            added=True
                    if not added:
                        library.append(BookOpperations(title,author,genre,publication_date,available,UserOperations("","",[])))
                return library
            except Exception as e:
                library=[]
                print(f"Error:{e}. Was unable to read file {file_name}. Either there was no data to read, or the data was not forammted correctly. Please check the data to make sure formatting is correct.")
        elif file_name=="user_info.txt":
            try:   
                users={}
                for line in file:
                    name,lib_id,borrowed_books=line.strip().split(":")
                    borrowed_books=borrowed_books.strip("#").split("#")
                    users[(UserOperations(name,lib_id,borrowed_books))]=(name,lib_id,borrowed_books)
                return users
            except Exception as e:
                library=[]
                print(f"Error:{e}. Was unable to read file {file_name}. Either there was no data to read, or the data was not forammted correctly. Please check the data to make sure formatting is correct.")
        else:
            print("Not a valid library file.")

#Main funtion and main user interface        
def main():
    read_file("user_info.txt")
    read_file("author_info.txt")
    read_file("book_info.txt")
    
    while True:
        my_choice=input("Welcome to the Library Management System!Main Menu:\n[1]Book Operations\n[2]User Operations\n[3]Author Operations\n[4]Quit\nUser Input:")
        if my_choice=='1':
            BookOpperations.UI_book_options(library, users)  
        elif my_choice=='2':
            UserOperations.UI_user_operations(users)
        elif my_choice=='3':
            AuthorOperations.UI_Author_Operations(authors)
        elif my_choice=='4':
            print("Have a great day! Thank you for using the library system!")  
            break  

if __name__=="__main__": 
    main()






