reset_query = [
'SET FOREIGN_KEY_CHECKS=0;',
'SET AUTOCOMMIT = 0;',
'DROP TABLE IF EXISTS `Customers`;',
"""CREATE TABLE Customers(
	id INT AUTO_INCREMENT NOT NULL,
	first VARCHAR(50) NOT NULL,
	last VARCHAR(50) NOT NULL,
	street VARCHAR(50) NOT NULL,
	city VARCHAR(50) NOT NULL,
	state VARCHAR(50) NOT NULL,
	phone VARCHAR(50) NOT NULL,
	PRIMARY KEY (id)
);""",
'DROP TABLE IF EXISTS `Employees`;',
"""CREATE TABLE Employees(
	id INT AUTO_INCREMENT NOT NULL,
	first VARCHAR(50) NOT NULL,
	last VARCHAR(50) NOT NULL,
	street VARCHAR(50) NOT NULL,
	city VARCHAR(50) NOT NULL,
	state VARCHAR(50) NOT NULL,
	phone VARCHAR(50) NOT NULL,
	PRIMARY KEY (id)
);""",
'DROP TABLE IF EXISTS `Movies`;',
"""CREATE TABLE Movies(
	movie_id INT AUTO_INCREMENT NOT NULL,
	title VARCHAR(100) NOT NULL,
	stock INT NOT NULL,
	price DECIMAL(16, 2) NOT NULL,
	PRIMARY KEY (movie_id)
);""",
'DROP TABLE IF EXISTS `Actors`;',
"""CREATE TABLE Actors(
	actor_id INT AUTO_INCREMENT NOT NULL,
	first VARCHAR(50) NOT NULL,
	last VARCHAR(50) NOT NULL,
	PRIMARY KEY (actor_id)
);""",

'DROP TABLE IF EXISTS `Orders`;',
"""CREATE TABLE Orders(
	order_id INT AUTO_INCREMENT NOT NULL,
	customer_id INT NOT NULL,
	employee_id INT,
	order_date DATETIME NOT NULL,
	credit_card_num VARCHAR(16) NOT NULL,
	order_fulfilled BOOL NOT NULL DEFAULT 0,
	PRIMARY KEY (order_id),
	FOREIGN KEY (customer_id) REFERENCES Customers(id)
    ON DELETE CASCADE,
	FOREIGN KEY (employee_id) REFERENCES Employees(id)
	ON DELETE CASCADE 
	-- TEMPORARY CASCADE --
);""",

'DROP TABLE IF EXISTS `Order_items`;',
"""CREATE TABLE Order_items(
	order_id INT NOT NULL,
	movie_id INT NOT NULL,
	quantity INT NOT NULL,
	PRIMARY KEY (order_id, movie_id),
	FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    ON DELETE CASCADE,
	FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
    ON DELETE CASCADE
);""",
'DROP TABLE IF EXISTS `Performances`;',
"""CREATE TABLE Performances(
	performance_id INT AUTO_INCREMENT NOT NULL,
	movie_id INT NOT NULL,
	actor_id INT NOT NULL,
	PRIMARY KEY (performance_id),
	FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) 
    ON DELETE CASCADE,
	FOREIGN KEY (actor_id) REFERENCES Actors(actor_id)
    ON DELETE CASCADE
);""",

"""INSERT INTO Customers (first, last, street, city, state, phone)
VALUE ('YJ', 'Park', '2415 Chestnut St', 'Philadelphia', 'PA', '1234567890')""",
"""INSERT INTO Customers (first, last, street, city, state, phone)
VALUE ('San', 'Davran', '1231 Maple St', 'New York City', 'NY', '0987654321')""",
"""INSERT INTO Customers (first, last, street, city, state, phone)
VALUE ('Tupac', 'Shakur', '9807 Oak St', 'Los Angeles', 'CA', '3216540987');""",

"""INSERT INTO Employees (first, last , street, city, state, phone)
VALUE ('Erling', 'Haaland', '3211 Oakview St.', 'Manchester', 'MA', '1111111111'),
('Harry', 'Kane', '3453 Carnaby St', 'London', 'TN', '2222222222'),
('Darwin', 'Nunez', '1315 Bristol St', 'Liverpool', 'UK', '3333333333');""",

"""INSERT INTO Orders (customer_id, employee_id, order_date, credit_card_num, order_fulfilled)
VALUE ('1', '2', '2022-01-11','1111222233334444', 0),
('2', '1', '2022-01-12', '2222333344445555', 1),
('3', '2', '2022-01-01', '3333444455556666', 1),
('2', '3', '2022-01-04', '4444555566667777', 0),
('1', '2', '2022-01-04', '5555666677778888', 0);""",

"""INSERT INTO Movies (title, stock, price)
VALUE ('Aliens', 3, 12.99) , 
( "The Purge" , 13 , 2.99 ) , 
( "The Black Phone" , 21 , 5.99 ) ; """,

"""INSERT INTO Order_items (order_id, movie_id, quantity) 
VALUE ( 1 , (SELECT movie_id FROM Movies WHERE title='The Black Phone') , 4 ) , 
( 1 , (SELECT movie_id FROM Movies WHERE title='The Purge') , 2 ) ,
( 2 , (SELECT movie_id FROM Movies WHERE title='Aliens') , 8 ) , 
( 3 , (SELECT movie_id FROM Movies WHERE title='The Purge') , 5 ) , 
( 4 , (SELECT movie_id FROM Movies WHERE title='Aliens') , 1 ) , 
( 5 , (SELECT movie_id FROM Movies WHERE title='The Purge') , 3 ) ; """,

"""INSERT INTO Actors(first, last)
Value ('Ethan', 'Hawke'), 
('Lena', 'Headey'), 
( 'Max' , 'Burkholder' ) , 
('Adelaide', 'Kane'),  
('Sigourney', 'Weaver'), 
('Michael', 'Biehn'),
('Carrie', 'Henn'),
('Paul', 'Reiser') ,
( "Mason" , "Thames" ) , 
( "Jeremy" , "Davies" ) , 
( "Rebecca" , "Clarke") ; """,

"""INSERT INTO Performances (movie_id, actor_id)
VALUE ( (SELECT movie_id FROM Movies WHERE title='The Purge') , (SELECT actor_id FROM Actors WHERE first='Ethan' AND last='Hawke') ) , 
( (SELECT movie_id FROM Movies WHERE title='The Purge') , (SELECT actor_id FROM Actors WHERE first='Lena' AND last='Headey') ) , 
( (SELECT movie_id FROM Movies WHERE title='The Purge') , (SELECT actor_id FROM Actors WHERE first='Max' AND last='Burkholder') ) , 
( (SELECT movie_id FROM Movies WHERE title='The Purge') , (SELECT actor_id FROM Actors WHERE first='Adelaide' AND last='Kane') ) , 
( (SELECT movie_id FROM Movies WHERE title='Aliens') , (SELECT actor_id FROM Actors WHERE first='Sigourney' AND last='Weaver') ) , 
( (SELECT movie_id FROM Movies WHERE title='Aliens') , (SELECT actor_id FROM Actors WHERE first='Michael' AND last='Biehn') ) , 
( (SELECT movie_id FROM Movies WHERE title='Aliens') , (SELECT actor_id FROM Actors WHERE first='Carrie' AND last='Henn') ) , 
( (SELECT movie_id FROM Movies WHERE title='Aliens') , (SELECT actor_id FROM Actors WHERE first='Paul' AND last='Reiser') ) , 
( (SELECT movie_id FROM Movies WHERE title='The Black Phone') , (SELECT actor_id FROM Actors WHERE first='Mason' AND last='Thames') ) , 
( (SELECT movie_id FROM Movies WHERE title='The Black Phone') , (SELECT actor_id FROM Actors WHERE first='Jeremy' AND last='Davies') ) , 
( (SELECT movie_id FROM Movies WHERE title='The Black Phone') , (SELECT actor_id FROM Actors WHERE first='Rebecca' AND last='Clarke') ) ;""",


'SET FOREIGN_KEY_CHECKS=1;',
'COMMIT;'
]